import pandas as pd
import os
import psycopg2
from datetime import datetime

POSTGRES_HOST = os.getenv("POSTGRES_HOST","")
POSTGRES_DB = os.getenv("POSTGRES_DB","")
POSTGRES_TABLE_CONVERSATIONS =  os.getenv("POSTGRES_TABLE_CONVERSATIONS","")
POSTGRES_TABLE_REPORTS = os.getenv("POSTGRES_TABLE_REPORTS","")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME","")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD","")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","")

class PostgreSQLClient:

    def __init__(self):
        
        self.client = psycopg2.connect(
                    dbname=POSTGRES_DB,
                    user=POSTGRES_USERNAME,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
        
        self._init_db()

        print('CLIENT POSTGRES READY')

    
    def _init_db(self):
        """
        This method creates two tables for the persistance of telegram bot data
        TODO: This operation should be made by a migration system
        
        :return: nothing
        :rtype: None
        """
       
        query_conversations = f"""
            CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE_CONVERSATIONS} (
                id SERIAL,
                chat_id VARCHAR NOT NULL,
                content VARCHAR,
                role VARCHAR,
                created_at TIMESTAMP DEFAULT NOW();
            f"""
        
        query_reports = f"""
            CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE_REPORTS} (
                id SERIAL,
                chat_id VARCHAR NOT NULL,
                content VARCHAR,
                severity VARCHAR,
                created_at TIMESTAMP DEFAULT NOW();
            f"""
        
        # Creating a cursor object
        cursor = self.client.cursor()
        try:
            cursor.execute(query_conversations)
            cursor.execute(query_reports)
            self.client.commit()
        except Exception as e: 
            print(e)
            print("POSTGRES ERROR")
        finally:
            # Close the cursor
            cursor.close()

    def insert_message(self, chat_id, role, content):
        """
        This method insert a message into the conversations table
        
        :chat_id: the chat_id from telegram
        :role: who is writing the message
        :content: the content of the message itself
        
        :return: nothing
        :rtype: None
        """
        mex = str(content)
        mex = mex.replace("\\", "\\\\")
        mex = mex.replace("'", "")
        mex = mex.replace("\n", " ")
        mex = mex.replace(";", "")
        # mex = unidecode(mex)

        query = f"""
                    INSERT INTO {POSTGRES_TABLE_CONVERSATIONS}(chat_id, role, content)
                    VALUES ({chat_id}, '{role}','{mex}');
                """
        # Creating a cursor object
        cursor = self.client.cursor()
        try:
            cursor.execute(query)
            self.client.commit()
        except Exception as e: 
            print(e)
            print("POSTGRES ERROR")
        finally:
            # Close the cursor
            cursor.close()

    def get_messages(self, chat_id):
        """
        This method retrieve al messages of a chat
        
        :chat_id: the chat_id from telegram
        
        :return: List of tuples containing all messages of a conversation
        :rtype: List
        """
        query = f"""
                    SELECT * from {POSTGRES_TABLE_CONVERSATIONS}
                    WHERE chat_id = {chat_id}
                    ORDER BY created_at DESC;
                """
        messages = None
        
        # Creating a cursor object
        cursor = self.client.cursor()
        try:
            cursor.execute(query)
            messages = cursor.fetchall()
        except Exception as e: 
            print(e)
            print("POSTGRES ERROR")
        finally:
            # Close the cursor
            cursor.close()

        return messages

    def insert_report(self, chat_id, content, severity):
        """
        This method lets you save on the db a report of a conversation
        
        :chat_id: the chat_id from telegram
        :content: the summary of the conversation
        :severity: the grade of dangerousness of the conversation

        :return: nothing
        :rtype: None
        """
        mex = str(content)
        mex = mex.replace("\\", "\\\\")
        mex = mex.replace("'", "")
        mex = mex.replace("\n", " ")
        mex = mex.replace(";", "")
        # mex = unidecode(mex)

        query = f"""
                    INSERT INTO {POSTGRES_TABLE_REPORTS}(chat_id, content, severity)
                    VALUES ({chat_id}, '{content}','{severity}');
                """
        
        # Creating a cursor object
        cursor = self.client.cursor()
        try:
            cursor.execute(query)
            self.client.commit()
        except Exception as e: 
            print(e)
            print("POSTGRES ERROR")
        finally:
            # Close the cursor
            cursor.close()
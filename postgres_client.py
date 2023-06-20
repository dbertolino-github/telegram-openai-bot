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
        
        # Creating a cursor object
        self.cursor = self.client.cursor()

        print('CURSORS POSTGRES READY')

        # # Register UUID for id_load
        # register_uuid()

    def insert_message(self, chat_id, role, content):

        mex = str(content)
        mex = mex.replace("\\", "\\\\")
        mex = mex.replace("\'", "")
        mex = mex.replace("\n", " ")
        mex = mex.replace(";", "")
        # mex = unidecode(mex)

        query = f"""
                    INSERT INTO {POSTGRES_TABLE_CONVERSATIONS}(chat_id, role, content)
                    VALUES ({chat_id}, '{role}','{mex}');
                """
        try:
            self.cursor.execute(query)
            self.client.commit()
        except:
            print("POSTGRES ERROR")

    def get_messages(self, chat_id):

        query = f"""
                    SELECT * from {POSTGRES_TABLE_CONVERSATIONS}
                    WHERE chat_id IS {chat_id};
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:
            print("POSTGRES ERROR")

    def insert_report(self, chat_id, content, severity):

        mex = str(content)
        mex = mex.replace("\\", "\\\\")
        mex = mex.replace("\'", "")
        mex = mex.replace("\n", " ")
        mex = mex.replace(";", "")
        # mex = unidecode(mex)

        query = f"""
                    INSERT INTO {POSTGRES_TABLE_CONVERSATIONS}(chat_id, content, severity)
                    VALUES ({chat_id}, '{content}','{severity}');
                """
        try:
            self.cursor.execute(query)
            self.client.commit()
        except:
            print("POSTGRES ERROR")

        

    # def retrieve_messages(self, chat_id):

    #     query = f"""
    #                 SELECT chat_id,  {POSTGRES_TABLE_CONVERSATIONS}
    #                 VALUES ('{chat_id}', '{role}','{content}';
    #             """
        
    #     self.cursor.execute(query)
    #     self.client.commit()
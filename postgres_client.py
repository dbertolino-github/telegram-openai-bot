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

class PostgreSQLClient:

    def __init__(self):
        
        self.client = psycopg2.connect(
                    dbname=POSTGRES_DB,
                    user=POSTGRES_USERNAME,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port='5432'
                )
        
        # Creating a cursor object
        self.cursor = self.client.cursor()

        # # Register UUID for id_load
        # register_uuid()

    def insert_message(self, chat_id, role, content):

        query = f"""
                    INSERT INTO {POSTGRES_TABLE_CONVERSATIONS}(chat_id, role, content)
                    VALUES ({chat_id}, '{role}','{content});
                """
        
        self.cursor.execute(query)
        self.client.commit()

    # def retrieve_messages(self, chat_id):

    #     query = f"""
    #                 SELECT chat_id,  {POSTGRES_TABLE_CONVERSATIONS}
    #                 VALUES ('{chat_id}', '{role}','{content}';
    #             """
        
    #     self.cursor.execute(query)
    #     self.client.commit()
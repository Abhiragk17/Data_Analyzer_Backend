# chatbot.py
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_SUFFIX
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os
import traceback
from pathlib import Path

class DataChatbot:
    def __init__(self):
        #self.llm = ChatGoogleGenerativeAI(
        #    model="gemini-1.5-pro",
        #    google_api_key=os.environ["GOOGLE_API_KEY"]
        #)
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            #model="llama-3.1-405b-reasoning",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.environ["GROQ_API_KEY"]
            # other params...
        )
        self.db = None
        self.agent = None
        # Create database directory if it doesn't exist
        self.db_path = Path("database/data.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def setup_database(self, df):
        """Convert DataFrame to SQLite database"""
        try:
            # Create SQLite database in file
            db_url = f"sqlite:///{self.db_path}"
            engine = create_engine(db_url)
            print(f'Database created at {self.db_path}')
            
            # Convert DataFrame to SQLite
            df.to_sql('data', engine, index=False, if_exists='replace')
            print(f'Database populated')
            
            # Create SQLDatabase instance
            self.db = SQLDatabase(engine)
            print(f'SQLDatabase instance created')
            
            # Create SQL agent
            print('Creating SQL toolkit...')
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            print('SQL toolkit created')
            
            # Custom instructions for the agent
            custom_prefix = SQL_PREFIX + """
            You are an expert data analyst with access to a SQL database.
Your job is to help users understand their data through insightful analysis and clear communication.

If someone greets you or says something casual (like "hi", "hello", "thanks"), respond politely and briefly before continuing with the task and stop. 
If the query isnt related to data or SQL analysis, gently guide them back to asking about data insights.

Always reason step-by-step when needed and make sure your responses are understandable by non-technical users.
            """
            
            custom_suffix = """
When responding:
1. Provide detailed, helpful answers based on the data.
2. Clearly explain your reasoning and results in plain language.
3. If clarification is needed, ask for it rather than guessing.

Focus on data.
            """ + SQL_SUFFIX
            
            print('Creating SQL agent...')
            self.agent = create_sql_agent(
                llm=self.llm,
                toolkit=toolkit,
                verbose=True,
                prefix=custom_prefix,
                suffix=custom_suffix,
                handle_parsing_errors=True,
                max_iterations=5
            )
            print(f'SQL agent created')
        except Exception as e:
            print(f"Error in setup_database: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise

    def chat(self, query):
        """Process user query and return response"""
        if not self.agent:
            return "Please upload a dataset first."
        
        try:
            print(f"Processing query: {query}")
            response = self.agent.invoke({"input": query})
            print(f"Response: {response}")
            return response['output']
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return f"Error processing query: {str(e)}"
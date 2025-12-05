import os
from autogen import AssistantAgent, UserProxyAgent, register_function
from agents.retriever import retrieve_schema
from agents.critic import validate_sql
from agents.sql_executor import run_sql
import pandas as pd
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()

# Global state to capture results from tools
class OrchestratorState:
    def __init__(self):
        self.last_sql = None
        self.last_df = None
        self.last_msg = ""
    
    def reset(self):
        self.last_sql = None
        self.last_df = None
        self.last_msg = ""

state = OrchestratorState()

# Wrapper functions for tools
def retrieve_schema_tool(question: Annotated[str, "The natural language question"]) -> str:
    return retrieve_schema(question)

def validate_sql_tool(sql: Annotated[str, "The SQL query to validate"]) -> str:
    valid, msg = validate_sql(sql)
    if not valid:
        return f"Invalid SQL: {msg}"
    return "SQL is valid."

def run_sql_tool(sql: Annotated[str, "The SQL query to execute"]) -> str:
    state.last_sql = sql
    try:
        df = run_sql(sql)
        state.last_df = df
        state.last_msg = "Query executed successfully."
        if df.empty:
            return "Executed successfully but returned no rows."
        return f"Executed successfully. Result preview:\n{df.head().to_markdown()}"
    except Exception as e:
        state.last_msg = f"Error: {str(e)}"
        return f"Error executing SQL: {str(e)}"

class AutoGenSQLOrchestrator:
    def answer_question(self, question: str):
        # Reset state
        state.reset()

        # Define Agents
        user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: (x.get("content") or "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )

        assistant = AssistantAgent(
            name="sql_assistant",
            system_message="""You are an expert SQL assistant.
            1. Retrieve the schema for the question.
            2. Generate a SQL query.
            3. Validate the SQL query using the validator tool.
            4. Execute the SQL query using the executor tool.
            5. If successful, reply with 'TERMINATE'.
            If there is an error, try to fix it.
            IMPORTANT: Always use the tools provided. Do not hallucinate schema or results.""",
            llm_config={
                "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}],
                "cache_seed": None
            }
        )

        # Register Tools
        register_function(
            retrieve_schema_tool,
            caller=assistant,
            executor=user_proxy,
            name="retrieve_schema",
            description="Retrieve database schema based on the question."
        )

        register_function(
            validate_sql_tool,
            caller=assistant,
            executor=user_proxy,
            name="validate_sql",
            description="Validate if a SQL query is safe and correct."
        )

        register_function(
            run_sql_tool,
            caller=assistant,
            executor=user_proxy,
            name="run_sql",
            description="Execute a SQL query and get the results."
        )

        # Start Chat
        user_proxy.initiate_chat(
            assistant,
            message=question
        )

        return state.last_sql, state.last_msg, state.last_df

# Singleton instance
orchestrator = AutoGenSQLOrchestrator()

def answer_question(question):
    return orchestrator.answer_question(question)

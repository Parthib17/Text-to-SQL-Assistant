# Text-to-SQL Assistant - Technical Documentation

This document provides a detailed technical overview of the **Text-to-SQL Assistant**, an application that converts natural language questions into executable SQL queries. It leverages **OpenAI's GPT models** for reasoning, **ChromaDB** for RAG (Retrieval-Augmented Generation), and **Streamlit** for the user interface.

## 🏗️ Architectural Overview

The application follows a **sequential pipeline architecture** to process user queries.

### High-Level Data Flow

1.  **User Input**: The user asks a question via the Streamlit UI (e.g., "Show me top 5 customers").
2.  **Orchestration**: The request is passed to the `answer_question` function in `orchestrator.py`.
3.  **Pipeline Execution**:
    1.  **Schema Retrieval (RAG)**: The system searches for relevant database tables using vector embeddings (ChromaDB).
    2.  **SQL Generation**: The LLM generates a SQL query based on the retrieved schema.
    3.  **Validation**: A critic module checks the SQL for safety (preventing `DROP`, `DELETE`, etc.).
    4.  **Execution**: The validated SQL is run against a MySQL database.
4.  **Response**: The results (Dataframe) and the generated SQL are sent back to the UI.

---

## 🧩 Modules & Components

The core logic resides in the `agents/` directory (note: while named `agents`, these are now functional modules in the pipeline).

### 1. Orchestrator (`agents/orchestrator.py`)
This is the simple pipeline controller.

*   **Function**: `answer_question(question)`
*   **Logic**: Sequentially calls retrieval, generation, validation, and execution steps. Returns the SQL, validation message, and result DataFrame.

### 2. Schema Retriever (`agents/retriever.py`)
Implements **Retrieval-Augmented Generation (RAG)** to provide context to the LLM. It avoids feeding the entire database schema to the LLM context window.

*   **Database**: Uses **ChromaDB** to store vector embeddings of table schemas.
*   **Embeddings**: Uses `text-embedding-3-small` to convert questions and table descriptions into vectors.
*   **Process**:
    *   `retrieve_schema(question)` queries the vector store for the top 3 most relevant tables.
    *   Returns a formatted string containing Table Name, Columns, and Description.

### 3. SQL Critic / Validator (`agents/critic.py`)
A safety layer to ensure the generated SQL is safe to execute.

*   **Function**: `validate_sql(sql)`
*   **Checks**: Scans for dangerous keywords like `DROP`, `DELETE`, `UPDATE`, `ALTER`.
*   **Result**: Returns `True` if safe, otherwise `False` with an error message.

### 4. SQL Executor (`agents/sql_executor.py`)
Handles the actual interaction with the MySQL database.

*   **Library**: `mysql.connector`
*   **Function**: `run_sql(sql)`
*   **Output**: Executes the query and returns the result as a **Pandas DataFrame**.

---

## 📂 Directory Structure

```plaintext
text_to_sql/
├── agents/
│   ├── orchestrator.py          # Main pipeline controller
│   ├── critic.py                # SQL validation logic
│   ├── retriever.py             # RAG logic with ChromaDB
│   ├── sql_executor.py          # MySQL database connection & execution
│   └── sql_generator.py         # SQL generation logic
├── db/
│   └── mysql_connection.py      # Database helper scripts
├── chroma_store/                # Persisted Vector Database (ChromaDB)
├── app.py                       # Streamlit Entry Point
├── build_schema_store.py        # Script to index schema into ChromaDB
├── requirements.txt             # Project Dependencies
└── .env                         # Environment variables (API Keys, DB Creds)
```

---

## 🚀 Setup & Usage

### Prerequisites
*   Python 3.8+
*   MySQL Database
*   OpenAI API Key

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file with the following:
    ```ini
    OPENAI_API_KEY=your_key_here
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=your_db
    ```

4.  **Build Schema Store**:
    Run this once to populate ChromaDB with your database schema:
    ```bash
    python build_schema_store.py
    ```

5.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

---

## 🛠️ Interaction Diagram

```mermaid
graph TD
    User[User (Streamlit UI)] --> Orchestrator[Orchestrator]
    Orchestrator --> Retriever[Retriever (ChromaDB)]
    Orchestrator --> Generator[SQL Generator (LLM)]
    Orchestrator --> Critic[Critic (Validator)]
    Orchestrator --> Executor[Executor (MySQL)]
    
    Retriever -- Schema Context --> Generator
    Generator -- Generated SQL --> Critic
    Critic -- Validation Status --> Orchestrator
    
    Orchestrator -- If Valid --> Executor
    Executor -- DataFrame --> Orchestrator
    
    Orchestrator --> User
```

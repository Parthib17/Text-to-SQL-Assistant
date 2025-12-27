import streamlit as st
from agents.orchestrator import answer_question
import time

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    .sql-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>Text-to-SQL Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Transform natural language into powerful SQL queries</p>", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.markdown("### About")
    st.info("""
    This assistant uses AI to convert your natural language questions 
    into SQL queries and executes them against your database.
    """)
    
    st.markdown("### Example Questions")
    st.markdown("""
    - List all the products
    - Show me all customers from London
    - What are the top 5 products by revenue?
    """)

# Main content area
st.markdown("---")

# Query input section
st.markdown("### Ask Your Question")
question = st.text_area(
    label="Enter your question",
    placeholder="e.g., Show all the customers details...",
    height=100,
    label_visibility="collapsed"
)

# Generate button with better spacing
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button("Generate SQL & Execute", use_container_width=True)

# Process query
if generate_button:
    if not question:
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Processing your question..."):
            # Simulate progress
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            try:
                sql, msg, df = answer_question(question)
                
                st.success("Query processed successfully!")
                
                # SQL Query Section
                st.markdown("---")
                st.markdown("### Generated SQL Query")
                st.code(sql, language="sql")
                
                # Add copy button info
                st.caption("Tip: Click the copy icon in the top-right of the code block to copy the SQL")
                
                # Validation Section
                st.markdown("---")
                st.markdown("### Validation Results")
                
                if "success" in msg.lower() or "valid" in msg.lower():
                    st.success(msg)
                elif "warning" in msg.lower():
                    st.warning(msg)
                else:
                    st.info(msg)
                
                # Results Section
                if df is not None and not df.empty:
                    st.markdown("---")
                    st.markdown("### Query Results")
                    
                    # Display metrics if applicable
                    if len(df) > 0:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Rows", len(df))
                        with col2:
                            st.metric("Total Columns", len(df.columns))
                        with col3:
                            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                    
                    # Display dataframe with better formatting
                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=400
                    )
                    
                    # Download option
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                elif df is not None:
                    st.info("Query executed successfully but returned no results.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6c757d;'>Parthib Mitra</p>",
    unsafe_allow_html=True
)
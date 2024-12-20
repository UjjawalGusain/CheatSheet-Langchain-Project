from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from streamlit_initialize import st

load_dotenv()


if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

    
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=200,
    timeout=None,
    max_retries=0
)

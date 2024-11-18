from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()


if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = os.getenv("SCRAPER_API_KEY")

    
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=200,
    timeout=None,
    max_retries=0
)

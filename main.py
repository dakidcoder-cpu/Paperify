from dotenv import load_dotenv
import warnings
import os
import glob
warnings.filterwarnings("ignore")

from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()
class ResearchResponse(BaseModel):
    title: str
    topic: str
    summary: str
    key_points: list[str]
    references: list[str]
    sources: list[str]
llm = ChatGroq(model="llama-3.1-8b-instant", )
output_parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant named Paperify.
            IMPORTANT: If someone asks "who are you" or any variation, ALWAYS respond ONLY with: "I am Paperify, a research assistant."
            Never mention that you are llama or any model name.
            For other queries, answer the user query and use necessary tools. 
            Research from the internet and wikipedia or make a prediction.
            Provide a clear, concise answer without extra formatting.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

tools = [search_tool, wiki_tool, save_tool]
agent = create_react_agent(
    model=llm,
    tools=tools,
)

agent_executor = agent

def run_query(query: str) -> str:
    """Run the agent on `query` and return the final plain-text answer.

    This function short-circuits identity questions, ensures generated
    text files are removed, and returns an error string on exception.
    """
    try:
        q = query.lower().strip()
        if q in ["who are you", "who are you?", "what are you", "what are you?"]:
            return "I am Paperify, a research assistant. I give you help in making research papers."

        raw_response = agent_executor.invoke({"messages": [("human", query)]})

        messages = raw_response.get("messages", [])
        final_message = None
        for msg in reversed(messages):
            if hasattr(msg, 'content') and msg.content and not msg.content.isspace():
                final_message = msg.content
                break

        return final_message or "No response generated."
    except Exception as e:
        return f"Error processing response: {e}"
    finally:
        # Delete any generated txt files
        for file in glob.glob("*.txt"):
            try:
                os.remove(file)
            except Exception:
                pass


if __name__ == "__main__":
    q = input("What can i help you research? ")
    print(run_query(q))

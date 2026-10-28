from dotenv import load_dotenv
import os
import requests
load_dotenv()

from langchain_groq import ChatGroq 
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from rich import print
from langchain.agents.middleware import wrap_tool_call
# Creating Tool

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_research(query:str ) -> str:
    """Provide all the information from web"""
    response = tavily_client.search(
        query = f"latest information on {query}",
        search_depth = "basic",
        max_results = 3
    )
    
    results = response.get("results",[])
    
    if not results:
        print(f"no result found for {query}")
    
    research_list = []
    
    for item in results:
        title = item.get("title", "No title")
        url = item.get("url", "")
        content = item.get("content", "")

        research_list.append(
            f"Title:{title}\n"
            f"URL:{url}\n"
            f"Content:{content}\n"
        )            
    return("Latest information on {web}:\n\n" + "\n\n".join(research_list))

# LLM Setup
 
llm = ChatGroq(model="openai/gpt-oss-120b")

@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call"""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'.Approve? (Yes/No):")
    
    if confirm.lower() == "no":
        return ToolMessage(
        content = "Tool call denied for user.",
        tool_call_id = request.tool_call["id"]
    )
    return handler(request)

Agent = create_agent(
    llm,
    tools= [web_research],
    system_prompt= "You are a helpful web information assistant",
    middleware= [human_approval]
)

print("Web Information Retriever | type exit if quit")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    result = Agent.invoke({
        "messages": [{"role":"user", "content":user_input}]
    })
    print("bot : ", result['messages'][-1].content )
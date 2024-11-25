from copy import deepcopy
import json
from flask import current_app, g
from langchain_openai import ChatOpenAI
import requests
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import InjectedToolArg, tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode, create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState
from typing_extensions import Annotated

class Question(BaseModel):
  '''Question to ask user.'''
  question: str = Field(..., description="Question about user's intent.")
  answers: List[str] = Field(..., description="Potential answers to this question.")

class Questions(BaseModel):
  '''Response to the user.'''
  questions: List[Question] = Field(..., description="List of questions to figure out the user's intent.")

@tool
def all_of_tag(tag: str):#, soup: Annotated[BeautifulSoup, InjectedToolArg]):
  '''First, use this to retrieve information about the webpage.

  Args:
    tag: html tag we want to retrieve all occurences of
  '''
  return { tag: list(map(lambda item: item.string.strip(), g.soup.find_all(tag))) }

@tool
def get_tag(tag: str):#, soup: Annotated[BeautifulSoup, InjectedToolArg]):
  '''First, use this to retrieve information about the webpage.

  Args:
    tag: html tag we want to retrieve first occurrence of
  '''
  return g.soup.find(tag)

def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()
  g.soup = BeautifulSoup(r.content, 'html.parser') # TODO don't set this in global variable. Pass it in hidden from llm.

  tools = [all_of_tag, Questions]

  config = {"configurable": {"thread_id": "test-thread"}}
  memory = MemorySaver()
  system_msg = "You ask questions to website visitors to help sort them based on intent. First, use the all_of_tag tool to gather information about the website. Finally, format them using the Questions tool."

  agent_executor = create_react_agent(llm, tools, state_modifier=system_msg, checkpointer=memory)
  output = agent_executor.invoke({ "messages": [("user", "Visitor to apple.com")]}, config)
  print("Full convo: ", output["messages"])

  print("\nOutput: ", output["messages"][-1].content)

  return output["messages"][-1].content

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  out = all_of_tag("h2", soup)
  print(json.dumps(out))
  return out

from copy import deepcopy
import json
from flask import current_app
from langchain_openai import ChatOpenAI
import requests
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import InjectedToolArg, tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
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
def all_of_tag(tag: str, soup: Annotated[BeautifulSoup, InjectedToolArg]):
  '''First, use this to retrieve information about the webpage.

  Args:
    tag: html tag we want to retrieve all occurences of
  '''
  return { tag: list(map(lambda item: item.string.strip(), soup.find_all(tag))) }

@tool
def get_tag(tag: str, soup: Annotated[BeautifulSoup, InjectedToolArg]):
  '''First, use this to retrieve information about the webpage.

  Args:
    tag: html tag we want to retrieve first occurrence of
  '''
  return soup.find(tag)

# def call_model(state: AgentState):
#   messages = state["messages"]
#   last_message = messages[-1]
#   if len(last_message.tool_calls) == 1 and last_message.tool_calls[0]




def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()
  soup = BeautifulSoup(r.content, 'html.parser')

  messages = [
    SystemMessage(content="First, use the all_of_tag tool to gather information about a website until you can formulate questions to ask the user."),
    SystemMessage(content="Finally, format them using the Questions tool"),
    SystemMessage(content="Information about the contents of the website comes from all_of_tag."),
  ]

  tools = [all_of_tag, Questions]

  llm_with_tools = llm.bind_tools(tools, tool_choice="any", strict=True)
  llm_output = llm_with_tools.invoke(messages)
  # print("llm_output 1 ", llm_output)
  messages.append(llm_output)
  tool_mapping = { "all_of_tag": all_of_tag, "Questions": Questions, "get_tag": get_tag }

  print("All the tool_calls ", llm_output.tool_calls)

  # tool_node = ToolNode(tools)
  # workflow = StateGraph()

  for tool_call in llm_output.tool_calls:
    # if I intend to extend this logic, should use langgraph for llm logic instead
    tool = tool_mapping[tool_call["name"]]
    call = deepcopy(tool_call)
    call["args"]["soup"] = soup
    tool_output = tool.invoke(call["args"])
    tool_msg = ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call["id"])
    print("\nTool msg: ", tool_msg)
    messages.append(tool_msg)
    # print("\nmessages: ", messages)
  messages.append("Format your response using the Questions tool")
  print("Made it to here. ", len(tool_call))
  print("Tool output ", tool_output)
  questions = llm_with_tools.invoke(messages)

  tool_call_final = questions.tool_calls
  print("\nTool call final: ", tool_call_final)



  q_index = -1 #tool_call_final.index(lambda e: True if e["name"] == 'Questions' else False)
  final = {}
  for call in questions.tool_calls:
    if call["name"] == "Questions":
      final = call
      break
  if (len(final.keys()) == 0):
    raise Exception("No Questions in output. " + str(questions.tool_calls))
  print("\nFinal: ", final)
  print("\nfinal answer: ", final["args"]["questions"])

  return final["args"]["questions"]

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  out = all_of_tag("h2", soup)
  print(json.dumps(out))
  return out

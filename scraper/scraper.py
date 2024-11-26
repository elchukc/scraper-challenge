import json
from flask import current_app, g
import requests
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import InjectedToolArg, tool
from langgraph.prebuilt import ToolNode, create_react_agent
from langgraph.graph import StateGraph, MessagesState, END
from typing_extensions import Annotated

class Question(BaseModel):
  '''Question to ask user.'''
  question: str = Field(..., description="Question about user's intent.")
  answers: List[str] = Field(..., description="Potential answers to this question.")

class Questions(BaseModel):
  '''Response to the user.'''
  questions: List[Question] = Field(..., description="List of questions to figure out the user's intent.")

# Inherit 'messages' key from MessagesState, which is a list of chat messages
class AgentState(MessagesState):
  # Final structured response from the agent
  final_response: Questions

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


# Define the function that responds to the user
def respond(state: AgentState):
  # Construct the final answer from the arguments of the last tool call
  response = Questions(**state["messages"][-1].tool_calls[0]["args"])
  # We return the final answer
  return {"final_response": response}

# Determine whether to continue or not
def should_continue(state: AgentState):
  messages = state["messages"]
  last_message = messages[-1]
  # If there is only one tool call and it is the response tool call we respond to the user
  if (
    len(last_message.tool_calls) == 1
    and last_message.tool_calls[0]["name"] == "Questions"
  ):
    return "respond"
  # Otherwise we will use the tool node again
  else:
    return "continue"

def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()
  g.soup = BeautifulSoup(r.content, 'html.parser') # TODO don't set this in global variable. Pass it in hidden from llm.

  tools = [all_of_tag, Questions]

  def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

  model_with_tools = llm.bind_tools(tools, tool_choice="any")

  workflow = StateGraph(AgentState)
  workflow.add_node("agent", call_model)
  workflow.add_node("respond", respond)
  workflow.add_node("tools", ToolNode(tools))

  workflow.set_entry_point("agent")
  workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "respond": "respond"})
  workflow.add_edge("tools", "agent")
  workflow.add_edge("respond", END)
  graph = workflow.compile()

  output = graph.invoke(input={"messages": [("user", "Visitor to apple.com")]})["final_response"]
  print("Output: ", output)
  return output.model_dump(mode='json')

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  out = all_of_tag("h2", soup)
  print(json.dumps(out))
  return out

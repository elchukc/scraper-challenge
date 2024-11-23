from copy import deepcopy
import json
import requests
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import InjectedToolArg, tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from typing_extensions import Annotated

# r = requests.get('https://realpython.github.io/fake-jobs/')
# r = requests.get("https://www.chatsimple.ai/")
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
  return list(map(lambda item: item.string.strip(), soup.find_all(tag)))

@tool
def get_tag(tag: str, soup: Annotated[BeautifulSoup, InjectedToolArg]):
  '''First, use this to retrieve information about the webpage.

  Args:
    tag: html tag we want to retrieve first occurrence of
  '''
  return soup.find(tag)
  # return list(map(lambda item: item.string.strip(), soup.find_all(tag)))

def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()
  soup = BeautifulSoup(r.content, 'html.parser')
  # soup = BeautifulSoup("<div>foo</div>", "html.parser")

  messages = [
    SystemMessage(content="First, use the all_of_tag tool to gather information about a website until you can formulate questions to ask the user."),
    SystemMessage(content="Questions should help you sort these visitors based on intent."),
    SystemMessage(content="Finally, format them into the Questions tool"),
  ]

  llm_with_tools = llm.bind_tools([all_of_tag], tool_choice="any") #, tool_choice="any", strict=True)
  llm_output = llm_with_tools.invoke(messages)
  # print("llm_output 1 ", llm_output)
  messages.append(llm_output)
  tool_mapping = { "all_of_tag": all_of_tag, "Questions": Questions, "get_tag": get_tag }

  for tool_call in llm_output.tool_calls:
    # if I intend to extend this logic, should use langgraph for llm logic instead
    tool = tool_mapping[tool_call["name"]]
    call = deepcopy(tool_call)
    call["args"]["soup"] = soup
    tool_output = tool.invoke(call["args"])
    tool_msg = ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call["id"])
    messages.append(tool_msg)
  print("Made it to here. ", len(tool_call))
  print("Tool output ", tool_output)
  # for msg in messages:
    # print(msg)
  # print("~~~Messages before final invoke ", messages)
  questions = llm_with_tools.invoke(messages)
  print("QUESTIONS ", questions.content)

  return questions.content

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  out = all_of_tag("h2", soup)
  print(json.dumps(out))
  return out

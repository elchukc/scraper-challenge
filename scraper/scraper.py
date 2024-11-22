import requests
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

# r = requests.get('https://realpython.github.io/fake-jobs/')
# r = requests.get("https://www.chatsimple.ai/")
class Question(BaseModel):
  '''Question to ask user.'''
  question: str = Field(..., description="Question about user's intent.")
  answers: List[str] = Field(..., description="Potential answers to this question.")

class Questions(BaseModel):
  '''Response to the user.'''
  questions: List[Question] = Field(..., description="List of questions to figure out the user's intent.")

def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()
  soup = BeautifulSoup(r.content, 'html.parser')

  def all_of_tag(tag: str):
    '''Use this to retrieve information about the webpage.

    Args:
      tag: html tag we want to retrieve all occurences of
    '''
    return list(map(lambda item: item.string.strip(), soup.find_all(tag)))

  messages = [
    # (
    #   "system",
    #   "Take some info scraped from a website and figure out what kind of visitors visit it."
    # ),
    # (
    #   "system",
    #   "Then ask some questions to help you sort these visitors based on intent."
    # ),
    # (
    #   "human",
    #   "title: {}, {}".format(soup.title, all_of_tag('h2')),
    # ),

    SystemMessage(content="Use tool all_of_tag to retrieve content from a website and figure out what kind of visitors visit it."),
    SystemMessage(content="Then ask some questions to help you sort these visitors based on intent."),
  ]
  # parser = PydanticOutputParser(pydantic_object=Questions)
  # prompt = ChatPromptTemplate(messages).partial(format_instructions=parser.get_format_instructions())

  llm_with_tools = llm.bind_tools([all_of_tag]) #, tool_choice="any", strict=True)
  questions = llm_with_tools.invoke(messages)
  print("QUESTIONS ", questions.content)

  return questions.content

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

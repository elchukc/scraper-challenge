import requests
from bs4 import BeautifulSoup
from typing_extensions import Annotated, TypedDict, List

# r = requests.get('https://realpython.github.io/fake-jobs/')
# r = requests.get("https://www.chatsimple.ai/")
class Question(TypedDict):
  '''Question to ask user.'''
  question: Annotated[str, ..., "Question about user's intent."]
  answers: Annotated[List[str], ..., "Potential answers to this question."]

def req():
  from . import chatbot
  # r = requests.get('https://realpython.github.io/fake-jobs/')
  r = requests.get('https://www.apple.com/')
  llm = chatbot.connect_ai()

  soup = BeautifulSoup(r.content, 'html.parser')

  messages = [
    (
      "system",
      "Take some info scraped from a website and figure out what kind of visitors visit it."
    ),
    (
      "system",
      "Then ask some questions to help you sort these visitors based on intent."
    ),
    (
      "human",
      "title: {}, {}".format(soup.title, all_of_tag(soup, 'h2')),
    ),
  ]
  structured_llm = llm.with_structured_output(Question)
  questions = structured_llm.invoke(messages)
  print(questions)

  return questions

def all_of_tag(soup: BeautifulSoup, tag: str):
  return list(map(lambda item: item.string.strip(), soup.find_all('h2')))

def soup():
  r = requests.get('https://www.apple.com/')
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

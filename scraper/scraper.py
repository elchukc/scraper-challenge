import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from flask import current_app

# r = requests.get('https://realpython.github.io/fake-jobs/')
# r = requests.get("https://www.chatsimple.ai/")

def req():
  r = requests.get('https://realpython.github.io/fake-jobs/')
  soup = BeautifulSoup(r.content, 'html.parser')
  # current_app.config['OPENAI_API_KEY']
  # for link in soup.findAll('a'):
  #   print(link)
  out = list(map(lambda item: item.string, soup.find_all('h2')))
  return out

def soup():
  r = requests.get('https://realpython.github.io/fake-jobs/')
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

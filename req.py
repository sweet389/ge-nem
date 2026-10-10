import requests
from pprint import pprint
from debug import debug
from dotenv import load_dotenv
import os
load_dotenv()
url=os.getenv('api-url')

def get_exam_by_year(year,args=[]):
  payload=url+year
  for param in args:
    payload+=f"{param}/"
  debug(payload, __file__)
  req=requests.get(payload)
  #pprint(req.content.decode(), compact=True)
  return req.json()
#get_exam_by_year("2010")

def get_exam_questions_by_year(year,args=[]):
  payload=url+year+"/questions"
  for param in args:
    payload+=f"{param}/"
  debug(payload, __file__)
  req=requests.get(payload)
  #pprint(req.content.decode())
  return req.json()

def get_exam_question_by_discipline(year,discipline,limit="10"):
  payload=url+year+"/questions?limit="+limit+"&discipline="+discipline
  debug(payload, __file__)
  req=requests.get(payload)
  pprint(req.content.decode(), compact=True)
#get_exam_question_by_discipline("2010", "ingles")


def get_exam_question_by_index(year,index):
  payload=url+year+"/questions/"+index
  debug(payload, __file__)
  req=requests.get(payload)
  pprint(req.content.decode(), compact=True)
  return req.json()
#get_exam_question_by_index("2010", "1")

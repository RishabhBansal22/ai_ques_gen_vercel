from .config import google_api_key
from prompts.sysprompt import sys_prompt, sys_answer_prompt
from google import genai
from google.genai import types

try:
   client = genai.Client(
    api_key= google_api_key,
    vertexai=False
    )
except:
   print("problem with generator client")

def generate_response(user_prompt):
   response = client.models.generate_content(
      model = "gemini-2.0-flash",
      config= types.GenerateContentConfig(
         system_instruction= sys_prompt
      ),
      contents = user_prompt
   )
   return response.text
    
def generate_answers(questions):
   response = client.models.generate_content(
      model = "gemini-2.0-flash",
      config= types.GenerateContentConfig(
         system_instruction= sys_answer_prompt
      ),
      contents = questions
   )
   return response.text
    






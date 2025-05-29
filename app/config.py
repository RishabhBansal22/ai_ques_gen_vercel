from dotenv import load_dotenv
import os
load_dotenv()

try:
   google_api_key = os.getenv('api_key')
except:
   print("there is a problem with config")

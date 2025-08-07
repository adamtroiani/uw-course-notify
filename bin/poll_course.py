import requests
import argparse
from time import sleep

SERVER_URL = "http://0.0.0.0:8000"
  
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Check course capacity")
  parser.add_argument("course_code", help="Course code to check (i.e. CLAS 202)")
  args = parser.parse_args()
  
  while True:
    requests.get(SERVER_URL+f"/availability/{args.course_code}/1259")
    sleep(5)

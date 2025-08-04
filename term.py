import requests
import yaml
import json 

BASE_URL = "https://openapi.data.uwaterloo.ca/v3"
API_KEYS_PATH = ".env/api_keys.yaml"

next_start_month = {
  "1": ("5", 0),
  "5": ("9", 0),
  "9": ("1", 1),
}

def get_term_code(next_term:bool):
  print("Getting term code...")
  url = f"{BASE_URL}/Terms/current"
  
  headers = {}
  with open(API_KEYS_PATH, "r") as file:
    api_keys = yaml.safe_load(file)
    headers["x-api-key"] = api_keys.get("uwaterloo")

  response = requests.get(url, headers=headers).json()
  current_term = response["termCode"]
  
  if not next_term:
    return current_term
  
  year = current_term[1:3]
  start_month = current_term[3]
  
  start_month, carry = next_start_month[start_month]
  return "1"+str(int(year)+carry)+start_month

if __name__ == "__main__":
  print(get_term_code(next_term = True))
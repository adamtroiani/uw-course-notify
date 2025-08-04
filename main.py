import requests
import argparse
import yaml

DEBUG = True

BASE_URL = "https://openapi.data.uwaterloo.ca/v3"
API_KEYS_PATH = ".env/api_keys.yaml"

def format_section_info(section):
  course_id = section["courseId"]
  section_num = section["classSection"]
  campus = section["locationName"]
  
  
  # classes = section["classes"]
  time = "0"
  # time = classes[0]["date"]["start_time"] + "-" + classes[0]["date"]["end_time"]
  
  return f"id:{course_id}, section:{section_num} ({campus}) [{time}]"
  
def has_capacity(course, term_code):
  print(f"Checking capacity for {course}...")
  course_subject, catalog_number = course.split(" ")
  url = f"{BASE_URL}/ClassSchedules/{term_code}/{course_subject}/{catalog_number}"
  
  headers = {}
  with open(API_KEYS_PATH, "r") as file:
    api_keys = yaml.safe_load(file)
    headers["x-api-key"] = api_keys.get("uwaterloo")

  response = requests.get(url, headers=headers).json()
  if DEBUG:
    print(response)
    
  if isinstance(response, dict):
    print("Course not found")
    return
  
  data = response[0]
  enrollment_capacity = data["maxEnrollmentCapacity"]
  enrollment_total = data["enrolledStudents"]

  if enrollment_total < enrollment_capacity:
    print(format_section_info(data["scheduleData"]))
  else:
    print(f"{course} is currently full")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Check course capacity")
  parser.add_argument("course_code", help="Course code to check (i.e. CLAS 202)")
  parser.add_argument("term_code", help="Term you wish to take the course")
  args = parser.parse_args()
  
  has_capacity(args.course_code, args.term_code)

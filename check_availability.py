import requests
import yaml
import json 
import argparse
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://openapi.data.uwaterloo.ca/v3"
API_KEYS_PATH = ".env/api_keys.yaml"

def format_section_info(section, cur_enrollment):
  course_component = section["courseComponent"]
  section_num = section["classSection"]
  
  schedule_data = section["scheduleData"][0]
  try:
    start_time =  schedule_data["classMeetingStartTime"].split("T")[1]
    end_time =  schedule_data["classMeetingEndTime"].split("T")[1]
    class_days = schedule_data["classMeetingDayPatternCode"]
    if start_time == end_time:
      time = "ONLINE"
    else:
      time = f"{start_time}-{end_time} {class_days}"
  except:
    time = "null"
  
  return f"{course_component} {section_num} ({cur_enrollment}) [{time}]"
  
def check_availability(course, term_code):
  logger.info(f"Checking capacity for {course}...")
  course_subject, catalog_number = course.split(" ")
  url = f"{BASE_URL}/ClassSchedules/{term_code}/{course_subject}/{catalog_number}"
  
  headers = {}
  with open(API_KEYS_PATH, "r") as file:
    api_keys = yaml.safe_load(file)
    headers["x-api-key"] = api_keys.get("uwaterloo")

  response = requests.get(url, headers=headers).json()
  response = list(filter(lambda section: section["courseComponent"] == "LEC", response))
  response.sort(key=lambda section: section["classSection"])
  with open(".debug/response.json", "w") as file:
    file.write(json.dumps(response, indent=2))
    
  if isinstance(response, dict):
    logger.error("Course not found")
    return
  
  res = []
  for section in response:
    enrollment_capacity = section["maxEnrollmentCapacity"]
    enrollment_total = section["enrolledStudents"]

    if enrollment_total < enrollment_capacity:
      res.append(format_section_info(section, f"{enrollment_total}/{enrollment_capacity}"))
  
  return res

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Check course capacity")
  parser.add_argument("course_code", help="Course code to check (i.e. CLAS 202)")
  parser.add_argument("term_code", help="Term you wish to take the course")
  args = parser.parse_args()
  
  availabilities = check_availability(args.course_code, args.term_code)
  if availabilities:
    print("Openings:")
    for section in availabilities:
      print(f"  {section}")
  else:
    print(f"{args.course_code} is currently full.")

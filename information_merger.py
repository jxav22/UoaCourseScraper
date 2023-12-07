import json

courses, faculties, info = [], [], []

with open('courses.json', 'r') as file1:
    courses = json.loads(file1.read())

with open('faculties.json', 'r') as file2:
    faculties = json.loads(file2.read())

def get_faculty_list(course_code):
    return [faculty['Faculty'] for faculty in faculties if course_code.startswith(f"{faculty['Code']} ")]

for course in courses:
    faculty_list = get_faculty_list(course['Code'])
    course['Faculties'] = faculty_list

    info.append(course)

with open('info.json', 'w') as file:
    json.dump(info, file, indent=4)
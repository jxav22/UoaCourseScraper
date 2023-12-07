import requests
import json
from bs4 import BeautifulSoup

# Terminology
# high level course - without code e.g COURSE
# low level course - with code e.g COURSE 123

# Gets faculty data for each high level course
def extract_faculty_info():
    main_link = 'https://www.calendar.auckland.ac.nz/en/courses/subject-index.html'
    response = requests.get(main_link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all table rows except the first two (header row, blank code)
        rows = soup.find_all('tr')[3:]

        faculty_info = []

        # Extracting data from each row
        for row in rows:
            columns = row.find_all('td')
            course_code = columns[0].text.strip()
            title = columns[1].text.strip()
            faculty = columns[2].text.strip()

            # Create a dictionary for each high levelcourse
            course = {
                "Code": course_code,
                "Title": title,
                "Faculty": faculty
            }
            
            faculty_info.append(course)

        return faculty_info
    else:
        print('Failed to retrieve the webpage')

# Gets the links for each high level course
def extract_course_links():
    main_link = 'https://www.calendar.auckland.ac.nz/en/courses/subject-index.html'
    response = requests.get(main_link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')[2:]

        links = []
        for row in rows:
            columns = row.find_all('td')
            title_elem = columns[1].find('a')
            title_link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else None

            if title_elem != None:
                links.append(title_link)
        
        return links
    else:
        print('Failed to retrieve the webpage')

# Gets course data for each low level course
def extract_course_info():
    links = extract_course_links()
    courses = []

    for link in links:
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Loop through each course section
            for course_section in soup.find_all(class_='coursePaper'):
                # Extract course code and title info
                code = course_section.find(class_='courseA').text.strip()
                title = course_section.find(class_='title').text.strip()

                # Extract stage info
                stage_element = course_section.find_previous(class_='stage')
                stage = stage_element.text.strip() if stage_element else ""

                course_info = {
                    'Code': code,
                    'Title': title,
                    'Stage': stage
                }

                courses.append(course_info)
        else:
            print('Failed to retrieve the webpage')
    
    return courses

# For updating files

def update_faculties():
    faculties = extract_faculty_info()
    with open('faculties.json', 'w') as file:
        json.dump(faculties, file, indent=4)

def update_courses():
    courses = extract_course_info()
    with open('courses.json', 'w') as file:
        json.dump(courses, file, indent=4)

# Call functions here

update_faculties()
# update_courses()
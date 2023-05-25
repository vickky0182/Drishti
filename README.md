# Drishti

## Problem Statement:

To develop an automated classroom attendance system and a mobile application for attendance management

## Objectives:

1. Develop a face recognition algorithm.

2. Setup system of cameras in classrooms to detect students, entering and leaving the classroom.

3. Re-enforcing the proposed method with further functionality.

4. Implement distance algorithm and other methods to avoid proxies.

5. Building an application with separate interfaces for students and faculties to track attendance.

# Steps

1. Clone the repository.
2. Install the required libraries from requiremnets.txt
3. Add a single clear image of the requires people's faces to a folder named "images". (Populate the database)
   ##### Note: Name of the image files should be exactly same as the ones mentioned in the google spreadsheet
4. Add the json file to connect to your google spreadsheet to a folder named "important". Basic template has been provided
5. On line number 194,195 in attendance_copy.py change the port numbers according to your syste.
6. Run simple_facerec.py once and then run attendance_copy.py

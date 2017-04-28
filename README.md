# TritonLink for Python

## Overview
This is a python library that simulates users' interaction with UCSD TritonLink **Student SSO** login system.

### WARNING: THIS SCRIPT IS JUST AN IMPLEMENTATION OF IDEAS!!!
Last tested: 2017 April

## Dependency
BeautifulSoup, Requests, re

## Documentation
### Create an instance
Create a instance for TritonLink session

```python
tl = TritonLink(user_name, user_password)
```
user_name and user_password should be the Active Directory (AD) user name/password that is able to use Student SSO to login TritonLink

###Login into TritonLink
Simulate user's action and login with Student SSO

```python
tl.login()
```

###Retrieve Student Information
Retrieve student info based on the current TritonLink login

```python
student_info = tl.get_student_info()
```

`student_info` will be a key-value pair dictionary.

Keys         | Values
------------ | -------------
name | name of the student
college | residential college
major | current major in UCSD
years | current year in UCSD
account_balance | current account balance in TritonLink
holds | number of holds in TritonLink 


###Retrieve Enrollment Information
Retrieve student enrollment information based on the current TritonLink login

####Retrieve Enrollment/Quarter Information

```python
enrolled_courses = tl.get_courses_enrolled()
```

`enrolled_courses` is a key-value pair dictionary

For example:

```python
for quarter, courses in enrolled_courses.iteritems():
	print "You've selected the following courses for "+quarter+" :";
	for course in courses:
		#whatever
```

Keys         | Values
------------ | -------------
(name of the quarter, e.g. "Spring Qtr 2015") | a ***list*** of key-value pairs for courses (described below) 

####Retrieve Course List

`courses = enrolled_courses[quarter_name]` will save the ***list*** of courses into `courses`

`courses[x]` will be a key-value pair dictionary described as following

Keys         | Values
------------ | -------------
department | department of the course (e.g. "CSE")
section | section number of the course (e.g. "87")
title | title of the course (e.g. "Introduction to Robotics")
units | number of units (e.g. "1.00")
grading | method of grading (e.g. "Letter" or "P/NP")
instructor | name of the instructor (Last Name, First Name)
meeting | a list of meetings relating to the course (including Lecture/Discussion/Midterm/Final)

####Retrieve Meetings for Course

`meetings = courses[x]['meeting']`will save the ***list*** of meetings into `meetings`

`meetings[x]` will be a key-value pair dictionary

Keys         | Values
------------ | -------------
id | id number for the meeting (only valid for a Lecture-type meeting)
type | type of the meeting ( "Discussion"/"Lecture"/"Midterm"/"Final")
section | section number (e.g. "A00") of the meeting
time | meeting time of the meeting (e.g. "7:00p - 7:50p")
days | days on which the meeting will hold (e.g. "MTuWThF")
building | building in which the meeting will hold (e.g. "CENTR")
room | room in which the meeting will hold (e.g. "119")


###See python script demo.py for more info.


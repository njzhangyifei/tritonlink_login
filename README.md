# TritonLink for Python

##Overview
This is a python library that simulates users' interaction with UCSD TritonLink Student SSO login system.

##Dependency
BeautifulSoup, Requests, re

##Documentation
###Create an instance
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

```python
enrolled_courses = tl.get_courses_enrolled()
```

`enrolled_courses` will be a key-value pair dictionary, 

Keys         | Values
------------ | -------------
department | department of the course (e.g. "CSE")
section | section number of the course (e.g. "87")
title | title of the course (e.g. "Introduction to Robotics")
units | number of units (e.g. "1.00")
grading | method of grading (e.g. "Letter" or "P/NP")
instructor | name of the instructor (Last Name, First Name)

###See python script demo.py for more info.

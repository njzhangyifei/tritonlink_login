from tl_login_requests import *
import getpass

user_name = raw_input('Enter your id: ')
user_password= getpass.getpass('Enter your password: ')
tl = TritonLink(user_name,user_password);
tl.login();
session = tl.requests_session;
mytl = tl.mytritonlink;
info = tl.get_student_info();
print "Welcome back, "+info['name'];
print "You are a "+info['years']+" year "+info['major']+" student in "+info['college'];
print "You have "+info['holds']+" holds. Your account balance is "+info['account_balance'];
enrolled_courses = tl.get_courses_enrolled();
print "You've selected the following courses:";
for course in enrolled_courses:
    print course['department'] +" "+course['section']+"\t: "+course['title']+"\tInstructor: "+course['instructor'];


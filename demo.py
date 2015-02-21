from tl_login_requests import *
import getpass

user_name = raw_input('Enter your id: ')
user_password= getpass.getpass('Enter your password: ')
tl = TritonLink(user_name,user_password);
tl.login();
session = tl.requests_session;
mytl = tl.mytritonlink;
info = tl.get_student_info();
print "Welcome back, "+info['name']+"\n";
print "You are a "+info['years']+" year "+info['major']+" student in "+info['college'];
print "You have "+info['holds']+" holds. Your account balance is "+info['account_balance'];

print;
enrolled_courses = tl.get_courses_enrolled();
for quarter, courses in enrolled_courses.iteritems():
    print "You've selected the following courses for "+quarter+" :";
    print "----------------------------------------------------------------";
    for course in courses:
        print course['department'] +" "+course['section']+": "+course['title']+"   Instructor: "+course['instructor'];
        meetings = course['meeting'];
        for meeting in meetings:
            print meeting['type']+" "+meeting['section']+" at "+meeting['building']+meeting['room']+" on "+meeting['days']+" during "+meeting['time'];
        print;
    print;


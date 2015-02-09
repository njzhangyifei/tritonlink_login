import requests
import re
import getpass
from HTMLParser import HTMLParser;
from bs4 import BeautifulSoup

#UCSD SSO SAML Response Parser class
class UCSD_SSO_SAML_Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self);
        self.SAMLResponse = '';
        self.TARGET = '';
    def handle_starttag(self,tag,attrs):
        self.SAMLCatched = False;
        self.TARGETCatched = False;
        for attr in attrs:
            if attr[0] == 'name':
                if attr[1] == 'SAMLResponse':
                    self.SAMLCatched = True;
            if self.SAMLCatched:
                if attr[0] == 'value':
                    self.SAMLResponse = attr[1];
        for attr in attrs:
            if attr[0] == 'name':
                if attr[1] == 'TARGET':
                    self.TARGETCatched = True;
            if self.TARGETCatched:
                if attr[0] == 'value':
                    self.TARGET = attr[1];
    def close(self):
        HTMLParser.close(self);

""" For simulating user login in UCSD Shibboleth SSO """
class TritonLink:
    tritonlink_url = "http://mytritonlink.ucsd.edu";
    ucsd_sso_saml_url = "https://act.ucsd.edu/Shibboleth.sso/SAML/POST";
    def __init__(self,user_id,user_pd):
        self._requests_session = requests.Session();
        self._loggedin = False;
        self._tritonlink_username = user_id;
        self._tritonlink_password = user_pd;
        self._mytritonlink = None;
    
    @property
    def requests_session(self):
        return self._requests_session;

    @property
    def mytritonlink(self):
        return self._mytritonlink;

    """ 
    login(self)
    Return mytritonlink page response 
    """
    def login(self):
        if (self._loggedin):
            return True;
        response = self._requests_session.get(self.tritonlink_url);
        student_sso_param = {
                'initAuthMethod':'urn:mace:ucsd.edu:sso:studentsso',
                'urn:mace:ucsd.edu:sso:username':self._tritonlink_username,
                'urn:mace:ucsd.edu:sso:password':self._tritonlink_password,
                'submit' : 'submit',
                'urn:mace:ucsd.edu:sso:authmethod':
                    'urn:mace:ucsd.edu:sso:studentsso'
                }
        response = self._requests_session.post(response.url,student_sso_param);
        parser = UCSD_SSO_SAML_Parser();
        parser.feed(response.text);
        SAML_response = parser.unescape(parser.SAMLResponse);
        SAML_target = parser.unescape(parser.TARGET);
        SAML_param = {
                'SAMLResponse' : SAML_response,
                'TARGET' : SAML_target
                }
        response = self._requests_session.post(
                self.ucsd_sso_saml_url,SAML_param,allow_redirects = False);
        response = self._requests_session.get(SAML_target);
        # ::TODO need to check the validity of login
        self._loggedin = True;
        self._mytritonlink = response.text;
        return True;

    def get_student_info(self):
        if (not(self._loggedin)):
            return False;
        soup = BeautifulSoup(self._mytritonlink);
        sidebar = soup.find('div',id='my_tritonlink_sidebar')
        name = sidebar.h2.string.strip()
        college = sidebar.find_all('p')[0].a.string.strip();
        major = sidebar.find_all('p')[1].a.string.strip();
        years = sidebar.find_all('p')[2].b.string.strip()
        account_balance = soup.find(
                'div',id='account_balance'
                ).find(
                        'div','cs_box_amount'
                        ).strong.string.strip();
        holds = soup.find(
                'div',id='holds'
                ).find(
                        'div','cs_box_content'
                        ).p.string.strip();
        holds = re.findall(r'\b\d+\b',holds)[0];
        student_info = {
                'name' : name,
                'college' : college,
                'major' : major,
                'years' : years,
                'account_balance':account_balance,
                'holds':holds,
                };
        return student_info;

    def get_courses_enrolled(self):
        enrolled_courses_url = "https://act.ucsd.edu/studentEnrolledClasses/enrolledclasses"
        enrolled_classes_html = self._requests_session.get(enrolled_courses_url);
        soup = BeautifulSoup(enrolled_classes_html.text);
        courses = [];
        courses_html = soup.find_all('td',{'bgcolor':'#c0c0c0'});
        for course_html in courses_html:
            course_department = course_html.find_next('tr').find_all('td')[1].text;
            course_section = course_html.find_next('tr').find_all('td')[2].text;
            course_title = course_html.find_next('tr').find_all('td')[3].text;
            course_units = course_html.find_next('tr').find_all('td')[4].text;
            course_grading = course_html.find_next('tr').find_all('td')[5].font.text;
            course_instructor = course_html.find_next('tr').find_all('td')[6].text;
            course = {
                    'department' : course_department,
                    'section' : course_section,
                    'title' : course_title,
                    'units' : course_units,
                    'grading' : course_grading,
                    'instructor' : course_instructor,
                    };
            courses.append(course);
        return courses;
    

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
#print response.headers;
enrolled_courses = tl.get_courses_enrolled();
print "You've selected the following courses:";
for course in enrolled_courses:
    print course['department'] +" "+course['section']+" : "+course['title']+"\tInstructor: "+course['instructor'];


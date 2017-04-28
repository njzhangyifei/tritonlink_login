import requests
import re
from HTMLParser import HTMLParser;
from bs4 import BeautifulSoup

#UCSD SSO SAML Response Parser class
class UCSD_SSO_SAML_Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self);
        self.SAMLResponse = '';
        self.RelayState = '';
    def handle_starttag(self,tag,attrs):
        self.SAMLCatched = False;
        self.RelayStateCatched = False;
        for attr in attrs:
            if attr[0] == 'name':
                if attr[1] == 'RelayState':
                    self.RelayStateCatched = True;
            if self.RelayStateCatched:
                if attr[0] == 'value':
                    self.RelayState = attr[1];
        for attr in attrs:
            if attr[0] == 'name':
                if attr[1] == 'SAMLResponse':
                    self.SAMLCatched = True;
            if self.SAMLCatched:
                if attr[0] == 'value':
                    self.SAMLResponse = attr[1];
    def close(self):
        HTMLParser.close(self);

""" For simulating user login in UCSD Shibboleth SSO """
class TritonLink:
    tritonlink_url = "http://mytritonlink.ucsd.edu";
    ucsd_sso_saml_url = "https://act.ucsd.edu/Shibboleth.sso/SAML/POST";
    ucsd_sso_saml2_url = "https://act.ucsd.edu/Shibboleth.sso/SAML2/POST";
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
        RelayState = parser.unescape(parser.RelayState);
        SAML_param = {
                'RelayState' : RelayState,
                'SAMLResponse' : SAML_response,
                }
        #update to SAML2, SPRING 2015
        response = self._requests_session.post(
                self.ucsd_sso_saml2_url,SAML_param,allow_redirects = False);
        response = self._requests_session.get(RelayState);
        # ::TODO need to check the validity of login
        self._loggedin = True;
        self._mytritonlink = response.text;
        return True;

    def get_student_info(self):
        if (not(self._loggedin)):
            return False;
        soup = BeautifulSoup(self._mytritonlink, 'lxml');
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
        soup = BeautifulSoup(enrolled_classes_html.text, 'lxml');
        quarters = {};
        courses_html = soup.find_all('td',{'bgcolor':'#c0c0c0'});
        #find all quarters first
        quarters_html = courses_html[len(courses_html)-1].find_all_previous('td',{'width':'34%','class':'boldheadertxt_noborder'})
        for quarter_html in quarters_html:
            quarter_name = quarter_html.text.strip();
            quarters[quarter_name] = [];

        courses = [];
        for course_html in courses_html:
            course_quarter = course_html.find_previous('td',{'width':'34%','class':'boldheadertxt_noborder'}).text.strip();
            
            course_row = course_html.find_next('tr')
    
            course_department = course_row.find_all('td')[1].text;
            course_section = course_row.find_all('td')[2].text;
            course_title = course_row.find_all('td')[3].text;
            course_units = course_row.find_all('td')[4].text;
            course_grading = course_row.find_all('td')[5].font.text;
            course_instructor = course_row.find_all('td')[6].text;
            
            meetings_html = course_row.find_all_next('tr',class_=re.compile("white_background"))

            meetings = []
            for meeting_html in meetings_html:
                terminating = False;
                attrs_next = meeting_html.find_next('tr').attrs
                if ((not('class' in attrs_next)) and (attrs_next)):
                    #terminating, but we still want this meeting row
                    terminating = True;

                meeting_row = meeting_html.find_all_next('td')
                meeting_id = meeting_row[0].text.strip();              
                meeting_type = meeting_row[1].text.strip();              
                meeting_section = meeting_row[2].text.strip();              
                meeting_time = meeting_row[3].text.strip();              
                meeting_days = meeting_row[4].text.strip();              
                meeting_building = meeting_row[5].text.strip();
                meeting_room = meeting_row[6].text.strip();

                meeting = {
                        'id' : meeting_id,
                        'type' : meeting_type,
                        'section' : meeting_section,
                        'time' : meeting_time,
                        'days' : meeting_days,
                        'building' : meeting_building,
                        'room' : meeting_room
                        };
                meetings.append(meeting);
                if terminating:
                    break;

            course = {
                    'department' : course_department,
                    'section' : course_section,
                    'title' : course_title,
                    'units' : course_units,
                    'grading' : course_grading,
                    'instructor' : course_instructor,
                    'meeting' : meetings
                    };
            courses = quarters[course_quarter]
            courses.append(course);
            quarters[course_quarter] = courses;
        return quarters;

    def get_courses_schedule(self):
        return 0;

####################################################
# Kidney cross-exchange app
# Medical Informatics Uva AMC
# MAM04 - Biomedical Information Systems Engineering
#
# Attila Csala - attilacsala@gmail.com
# December 2014, Amsterdam
#
# This code is mainly based on Google App Engine tutorial: https://cloud.google.com/appengine/docs/python/gettingstartedpython27/introduction


# import dependencies
import os
import cgi
import urllib
import webapp2
import jinja2

# get google authentication
from google.appengine.api import users

# import_ndb
from google.appengine.ext import ndb

# imort_google_mails_api
from google.appengine.api import mail

# import data model
from data_model import *

# import matching_algorithm
from matching_algorithm import *
import matching_algorithm

# Set up environment for template, based on Google App Engine tutorial 
JINJA_ENVIRONMENT = jinja2.Environment(
		# pull out the templates from a subfolder
		loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'htmls')),
		extensions = ['jinja2.ext.autoescape'],
		autoescape = True
		)

# [START login page, based on Google App Engine tutorial]
class LoginPageHandler(webapp2.RequestHandler):
    def get(self):
    			# Checks for active Google account session
        user = users.get_current_user()
    
    			# Redirect user after logging in
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            
            # If user already submitted details, redirect to the main page
            if Patients.query(Patients.patient == user).fetch(10):
            		self.redirect('/main')
            		
            # If user hasn't filled in details yet, redirect to details registration'
            else:
            		self.redirect('/settings')
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
				
        template_values = {
        		'current_user': users.get_current_user(),
        		's_current_user': str(users.get_current_user()),
        		'url': url,
        		'url_linktext': url_linktext
        }
        
        template = JINJA_ENVIRONMENT.get_template("login.html")
        self.response.write(template.render(template_values))
# [END login page]

# [START main_page, based on Google App Engine tutorial]
class MainPageHandler(webapp2.RequestHandler):
    def get(self):

        # [START query]
        patients_query = Patients.query().order(-Patients.date)
        patients = patients_query.fetch(10)
        
        # [END query]

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            self.redirect('/')
            
#!!##        # Count patients per hospitals
        amc_patients = Patients.query(Patients.transplant_center == "Academisch Medisch Centrum Amsterdam").fetch()
        gumc_patients = Patients.query(Patients.transplant_center == "Universitair Medisch Centrum Groningen").fetch()
        lumc_patients = Patients.query(Patients.transplant_center == "Leids Universitair Medisch Centrum").fetch()
        azm_patients = Patients.query(Patients.transplant_center == "Academisch Ziekenhuis Maastricht").fetch()
        rn_patients = Patients.query(Patients.transplant_center == "Radboudumc, Nijmegen").fetch()
        emcr_patients = Patients.query(Patients.transplant_center == "Erasmus MC, Rotterdam").fetch()
        umc_patients = Patients.query(Patients.transplant_center == "Universitair Medisch Centrum Utrecht").fetch()

        template_values = {
        		'current_user': users.get_current_user(),
        		's_current_user': str(users.get_current_user()),
        		'patients': patients,
        		'url': url,
        		'url_linktext': url_linktext,
        		'amc_patients': len(amc_patients),
        		'gumc_patients': len(gumc_patients),
        		'lumc_patients': len(lumc_patients),
        		'azm_patients': len(azm_patients),
        		'rn_patients': len(rn_patients),
        		'emcr_patients': len(emcr_patients),
        		'umc_patients': len(umc_patients),
        }
        
        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render(template_values))
# [END main_page]

# [START data submittion - Complete, based on Google App Engine tutorial]
class CompleteHandler(webapp2.RequestHandler):
    def post(self):

        patients = Patients()

        patients.patient = users.get_current_user()
        
        patients.transplant_center = self.request.get('center')
        patients.blood_type_needed = self.request.get('blood_type_needed')
        patients.blood_type_offered = self.request.get('blood_type_offered')
        patients.email = users.get_current_user().email()
        
        patients.put()

        self.redirect('/main')
    
    # redirect hackers 
    def get(self):
    			self.redirect('/main')
# [END data submittion - Complete]

# [START data registration - Register, based on Google App Engine tutorial]
class RegisterHandler(webapp2.RequestHandler):
    def get(self):
    
				if users.get_current_user():
				        url = users.create_logout_url(self.request.uri)
				        url_linktext = 'Logout'
				else:
				        url = users.create_login_url(self.request.uri)
				        url_linktext = 'Login'
				        self.redirect('/')

				template_values = {
				    		'current_user': users.get_current_user(),
				    		's_current_user': str(users.get_current_user()),
				    		'url': url,
				    		'url_linktext': url_linktext,
				}
				    
				template = JINJA_ENVIRONMENT.get_template("register.html")
				self.response.write(template.render(template_values))
# [END data registration - Register]


# [START email sending - EmailTestHandler, based on Google App Engine tutorial]
class EmailTestHandler(webapp2.RequestHandler):
		def post(self):
				user = users.get_current_user()
				
				#handle intruders
				if user is None:
						login_url = users.create_login_url(self.request.path)
						self.redirect(login_url)
						return
        
        #composing first message for the match
				to_addr = self.request.get("friend_email")
				from_addr = self.request.get("requester_email")
				
				if not mail.is_email_valid(to_addr):
            # Return an error message
						pass
				
				kidney_mail_address = "info@kidnify.appspotmail.com"
				
				message = mail.EmailMessage()
				message.sender = kidney_mail_address
				message.to = to_addr
				message.body ="""
Hi there,
				
We have found a match for you. Please get in touch with your potential match at:

%s
				
Thanks,

The kidnify team
        """ % (from_addr)

				#send out first message
				message.send()
				
				#compose second, confirmation message for the requester
				second_message = mail.EmailMessage()
				
				message.sender = kidney_mail_address
				message.to = from_addr
				message.body ="""
Hi there,
				
We have emailed your match (for privacy reasons, you will not receive their email address).

Enjoy your new kindey!
				
Thanks,

The kidnify team
        """
        
        #send out second message
				message.send()
				
				
				self.redirect('/')
# [END email sending - EmailTestHandler]

# [START MatchTestHandler]
class MatchHandler(webapp2.RequestHandler):
		def post(self):
				
				user = Patients.query(Patients.patient == users.get_current_user()).fetch(1)
				
				blood_type_needed = user[0].blood_type_needed
				blood_type_offered = user[0].blood_type_offered		
				
				#match_algorithm is imported from matching_algorithm.py
				matching_patients = match_algorithm(blood_type_needed, blood_type_offered)
				
				#matching_patients = pre_matching_patients.filter(Patients.blood_type_needed == blood_type_offered).fetch(10)
				
				template = JINJA_ENVIRONMENT.get_template("matching.html")

				#if there is a matching person, display different text parts on the page
				if matching_patients:
						#self.response.write(matching_patients)
						display_text = "There is a match! Please get in touch with the other patient for futher information"
						dinamic_part = """
						<style> body {
						background: url(pics/match_bg.jpg); 
						background-size: 100%%; 
						background-repeat: no-repeat;}
						</style>
						<form method='POST' action='/emailTest'>
						<input type='hidden' name='friend_email' value= %s >
						<input type='hidden' name='requester_email' value= %s >
						<input type='submit' value="Send email">
						</form>
						
						""" % (matching_patients[0].email, user[0].email)
				
				else:
						display_text = "We cannot find any matches for you yet. We will keep you posted by email as soon as there is a potential match for you."
						dinamic_part = ""
	
				template_values = {
				    		'display_text': display_text,
				    		's_current_user': str(users.get_current_user()),
				    		'dinamic_part': dinamic_part
				}
						
				self.response.write(template.render(template_values))
# [END MatchTestHandler]

# [START MatchEmailRequestHandler]
class MatchEmailRequestHandler(webapp2.RequestHandler):
		def get(self):
				
				user = Patients.query(Patients.patient == users.get_current_user()).fetch(1)
				
				blood_type_needed = user[0].blood_type_needed
				blood_type_offered = user[0].blood_type_offered

				matching_patients = Patients.query(Patients.blood_type_offered == blood_type_needed, Patients.blood_type_needed == blood_type_offered).fetch(10)
				#matching_patients = pre_matching_patients.filter(Patients.blood_type_needed == blood_type_offered).fetch(10)
				
				#voorbeeld = Patients.GqlQuery("SELECT patient FROM Patients")
				
				template = JINJA_ENVIRONMENT.get_template("matching.html")

				#if there is a matching person, display different text parts on the page
				if matching_patients:
						#self.response.write(matching_patients)
						display_text = "There is a match! Please get in touch with the other patient for futher information"
						dinamic_part = """
						<form method='POST' action='/emailTest'>
						<input type='hidden' name='friend_email' value= %s >
						<input type='hidden' name='requester_email' value= %s >
						<input type='submit' value="Send email">
						</form>
						""" % (matching_patients[0].email, user[0].email)
						
						
						
				else:
						display_text = "We cannot find any matches for you yet. We will keep you posted by email as soon as there is a potential match for you."
						dinamic_part = ""
	
				
				template_values = {
				    		'display_text': display_text,
				    		's_current_user': str(users.get_current_user()),
				    		'dinamic_part': dinamic_part
				}
						
				self.response.write(template.render(template_values))
# [END MatchEmailRequestHandler]

# Handle routing
application = webapp2.WSGIApplication([
		('/', LoginPageHandler),
    ('/main', MainPageHandler),
    ('/sign', CompleteHandler),
    ('/settings', RegisterHandler),
    ('/emailTest', EmailTestHandler),
    ('/matching', MatchHandler)
], debug=True)

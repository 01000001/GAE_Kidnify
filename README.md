GAE_Kidnify
===========

Online platform for a cross-kidney exchange program in the Netherlands

Instructions for installing and running the software:
###############

The application is available online at:
 http://kidnify.appspot.com/

If you want to run it locally:

Download the Download the Google App Engine SDK from:
https://cloud.google.com/appengine/downloads

Open the SDK, go to File -> Add existing application, add the the root directory of kidney_app. Hit Run, hit Browse, or go to localhost (you can find the Port which you opened for the application in the SDK).


Software requirements for the application
##############

List of features of Kidnify:
supports “cross-over matching” kidney donation between patients through data maintained from patients, taken their blood type into consideration
enables users to log in to the application via their google account
enables users to input information about the organ they are looking for and the organ they have to offer for the cross-over matching, regarding blood type
enables users to request a matching procedure
users are notified through email upon potential matches

Services used:
Google App Engine
Google Datastore API
Google Accounts
Google Mail API
Google Maps API

Design and structure
##############
appkidney.py is the back end code, written in python
app.yaml is needed for configuration of Google App Enigne
index.yaml is automatically generated after indexing the database

GAE_KidnyApp
===========

Online platform for a cross-kidney exchange program in the Netherlands

Software requirements for the application
##############

List of features of KidnyApp:
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

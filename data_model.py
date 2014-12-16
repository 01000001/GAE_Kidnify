####################################################
# Kidney cross-exchange app data model for database
# Medical Informatics Uva AMC
# MAM04 - Biomedical Information Systems Engineering
#
# Attila Csala - attilacsala@gmail.com
# December 2014, Amsterdam

from google.appengine.ext import ndb

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

# [START greeting]
class Patients(ndb.Model):
    """Models an individual Users entry."""
    patient = ndb.UserProperty(required = True)
    email = ndb.StringProperty(required = True)
    
    #Source: http://www.transplantatiestichting.nl/medische-procedure/toewijzing/transplantatiecentra
    transplant_center = ndb.StringProperty(choices = ['Academisch Medisch Centrum Amsterdam', 'Universitair Medisch Centrum Groningen', 'Leids Universitair Medisch Centrum', 'Academisch Ziekenhuis Maastricht', 'Radboudumc, Nijmegen', 'Erasmus MC, Rotterdam', 'Universitair Medisch Centrum Utrecht'], required = True)
    
    blood_type_needed = ndb.StringProperty(required = True)
    blood_type_offered = ndb.StringProperty(required = True)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

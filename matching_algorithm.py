####################################################
# Kidney cross-exchange app matching algorithm
# Medical Informatics Uva AMC
# MAM04 - Biomedical Information Systems Engineering
#
# Attila Csala - attilacsala@gmail.com
# December 2014, Amsterdam
#
# Algorithm for blood matching, due to the relatice complexity of blood type matching and the small number of cases, I found hardcoding the rules the most efficient way for implementation. It is somewhat unelegant but I expect no new blood types to be discovered nor new rules for blood type matching in the near future. 
#Source for matching rules: http://www.redcrossblood.org/learn-about-blood/blood-types

# import_ndb
from google.appengine.ext import ndb

# import data model
from data_model import *

def match_algorithm(blood_type_needed, blood_type_offered):

### Blood type needed A	
				
				#Recipients with blood type A... can receive a kidney from blood types A and O
				#Donors with blood type B... can donate to recipients with blood types B and AB
				if blood_type_needed == "A" and blood_type_offered == "B":
						matching_patients = Patients.query(Patients.blood_type_offered == "A" or Patients.blood_type_offered == "O", Patients.blood_type_needed == "B" or Patients.blood_type_needed == "AB").fetch(10)

				#Recipients with blood type A... can receive a kidney from blood types A and O
				#Donors with blood type AB... can donate to recipients with blood type AB only				
				elif blood_type_needed == "A" and blood_type_offered == "AB":
						matching_patients = Patients.query(Patients.blood_type_offered == "A" or Patients.blood_type_offered == "O", Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type A... can receive a kidney from blood types A and O
				#Donors with blood type O... can donate to recipients with blood types A, B, AB and O		
				elif blood_type_needed == "A" and blood_type_offered == "O":
						matching_patients = Patients.query(Patients.blood_type_offered == "A" or Patients.blood_type_offered == "O").fetch(10)
				
#### Blood type needed B				
				
				#Recipients with blood type B... can receive a kidney from blood types B and O
				#Donors with blood type A... can donate to recipients with blood types A and AB
				elif blood_type_needed == "B" and blood_type_offered == "A":
						matching_patients = Patients.query(Patients.blood_type_offered == "B" or Patients.blood_type_offered == "O", Patients.blood_type_needed == "A" or Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type B... can receive a kidney from blood types B and O
				#Donors with blood type AB... can donate to recipients with blood type AB only
				elif blood_type_needed == "B" and blood_type_offered == "AB":
						matching_patients = Patients.query(Patients.blood_type_offered == "B" or Patients.blood_type_offered == "O", Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type B... can receive a kidney from blood types B and O
				#Donors with blood type O... can donate to recipients with blood types A, B, AB and O		
				elif blood_type_needed == "B" and blood_type_offered == "O":
						matching_patients = Patients.query(Patients.blood_type_offered == "B" or Patients.blood_type_offered == "O").fetch(10)
				
#### Blood type needed AB
				
				#Recipients with blood type AB... can receive a kidney from blood types A, B, AB and O
				#Donors with blood type A... can donate to recipients with blood types A and AB
				elif blood_type_needed == "AB" and blood_type_offered == "A":
						matching_patients = Patients.query(Patients.blood_type_needed == "A" or Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type AB... can receive a kidney from blood types A, B, AB and O
				#Donors with blood type B... can donate to recipients with blood types B and AB
				elif blood_type_needed == "AB" and blood_type_offered == "B":
						matching_patients = Patients.query(Patients.blood_type_needed == "B" or Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type AB... can receive a kidney from blood types A, B, AB and O
				#Donors with blood type O... can donate to recipients with blood types A, B, AB and O	
				elif blood_type_needed == "AB" and blood_type_offered == "O":
						matching_patients = Patients.query().fetch(10)
				
#### Blood type needed O

				#Recipients with blood type O... can receive a kidney from blood type O only
				#Donors with blood type A... can donate to recipients with blood types A and AB
				elif blood_type_needed == "O" and blood_type_offered == "A":
						matching_patients = Patients.query(Patients.blood_type_offered == "O", Patients.blood_type_needed == "A" or Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type O... can receive a kidney from blood type O only
				#Donors with blood type B... can donate to recipients with blood types B and AB
				elif blood_type_needed == "O" and blood_type_offered == "B":
						matching_patients = Patients.query(Patients.blood_type_offered == "O", Patients.blood_type_needed == "B" or Patients.blood_type_needed == "AB").fetch(10)
						
				#Recipients with blood type O... can receive a kidney from blood type O only
				#Donors with blood type AB... can donate to recipients with blood type AB only
				elif blood_type_needed == "O" and blood_type_offered == "AB":
						matching_patients = Patients.query(Patients.blood_type_offered == "O", Patients.blood_type_needed == "AB").fetch(10)
				
				#If patients register with the same blood type they offer that they need, send an email for the patient
				else:
						matching_patients = Patients.query(Patients.blood_type_offered == blood_type_offered , Patients.blood_type_needed == blood_type_offered).fetch(10)
						
				return matching_patients

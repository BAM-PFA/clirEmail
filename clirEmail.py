from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import ast
import csv
import os.path
import pickle

from letterContent import Email
from secrets.other import FOLDER_ID

# all modified from 
# https://github.com/googleapis/google-api-python-client

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
	'https://www.googleapis.com/auth/documents',
	'https://www.googleapis.com/auth/drive',
	"https://www.googleapis.com/auth/drive.file"
	]


def login():
	# Do some login stuff
	# Return live services for Docs and Drive APIs
	creds = None

	if os.path.exists('secrets/token.pickle'):
		with open('secrets/token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'secrets/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('secrets/token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	g_docs = build('docs', 'v1', credentials=creds)
	g_drive = build('drive','v3',credentials=creds)

	return g_docs, g_drive

def insert_paragraph(par,service,docID):
	print(par)
	insert = [
		 {
			'insertText': {
				'location': {
					'index': 1,
				},
				'text': par
			}
		}
	]

	service.documents().batchUpdate(
		documentId=docID,
		body={'requests':insert}
		).execute()

def parse_paragraphs(person):
	# take in a row from the CSV of people to contact
	# return a completed Email class
	name = person[0]
	deceased = person[1]
	titles = ast.literal_eval(person[2])
	recordIDs = person[4]
	dates = ast.literal_eval(person[5])

	completeEmail = Email(
		name=name,
		deceased=deceased,
		titles=titles,
		dates=dates,
		recordIDs=recordIDs
		)

	completeEmail.dear()
	completeEmail.is_deceased()
	completeEmail.test_dates()
	completeEmail.test_titles()
	completeEmail.paragraphs_to_list()
	completeEmail.reverse_paragraphs()

	return completeEmail


def main():
	g_docs, g_drive = login()

	with open('contacts.csv','r') as f:
		reader = csv.reader(f)
		for person in reader:
			# print(person)
			completeEmail = parse_paragraphs(person)

			gDocTitle = 'Email to {}'.format(person[0])
			_body = {'title':gDocTitle}

			new_doc = g_docs.documents().create(body=_body).execute()
			docID = new_doc.get("documentId")
			# parents = g_drive.files().get(fileId=_id).execute()
			# print(parents)
			# parent = parents.get('parents')[0]
			# print(parent)
			# print(_id)

			for paragraph in completeEmail.reversedParagraphs:
				# print(par)
				if paragraph != None:
					insert_paragraph(paragraph, g_docs, docID)

			# MOVE THE COMPLETE DOCUMENT TO THE PROJECT FOLDER
			move = g_drive.files().update(
				fileId=docID,
				addParents=FOLDER_ID,
				fields='id, parents'
				).execute()
			print(move)

if __name__ == '__main__':
	main()
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from secrets.other import FOLDER_ID

# https://github.com/googleapis/google-api-python-client

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/drive']

# The ID of a sample document.
DOCUMENT_ID = None

# FOLDER_ID = 

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    # Retrieve the documents contents from the Docs service.
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()
    # files  = g_drive.files().list(q="'{}' in parents".format(FOLDER_ID)).execute()

    # print('The title of the document is: {}'.format(document.get('title')))
    for i in range(0,5):
        title = 'My Document {}'.format(str(i))
        content = "Hello my name is {}. You killed my father, prepare to die.".format(str(i))
        print(content)
        endIndex = len(content)-1
        print(endIndex)
        _body = {
            "title": title,
            "body": 
                {
                    "content": [
                        # {
                        #     "startIndex": 0, 
                        #     "endIndex": 1, 
                        #     "sectionBreak": {
                        #         "sectionStyle": {
                        #             "columnSeparatorStyle": "NONE", 
                        #             "contentDirection": "LEFT_TO_RIGHT"
                        #         }
                        #     }
                        # },
                        {
                            "startIndex": 1,
                            "endIndex": endIndex,
                            "paragraph":
                                {
                                "elements":[
                                    {
                                    # "startIndex": 1,
                                    # "endIndex": endIndex,
                                    "textRun":
                                        {
                                        "content":"BOLLOCKS"
                                        }
                                    }
                                ]
                                }
                        }
                    ]
                }
            }
        # print(_body)

        new_doc = g_docs.documents().create(body=_body).execute()
        print(new_doc)
        _id = new_doc.get("documentId")
        # parents = g_drive.files().get(fileId=_id).execute()
        # print(parents)
        # parent = parents.get('parents')[0]
        # print(parent)
        # print(_id)
        move = g_drive.files().update(fileId=_id,addParents=FOLDER_ID,fields='id, parents').execute()
        print(move)


    # for _file in files.get('files',[]):
    #     print('found {}'.format(_file.get('name')))


if __name__ == '__main__':
    main()
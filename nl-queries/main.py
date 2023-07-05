import os
import io
import logging
import spacy
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(level=logging.INFO)

CLIENT_SECRET_FILE = '../credentials.json'
DOCUMENTS_FOLDER_ID = os.getenv('google_drive_id') or '1me6PtWgQpshDIUUHVjawD7zKTxcHPHKK'
SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate():
    return service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)


def download_documents(drive_service):
    documents = drive_service.files().list(q=f"'{DOCUMENTS_FOLDER_ID}' in parents and trashed=false",
                                           fields="files(name, id, mimeType)").execute().get('files', [])

    if not documents:
        return []

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    logging.info(f"Downloading {len(documents)} documents from Google Drive:")
    for document in documents:
        logging.info(f"Downloading {document['name']}...")

        if 'application/vnd.google-apps' in document['mimeType']:
            request = drive_service.files().export_media(fileId=document['id'], mimeType='application/pdf')
        else:
            request = drive_service.files().get_media(fileId=document['id'])

        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(f"Download {int(status.progress() * 100)}%")

        document_content = buffer.getvalue()
        with open(f"downloads/{document['name']}", 'wb') as f:
            f.write(document_content)

        logging.info(f"Downloaded {document['name']}.")


def process_query(documents, query):
    nlp = spacy.load("en_core_web_sm")

    if query == "How many nouns are in all the documents?":
        docs = [nlp(open(document, 'r').read()) for document in documents]
        nouns = [token.text for doc in docs for token in doc if token.pos_ == "NOUN"]
        return len(nouns)
    elif query == "How many verbs are in all he documents?":
        docs = [nlp(open(document, 'r').read()) for document in documents]
        verbs = [token.text for doc in docs for token in doc if token.pos_ == "VERB"]
        return len(verbs)
    else:
        return "I am not able to process your query"


def main(query):
    credentials = authenticate()
    drive_service = build('drive', 'v3', credentials=credentials)
    download_documents(drive_service)
    downloaded_documents = [f"downloads/{file}" for file in os.listdir('downloads')]
    result = process_query(downloaded_documents, query)
    logging.info(f"Query: {query}")
    logging.info(f"Result: {result}")


if __name__ == '__main__':
    query = "How many nouns are in all the documents?"
    main(query)
    query = "How many verbs are in all he documents?"
    main(query)

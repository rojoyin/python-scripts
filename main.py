import os
import io
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(level=logging.INFO)

CLIENT_SECRET_FILE = 'credentials.json'
DOCUMENTS_FOLDER_ID = '1me6PtWgQpshDIUUHVjawD7zKTxcHPHKK'
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


def main():
    credentials = authenticate()
    drive_service = build('drive', 'v3', credentials=credentials)
    download_documents(drive_service)


if __name__ == '__main__':
    main()

import argparse
import os.path
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class GDriveService:
    def __init__(self):
        self.CFILE = None

    def list_files(self):
        try:
            service = self.get_service()
    
            results = service.files().list(
                pageSize=20, fields="nextPageToken, files(id, name, createdTime)").execute()
            items = results.get('files', [])
    
            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1}) {2}'.format(item['name'], item['id'], item['createdTime']))
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    def delete(self, file_id):
        try:
            service = self.get_service()
            response = service.files().delete(fileId=file_id).execute()
            print(f"File {file_id} deleted")
        except HttpError as error:
            print(f'An error occurred: {error}')
            return
    
    def delete_by_name(self, file_name):
        try:
            service = self.get_service()
            results = service.files().list(
                q=f"name='{file_name}'",
                fields="files(id)").execute()
            items = results.get('files', [])
    
            if not items:
                print('No files found.')
                return
            for item in items:
                file_id = item['id']
                response = service.files().delete(fileId=file_id).execute()
                print(f"File {file_id} deleted")
        except HttpError as error:
            print(f'An error occurred: {error}')
            return

    def upload(self, file_path, target_id=None):
        # Define the file to upload
        file_name = os.path.basename(file_path)
        
        # Create a media object for the file
        media = MediaFileUpload(file_path, resumable=True)
        
        service = self.get_service()
        # Create a file on Google Drive
        # NB you have to share the folder (MIRBackups) with the service account email
        file_metadata = {
            'name': file_name,
        }
        if target_id:
            file_metadata['parents'] = [target_id]

        try:
            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None
    
        print(f'File {uploaded_file["name"]} uploaded to Google Drive with ID: {uploaded_file["id"]}')
    
    def get_service(self):
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        credentials_path = './creds.json'
        if self.CFILE:
            credentials_path = self.CFILE
        
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
        
        # Create a service object to interact with the Google Drive API
        service = build('drive', 'v3', credentials=creds)
        return service
    
    def set_creds(self, cfile):
        if os.path.isfile(cfile):
            self.CFILE=cfile
        else:
            print(f"Credentials file <{cfile}> not found using default")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI file management tool for Google Drive")
    parser.add_argument("-c", "--credentials", help="google oauth credentials file", metavar='creds')
    parser.add_argument("-d", "--delete", help="delete a file using the drive id", metavar='id')
    parser.add_argument("-dn", "--delete-name", help="delete files witha given name", metavar='name')
    parser.add_argument("-l", "--list", help="list files", action="store_true")
    parser.add_argument("-t", "--target", help="target drive id", metavar='tid')
    parser.add_argument("-u", "--upload", help="upload a file, optionally to a target drive id", metavar='path')
    args = parser.parse_args()

    gds = GDriveService()
    if args.credentials:
        gds.set_creds(args.credentials)

    if args.list:
        gds.list_files()
    elif args.delete:
        gds.delete(args.delete)
        gds.list_files()
    elif args.delete_name:
        gds.delete_by_name(args.delete_name)
        gds.list_files()
    elif args.upload:
        if args.target:
            gds.upload(args.upload, args.target)
        else:
            gds.upload(args.upload)
        gds.list_files()


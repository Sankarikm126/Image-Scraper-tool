import dropbox
import os

access_token = os.environ['DROPBOX_TOKEN']
dbx = dropbox.Dropbox(access_token)

def create_dropbox_folder(path):
    try:
        dbx.files_create_folder_v2(path)
    except dropbox.exceptions.ApiError:
        pass

def upload_to_dropbox(local_path, dropbox_path):
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

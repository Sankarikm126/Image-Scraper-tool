import dropbox
import json

with open('config.json') as f:
    config = json.load(f)

dbx = dropbox.Dropbox(config['access_token'])

def create_dropbox_folder(path):
    try:
        dbx.files_create_folder_v2(path)
    except dropbox.exceptions.ApiError:
        pass  # Folder may already exist

def upload_to_dropbox(local_path, dropbox_path):
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

# gdrive_manage
A command line file manager for Google Drive

Mainly intended for Google Service account where there is no UI.
It is also useful for automated file management, e.g. using cron.

## usage
gdrive_manage.py [-h] [-c creds] [-d id] [-dn name] [-l] [-t tid] [-u path]

CLI file management tool for Google Drive

options:
  -h, --help            show this help message and exit
  -c creds, --credentials creds
                        google oauth credentials file
  -d id, --delete id    delete a file using the drive id
  -dn name, --delete-name name
                        delete files witha given name
  -l, --list            list files
  -t tid, --target tid  target drive id
  -u path, --upload path
                        upload a file, optionally to a target drive id

## installation

You will need a Google Oauth2 credentials file to give you permission to 
access your drive. This might of help https://developers.google.com/workspace/guides/create-credentials

After that pip install -r requirements.txt 

An example docker file is also provided if that is instaled on a host machine then backups
could be run with a command like :
   docker run -v .:/bup gdrive_image:latest python3 gdrive_manage.py -u /bup/some_file

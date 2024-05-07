# Possible Errors

# There are numerous errors that can cause the updating process to fail.

# If the user’s PC is behind a proxy, the download of the manifest file or zip file may fail; to avoid this, whitelist the URLs where the manifest file and zip file are hosted.
# If the user’s PC lacks the necessary storage, the download of the zip file or extraction of the zip file may fail. To avoid this, instruct the user to keep enough disc space.
# If the updater does not have the required permissions, the killing process of application may fail. To avoid this make sure updater and application are running with the same user permissions.
# Copying the executables may fail if the application is not stopped properly.
# Because of the partial copy, restarting the application may fail; to avoid this, make the upgrading process atomic, as we discussed in the previous section.






import requests
import os
import shutil
import json
import datetime
import dateutil.parser
import wget
import subprocess
from zipfile import ZipFile


# username = 'aymanreda56'
# reponame= 'test'
# versionfile='ver.txt'
# url = f'http://github.com/{username}/{reponame}/archive/main.zip'





def move_files_inside_folder_to_outside(folder_path):
    # Get a list of all files inside the folder
    files = os.listdir(folder_path)
    
    # Move each file to the parent directory
    for file_name in files:
        # Construct the source and destination paths
        source = os.path.join(folder_path, file_name)
        destination = os.path.join(os.path.dirname(os.path.dirname(folder_path)), file_name)
        
        # Move the file
        shutil.move(source, destination)
    
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        print(e)





def check_For_Updates(username, reponame, versionfile):

    try:
        r = requests.get(f"https://api.github.com/repos/{username}/{reponame}/commits")

        entry_date = r.json()[0]['commit']['author']['date']
        latest_version = dateutil.parser.parse(entry_date)

    except Exception as e:
        print(e)
        return False, None, ''
    
    if(os.path.exists(versionfile)):
        with open(file=f"{versionfile}", mode='r')as f:
            current_version_str = f.read()
    else:
        print('no version file, downloading the new version...')
        return True, latest_version, entry_date
        
    

    

    if(current_version_str == ''):
        print('no version file, downloading the new version...')
        return True, latest_version, entry_date
    
    current_version = dateutil.parser.parse(current_version_str)


    if(current_version < latest_version):
        print('New Version Available!')
        return True, latest_version, entry_date
    else:
        print('Up To Date')
        return False, latest_version, entry_date




def download_update(username, reponame, versionfile, url):
    is_update_available, new_version, new_version_str = check_For_Updates(username=username, reponame=reponame, versionfile=versionfile)

    if(is_update_available):
        print(f'downloading from {url}')
        
        try:
            filename = wget.download(url)
        except Exception as e:
            print(e)
            return
        print('HERERERER')
        print(filename)
        new_version_zipfile_path = os.path.join(os.getcwd(), filename)

        # subprocess.run('git pull')


        new_version_folder, extension = os.path.splitext(new_version_zipfile_path)
        with ZipFile(filename, 'r') as zObject: 
            temp_dir = os.path.join(os.getcwd(), 'temp')
            if(not os.path.exists(temp_dir)):
                os.mkdir(temp_dir)
            zObject.extractall()

            

        move_files_inside_folder_to_outside(new_version_folder)
        

        try:
            shutil.rmtree(temp_dir)
            os.remove(new_version_zipfile_path)
        except Exception as e:
            print(e)
        



        with open(file="ver.txt", mode='w')as f:
            f.write(new_version_str)


    else:
        print('Up to date :)')

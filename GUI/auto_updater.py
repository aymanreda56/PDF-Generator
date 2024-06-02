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



with open('db_path.txt', 'r') as f:
    DB_FOLDER = os.path.abspath(f.read())
    DB_PATH = os.path.abspath(os.path.join(DB_FOLDER, 'Soldiers.db'))



# username = 'aymanreda56'
# reponame= 'test'
# versionfile='ver.txt'
# url = f'http://github.com/{username}/{reponame}/archive/main.zip'



def merge_directories(src:str, dst:str) -> None:
    """
    Recursively merges two directories. Files in the destination directory
    will be replaced by files with the same name from the source directory.

    :param src: The source directory path
    :param dst: The destination directory path
    """

    for src_dir, dirs, files in os.walk(src):
        # Calculate the relative path from the source directory
        relative_path = os.path.relpath(src_dir, src)
        # Determine the corresponding destination directory
        dst_dir = os.path.join(dst, relative_path)

        # Ensure the destination directory exists
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # Copy files from the source to the destination
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            shutil.copy2(src_file, dst_file)

    # Walk the directories again to ensure all subdirectories are created
    for src_dir, dirs, files in os.walk(src):
        for dir_ in dirs:
            src_subdir = os.path.join(src_dir, dir_)
            dst_subdir = os.path.join(dst, os.path.relpath(src_subdir, src))
            if not os.path.exists(dst_subdir):
                os.makedirs(dst_subdir)

# if __name__ == "__main__":
#     src_folder = "path/to/source_folder"
#     dst_folder = "path/to/destination_folder"
#     merge_directories(src_folder, dst_folder)





def move_files_inside_folder_to_outside(folder_path):

    # Get a list of all files inside the folder
    files = os.listdir(folder_path)
    parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(folder_path)))
    
    # # Move each file to the parent directory
    # for file_name in files:
    #     # Construct the source and destination paths
    #     source = os.path.join(folder_path, file_name)
    #     destination = os.path.join(parent_folder, file_name)
        
    #     # Move the file
    shutil.copytree(folder_path, parent_folder, dirs_exist_ok=True)
    
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        print(e)




def move_db_folder(destination_folder):
    db_folder_path = DB_FOLDER#os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')

    #dst_folder = os.path.dirname(db_folder_path)
    shutil.copyfile(db_folder_path, destination_folder)


# def return_db_folder():
#     db_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')
#     dst_folder = os.path.dirname(db_folder_path)
#     shutil.copyfile(dst_folder, db_folder_path)
#     shutil.rmtree(dst_folder)




def check_For_Updates(username, reponame, versionfile):

    try:
        r = requests.get(f"https://api.github.com/repos/{username}/{reponame}/commits")
        r = r.json()
        
        print(r)

        if(type(r) == dict):
        
            if(('commit' not in r.keys())):
                return False, None, ''
            
        elif(type(r) == list):
            print(r[0].keys())
            if ('commit' not in r[0].keys()):
                return False, None, ''
        entry_date = r[0]['commit']['author']['date']
        latest_version = dateutil.parser.parse(entry_date)

    except Exception as e:
        print(e)
        print("Can't connect to remote server, either due to internet issues or the repo is private")
        return False, None, ''
    

    versionfile = os.path.join( os.path.dirname(os.path.abspath(__file__)) , versionfile)
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

    versionfile = os.path.join( os.path.dirname(os.path.abspath(__file__)) , versionfile)

    if(is_update_available):
        print(f'downloading from {url}')
        
        try:
            project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            outside_project_folder = os.path.dirname(project_folder)
            filename = wget.download(url, out = outside_project_folder, bar=None)
            filename = os.path.abspath(filename)
        except Exception as e:
            print(e)
            return
        print('HERERERER')
        print(filename)

        try:
            pass
            # new_version_zipfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        except Exception as e:
            print(e)
            print('error during extracting the zip file')
            return
        

        # subprocess.run('git pull')


        # new_version_folder, extension = os.path.splitext(new_version_zipfile_path)
        with ZipFile(filename, 'r') as zObject: 
            temp_dir = os.path.join(outside_project_folder, 'temp')
            if(not os.path.exists(temp_dir)):
                os.mkdir(temp_dir)
            zObject.extractall(path = temp_dir)

            assert(len(os.listdir(temp_dir)) > 0)
            new_version_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])


        merge_directories(src = new_version_folder, dst = project_folder)
            

        # move_files_inside_folder_to_outside(new_version_folder)
        

        # try:
        #     shutil.rmtree(temp_dir)
        os.remove(filename)
        # except Exception as e:
        #     print(e)
        

        # _, onlynewFoldername = os.path.split(filename)

        

        with open(file="ver.txt", mode='w')as f:
            f.write(new_version_str)

        # workpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # cleanup(workpath=workpath, new_workpath=os.path.join( workpath, onlynewFoldername))


    else:
        print('Up to date :)')



def cleanup(workpath:str, new_workpath:str):
    shutil.copytree(DB_FOLDER, new_workpath)

    allFolders = os.listdir(workpath)
    for folder in allFolders:
        if(os.path.abspath(os.path.abspath(os.path.join(workpath, folder))) == os.path.abspath(new_workpath)):
            continue
        shutil.rmtree(os.path.abspath(os.path.abspath(os.path.join(workpath, folder))))
    




# download_update(username=username, reponame=reponame, versionfile=versionfile, url=url)
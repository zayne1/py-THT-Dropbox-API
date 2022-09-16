from datetime import datetime, timedelta
import os
import random
import json
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

APP_KEY = "osaf9oqdzzd6wbx"
APP_SECRET = "dr8hy4doxwj4586"
# APP_REFRESH_TOKEN = 'hWab75X6Qm8AAAAAAAAAATYN67Kptbi76QOInZ8cRqM7xMllwsv9VpfmQ2S4ESAA'
APP_REFRESH_TOKEN = 'TN_RtZuRTz8AAAAAAAAAAYuNPb38WlYHitRH_2kDKX8pLczkiJAhDVHlK577X5t9'
ACCESS_TOKEN=''


def print_logo():
    print('')
    print('██████╗░██████╗░░█████╗░██████╗░██████╗░░█████╗░██╗░░██╗')
    print('██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝')
    print('██║░░██║██████╔╝██║░░██║██████╔╝██████╦╝██║░░██║░╚███╔╝░')
    print('██║░░██║██╔══██╗██║░░██║██╔═══╝░██╔══██╗██║░░██║░██╔██╗░')
    print('██████╔╝██║░░██║╚█████╔╝██║░░░░░██████╦╝╚█████╔╝██╔╝╚██╗')
    print('╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═════╝░░╚════╝░╚═╝░░╚═╝')
    print('')
    print('░█████╗░░█████╗░███╗░░██╗███╗░░██╗███████╗░█████╗░████████╗░█████╗░██████╗░')
    print('██╔══██╗██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗')
    print('██║░░╚═╝██║░░██║██╔██╗██║██╔██╗██║█████╗░░██║░░╚═╝░░░██║░░░██║░░██║██████╔╝')
    print('██║░░██╗██║░░██║██║╚████║██║╚████║██╔══╝░░██║░░██╗░░░██║░░░██║░░██║██╔══██╗')
    print('╚█████╔╝╚█████╔╝██║░╚███║██║░╚███║███████╗╚█████╔╝░░░██║░░░╚█████╔╝██║░░██║')
    print('░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝')
    print('')

def oauth_reg_flow():
    """
    Reg flow to get an access token online, as per Dropbox docs
    We did some research and found a better way, with curl, which needs 
    No user input to generate an access token
    
    Args:
      
    Returns:
      
    Raises:
      none
    """


    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

    with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
        dbx.users_get_current_account()
        print("Successfully set up client!")
    oauth_result = auth_flow.finish(auth_code)


def get_cached_access_token():

    """
    get a cached (in local file storage) token
    
    Args:
    
    Returns:
      the access token or False
      
    Raises:
      none
    """

    file_exists = os.path.exists('access_cache.txt')
    ACCESS_TOKEN = False

    if not file_exists:
        print('* Info: Access cache file does not exist, creating a new one')
        ACCESS_TOKEN = get_new_access_token()
    
    # file should exist, containing access token
    else:
        f = open("access_cache.txt", "r")
        last_updated_str = str(f.readline())
        last_updated_str = last_updated_str.rstrip("\r\n")
        last_updated_dt = datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S.%f')
        ACCESS_TOKEN = f.readline()
        f.close()
    
    # if file exists, and more than 3 hours have passed
    if file_exists and(datetime.now() - last_updated_dt) > timedelta(hours=3):
        print('* Info: Access cache file will expire soon, creating a new one')
        ACCESS_TOKEN = get_new_access_token() # get new token as they expire after 4 hours

    return ACCESS_TOKEN


def get_new_access_token():
    """
    get a brand new access token if our cache is invalid
    
    Args:
    
    Returns:
      Access tokem
      
    Raises:
      none
    """

    # get short lived token via curl as per
    # https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/Get-refresh-token-from-access-token/m-p/596755/highlight/true#M27728
    result = os.popen("curl -s https://api.dropbox.com/oauth2/token -d refresh_token="+APP_REFRESH_TOKEN+" -d grant_type=refresh_token -d client_id="+APP_KEY+" -d client_secret="+APP_SECRET+" ").read()
    ACCESS_TOKEN = json.loads(result)['access_token']

    f = open("access_cache.txt", "w")
    f.write(str(datetime.now()))
    f.write("\r\n")
    f.write(ACCESS_TOKEN)
    f.close()

    return ACCESS_TOKEN


def connect_dropbox(ACCESS_TOKEN):
    """
    Connect to dropbox api
    
    Args:
      ACCESS_TOKEN: access token
    
    Returns:
      drop box instance or or False
      
    Raises:
      none
    """
    
    dbx = False
    
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
    except AuthError as e:
        print('There was an error connecting to Dropbox ' + str(e))
    return dbx


def get_remote_file_list(dbx, path):

    """
    Get list of files in remote path specified
    
    Args:
      dbx: drop box instance
      path: remote path
    
    Returns:
      True or nothing
      
    Raises:
      none
    """

    # could also use: 
    # for entry in dbx.files_list_folder('').entries:
    #     print(entry.name)

    files = dbx.files_list_folder(path).entries
    f_list=[]

    for file in files:
        f_list.append({'name': file.name, 'modified': file.client_modified,})

    return f_list


def get_space_allocated(ACCESS_TOKEN):
    """
    return space allocated for user (2GB for free tier)
    
    Args:
      ACCESS_TOKEN: access token
    
    Returns:
      size alloc in mb
      
    Raises:
      none
    """

    result = os.popen("curl -s -X POST https://api.dropboxapi.com/2/users/get_space_usage --header 'Authorization: Bearer "+ ACCESS_TOKEN +"'").read()
    allocation = json.loads(result)['allocation']['allocated']
    allocation = allocation / 1000
    allocation = allocation / 1000
    return int(allocation)


def upload_file(local_file_path, dbx):
    """
    Upload local file to remote root dir
    
    Args:
      local_file_path: local file + path str
    
    Returns:
      
    Raises:
      none
    """

    remote_target_dir = '/'
    file_name = os.path.basename(local_file_path)
    remote_file_and_path = remote_target_dir + file_name

    with open(local_file_path, 'rb') as f:
        dbx.files_upload(f.read(), remote_file_and_path, mode=dropbox.files.WriteMode.overwrite)


def generate_random_file():
    """
    generate a random file name, put some random text in it
    
    Args:
      
    Returns:
      str path to new file
      
    Raises:
      none
    """
    
    fname = os.getcwd() + '/new-tmp-file-' + str(random.randint(1000,9999)) + '.txt'

    f = open(fname, "w")
    f.write(str(datetime.now()))
    f.write("\r\n")
    f.write('temp file')
    f.close()

    return str(fname)


def main():
    """
    Dropbox connect
    ---------------

    print logo,
    get an access token,
    connect,
    show remote user's name,
    retrieve remote file list,
    retrieve remote storage info,
    create random file, insert some random text, and upload it,
    retrieve updated remote file list


    TODO:
    enhancement: create readme
    enhancement: we put it inside a class (define structure before coding)
    enhancement: we put our settings in a seperate file that we import
    enhancement: we show via a tree structure which shows dirs
    enhancement: we show files inside tables on terminal
    enhancement: we chnage our txt files to python code files with syntax highlighting
    enhancement: MAke it constantly loop (like we did in prev task) and ask for input at bottom, 
    """

    print_logo()

    
    
    try:
        ACCESS_TOKEN = get_cached_access_token()
    except Exception:
        abort(401)

    dbx = connect_dropbox(ACCESS_TOKEN)
    acc=dbx.users_get_current_account()

    print("_________________________________________________________\r\n")
    print('Good day, user: ' + acc.name.display_name)
    print("_________________________________________________________")
    print("\r\n\r\n")


    print("Remote File list:________________________________________")
    print("=========================================================\r\n")
    flist = get_remote_file_list(dbx, '')
    for file in flist:
        print(file.get('name').rjust(3), file.get('modified'))
        print('_________________________________________________________')
    print("\r\n\r\n")
    
    print("Storage info:____________________________________________")
    print("=========================================================\r\n")
    space_usage = dbx.users_get_space_usage()
    print('Used Space:      '+ str(space_usage.used) + ' Bytes')
    print('Allocated Space: '+ str(get_space_allocated(ACCESS_TOKEN))+' MB')
    print('_________________________________________________________')
    print("\r\n\r\n")

    print("File creation and upload:________________________________")
    print("=========================================================\r\n")
    new_random_file = generate_random_file()
    print('New file created: '+ new_random_file)
    print('Uploading new file: "'+os.path.basename(new_random_file)+'"" <<<<<<<')
    upload_file(new_random_file, dbx)
    print("\r\n\r\n")


    print("Updated Remote File list:________________________________")
    print("=========================================================\r\n")
    flist = get_remote_file_list(dbx, '')
    for file in flist:
        print(file.get('name').ljust(3), file.get('modified'))
        print('_________________________________________________________')
    print("\r\n\r\n")
    


    


# Using the special variable 
# __name__
if __name__=="__main__":
    main()

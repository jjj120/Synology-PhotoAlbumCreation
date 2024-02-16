from synology_api import photos, exceptions
from dotenv import load_dotenv
import os, pyotp, json, time

load_dotenv()

IP = os.getenv('SYNOLOGY_IP')
PORT = os.getenv('SYNOLOGY_PORT')
USERNAME = os.getenv('SYNOLOGY_USERNAME')
PASSWORD = os.getenv('SYNOLOGY_PASSWORD')

OTP_SET = os.getenv('SYNOLOGY_OTP_SECRET') != None

TOTP_GEN = pyotp.TOTP(os.getenv('SYNOLOGY_OTP_SECRET'))

print(f"OTP_SET: {OTP_SET}, logging in as {USERNAME} at {IP}:{PORT}")

def json_print(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))

RETRIES = 3
loggedIn = False
for i in range(RETRIES):
    try:
        PHOTOS = photos.Photos(IP, PORT, USERNAME, PASSWORD, secure=False, cert_verify=False, dsm_version=7, debug=True, otp_code=(TOTP_GEN.now() if OTP_SET else None))
        loggedIn = True
        break
    except exceptions.LoginError as e:
        time.sleep(5)
        
if not loggedIn:
    print(f"Failed to login after {RETRIES} retries")
    exit(1)
    


def findAllAlbums(limit = 5000):
    albums = PHOTOS.list_albums(limit=limit)["data"]["list"]
    albumNames = [album["name"] for album in albums]
    return albums, albumNames

def default_onFind(folder, albums):
    print(f'Found folder {folder["id"]} at {folder["name"]}')

def search_teams_folders(root_id, albums, name, case_sensitive = False, onFind = default_onFind):
    queue = []
    folders = PHOTOS.list_teams_folders(root_id)["data"]["list"]
    for folder in folders:
        queue.append(int(folder["id"]))
    
    found = []
    foundNames = []
    
    while len(queue) > 0:
        folder = queue.pop(0)
        folder_data = PHOTOS.list_teams_folders(folder)["data"]["list"]
        for sub_folder in folder_data:
            if (case_sensitive and name in sub_folder["name"]) or (not case_sensitive and name.lower() in sub_folder["name"].lower()):
                found.append(int(sub_folder["id"]))
                foundNames.append(sub_folder["name"])
                
                if onFind != None:
                    onFind(sub_folder, albums)
                
                # searched folder cannot contain another searched folder
                continue
            queue.append(int(sub_folder["id"]))
    
    return found, foundNames

def onFind(folder, albums):
    print(f'Found folder {folder["id"]} at {folder["name"]}')
    
    create_album(folder, albums)


def create_album(folder, albumNames):
    albumName = "/".join(folder["name"].split("/")[2:-1]).strip()
    
    if albumName in albumNames:
        print(f"Album {albumName} already exists")
        return

    if " " in albumName:
        albumName = f'"{albumName}"'
    
    albumCondition = {
        "user_id":0,
        "item_type":[],
        "folder_filter":[int(folder["id"])]
    }
    
    print(f"Creating album {albumName} with condition {albumCondition}")
    album = PHOTOS.create_album(albumName, albumCondition)
    print("")
    
    return album

albums, albumNames = findAllAlbums()

root_id = 0
search_teams_folders(root_id, albumNames, "bearbeitet", onFind=onFind)


def delete_albums(albums):
    for album in albums:
        if ("Bearbeitet" == album["name"]):
            continue
        print(f'Deleting album {album["name"]}')
        PHOTOS.delete_album(int(album["id"]))
        print("")

# delete_albums(albums)
# Synology Photo Album creation script

This script is used to create a conditional album in Synology photos. It is primarily used for my own use case, but can be easily modified to suit your needs.

My use case is that I name all my edited photos `"bearbeitet/<original_name>-bearbeitet.jpg"`. I want to create an album for each directory that contains edited photos. The album then contains all photos in that directory.

I also have an album named `"Bearbeitet"`, which contains all edited photos. This album should not be touched. 

## Usage

1. Install the requirements with `pip install -r requirements.txt`
2. Create a `.env` file with the following content:
```python
SYNOLOGY_IP="<synology_ip>"
SYNOLOGY_PORT="<synology_port>" # Default is 5000 or 5001
SYNOLOGY_USERNAME="<synology_username>"
SYNOLOGY_PASSWORD="<synology_password>"
SYNOLOGY_OTP_SECRET="<synology_otp_secret>" # Optional if 2FA is enabled
SYNOLOGY_RETRIES=5 # Optional, default is 5
SYNOLOGY_DSM_VERSION=7 # Optional, default is 7
```
3. Run the script with `python main.py`

This can be run periodically on the NAS with the Task Scheduler to automatically create albums.

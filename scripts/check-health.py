# check if fm1.hmu.gr is up
import subprocess
import requests
import os
from ftplib import FTP, error_perm
from dotenv import load_dotenv

dotenv_path = '../wordpress/.env.ftp'
load_dotenv(dotenv_path)

ftp_user = os.getenv('FTP_USER_NAME')
ftp_pass = os.getenv('FTP_USER_PASS')

ftp_host = 'localhost'
ftp_port = 21


def check_ftp_server():
    try:
        with FTP() as ftp:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.set_pasv(True)  # Enable passive mode
            # Attempt to list the directory
            ftp.dir()
    except error_perm as e:
        print(f'Permission error: {e}')
        return False
    except Exception as e:
        print(f'Error connecting to FTP server: {e}')
        return False
    return True


def restart_service(service):
    # find the script root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if(service == 'icecast'):
        subprocess.run(['cmd', '/C', f'{script_dir}\\restart-icecast.bat'], check=True)
        print('IceCast restarted.')
    elif(service == 'nginx'):
        subprocess.run(['cmd', '/C', f'{script_dir}\\restart-nginx.bat'], check=True)
        print('Nginx restarted.')
    elif(service == 'wordpress'):
        subprocess.run(['cmd', '/C', f'{script_dir}\\restart-wordpress.bat'], check=True)
        print('WordPress restarted.')
    else:
        print('Error: Service not found.')
        return

try:
    # Localhost IceCast check
    requests.get('http://localhost:8082/')
    requests.get('http://localhost:8082/live.m3u')

    # Check website and icecast through HTTPS (nginx)
    wordpress = requests.get('https://fm1.hmu.gr/', verify=False)
    if(not(wordpress.status_code == 200)):
        print('Error: WordPress is not running.')
        restart_service("wordpress")
        restart_service("nginx")
    else:
        print('WordPress is healthy.')

    if not check_ftp_server():
        restart_service("wordpress")
    else:
        print('FTP server is healthy.')

    icecast = requests.get('https://fm1.hmu.gr:8000/status-json.xsl', verify=False)
    icestats = (icecast.json())["icestats"]
    if(not("source" in icestats.keys()) or not(icecast.status_code == 200)): # if butt is malfunctioning, icestats will not have a source key
        print('Error: IceCast is not running.')
        restart_service("icecast")
    else:
        print('IceCast is healthy.')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
    restart_service("icecast")
    restart_service("nginx")
    restart_service("wordpress")




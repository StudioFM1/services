# check if fm1.hmu.gr is up
import subprocess
import requests
import os

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
    # get status code
    if(not(wordpress.status_code == 200)):
        print('Error: WordPress is not running.')
        restart_service("wordpress")
        restart_service("nginx")

    # Check website and icecast through HTTPS (nginx)
    icecast = requests.get('https://fm1.hmu.gr:8000/status-json.xsl', verify=False)
    icestats = (icecast.json())["icestats"]
    if(not("source" in icestats.keys()) or not(icecast.status_code == 200)):
        print('Error: IceCast is not running.')
        restart_service("icecast")

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
    restart_service("icecast")
    restart_service("nginx")
    restart_service("wordpress")




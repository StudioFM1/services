# check if fm1.hmu.gr is up
import subprocess
import requests
import os

def restart_services():
    # find the script root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # run restart_services.bat
    subprocess.run(['cmd', '/C', f'{script_dir}\\restart-services.bat'], check=True)
    print('Services restarted.')

try:
    # Localhost IceCast check
    requests.get('http://localhost:8082/')
    requests.get('http://localhost:8082/live.m3u')

    # Check website and icecast through HTTPS (nginx)
    requests.get('https://fm1.hmu.gr/', verify=False)
    requests.get('https://fm1.hmu.gr:8000', verify=False)
    requests.get('https://fm1.hmu.gr:8000/live.m3u', verify=False)

    print('All services are up and running.')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
    restart_services()



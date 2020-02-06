import subprocess
import json

configfile = "competition.config"


ip = "172.168.1.128"


def ping_tests():
    try:
        with open(configfile) as f:
            config = json.load(f)
            nteams = config['NumberOfTeams']
            maddress = config['ManagementInterfaceAddress']

            for i in range(1, nteams+1):
                interface = config['Team%dInterface' % (i)]
                address = config['Team%dInterfaceAddress' % (i)]
                print('TEAM %d: %s ::: %s'.center(100) %
                      (i, interface, address))
            print('\n')
    except FileNotFoundError:
        print('Nessun file di configurazione trovato.')
    except (json.decoder.JSONDecodeError, KeyError):
        print('Il file di configurazione è vuoto o corrotto.')

    try:
        response = subprocess.check_output(
            ['ping', '-c', '3', ip],
            # stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
        )
    except subprocess.CalledProcessError:
        response = None

    print(response)

    if "0%" in response:
        print("host raggiunto, nessun pacchetto perso.")

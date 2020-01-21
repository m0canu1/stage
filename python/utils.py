import yaml
import json
import netifaces

configfile = "/home/alex/Desktop/git/stage/config/competition.config"
netplanfile = "/home/alex/Desktop/git/stage/yaml/50-cloud-init.yaml"
f2 = "/home/alex/Desktop/git/stage/yaml/phasetwo.yaml"

default_config = {'network': {'ethernets': {'ens33': {'dhcp4': False, 'dhcp6': False},
                                            'ens38': {'dhcp4': False, 'dhcp6': False},
                                            'version': 2}}}

competition_config = {}
# competition_config['VirtualRouterAddress'] = {}

# competition_config = {'VirtualRouterAddress': 0,
#                       'VirtualRouterInterface': 0,
#                       'ManagementMachineAddress': 0,
#                       'ManagementMachineInterface': 0,
#                       'NumberOfTeams': 0}

# dizionario per la configurazione netplan
config = {}
config['network'] = {}
config['network']['ethernets'] = {}
config['network']['ethernets']['version'] = {2}


def yes_or_no():
    query = input('Vuoi modificare? [y/n]: ')
    while (query not in ['y', 'n', 'Y', 'N'] or query == ''):
        print('Please answer with yes or no!'.center(50))
        query = input('Vuoi modificare? [y/n]: ')
    Fl = query[0].lower()
    if Fl == 'y':
        return True
    if Fl == 'n':
        return False


def address_to(address):
    i = len(address) - 1
    while (address[i]) != '.':
        address = address[:-1]
        i = i-1
    return address + '0'


def load_from_config():
    with open(configfile) as f:
        try:
            config = json.load(f)
            return config
        except ValueError: 
            return competition_config


def save_to_config(config):
    with open(configfile, 'w') as f:
        json.dump(config, f)
    config

def save_to_netplanconfig(config):
    with open(netplanfile, 'w') as f:
        yaml.safe_dump(config, f)


# 0 for Virtual Router
# 1 for Management
def set_address_support(machine):
    competition_config = load_from_config()
    address = ''

    if (machine == 0):
        while address == '':
            address = str(input("""Virtual Router address: """))
        competition_config["VirtualRouterAddress"] = address
    else:
        while address == '':
            address = str(input("""ManagementMachineAddress: """))
        competition_config["ManagementMachineAddress"] = address
    
    save_to_config(competition_config)


def set_address(machine):
    competition_config = load_from_config()

    if (machine == 0):
        if("VirtualRouterAddress" in competition_config):
            print("L'indirizzo corrente del Virtual Router è: %s" %
                  (competition_config["VirtualRouterAddress"]))
            if yes_or_no():
                set_address_support(0)
        else:
            set_address_support(0)

    else:
        if("ManagementMachineAddress" in competition_config):
            print("L'indirizzo corrente della Macchina di Management è: %s" %
                  (competition_config["ManagementMachineAddress"]))
            if yes_or_no():
                set_address_support(1)
        else:
            set_address_support(1)



def phase_one():

    address = str(input("""Virtual Router address: """))
    default_config['network']['ethernets']['ens33']['addresses'] = [
        address + '/24']
    competition_config['VirtualRouterAddress'] = address

    address = str(input("""Management Machine address: """))
    default_config['network']['ethernets']['ens38']['addresses'] = [
        address + '/24']
    competition_config['ManagementMachineAddress'] = address

    with open(configfile, 'w') as f:
        json.dump(competition_config, f)



def phase_two():
    with open(configfile) as f:
        competition_config = json.load(f)
    nteams = competition_config["NumberOfTeams"]
    vr_address = competition_config["VirtualRouterAddress"] + '/24'
    mma_address = competition_config["ManagementMachineAddress"] + '/24'

    config = yaml.load(open(f1, 'r'), Loader=yaml.FullLoader)

    config['network']['ethernets']['ens33']['addresses'] = [vr_address]
    config['network']['ethernets']['ens38']['addresses'] = [mma_address]

    for i in range(0, nteams):
        team_address = input("""Team %d address: """ % (i+1))
        addresses = {'addresses': [str(team_address + '/24')]}
        routes = [
            {'to': address_to(team_address) + '/24', 'via': default_gateway}]
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)] = addresses
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['routes'] = routes
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['dhcp4'] = False
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['dhcp6'] = False

    yaml.dump(config, open(f2, 'w'))
    remove_quotes(f2)


def remove_quotes(fname):
    file = open(fname, 'r')
    data = file.read()
    data = data.replace("'", "")
    file = open(fname, 'w')
    file.write(data)


def edit_vr_address():
    with open(configfile, 'r') as f:
        conf = json.load(f)
    new_val = str(input("Address of Virtual Router: "))
    conf["VirtualRouterAddress"] = new_val
    with open(configfile, 'w') as f:
        json.dump(conf, f)


def edit_mma_address():
    with open(configfile, 'r') as f:
        conf = json.load(f)
    new_val = str(input("Address of Management machine: "))
    conf["ManagementMachineAddress"] = new_val
    with open(configfile, 'w') as f:
        json.dump(conf, f)


def set_teams_number(nteams):
    with open(configfile, 'r') as f:
        conf = json.load(f)
    conf["NumberOfTeams"] = nteams
    with open(configfile, 'w') as f:
        json.dump(conf, f)


def get_interfaces_list_noloopback():
    # salva in una lista il nome di tutte le interfacce disponibili
    if_list = netifaces.interfaces()

    # elimina l'interfaccia di loopback
    if_list.pop(if_list.index('lo'))

    return if_list


def choose_interface(machine, if_list):
    print('Scegli tra le seguenti:\n')
    print(', '.join(if_list).center(100)+'\n')

    if (machine == 0):
        str = 'Virtual Router'
    else:
        str = 'Macchina di Management'

    interface = input('Interfaccia per %s: ' % (str))
    while (interface not in if_list):
        print('\nERRORE, interfaccia non presente. Scegli tra le seguenti:\n')
        print(', '.join(if_list).center(100)+'\n')
        interface = input('Riprova: ')

    competition_config = load_from_config()
    # salva le interfacce nel file di configurazione
    if (machine == 0):
        competition_config['VirtualRouterInterface'] = interface
    else:
        competition_config['ManagementMachineInterface'] = interface

    save_to_config(competition_config)
    return interface


def choose_teams_number_support(maxteams):
    competition_config = load_from_config()
    nteams = -1
    while (nteams < 0 or nteams > maxteams):
        try:
            nteams = int(input('Numero di squadre (max %d): ' % (maxteams)))
            if (nteams > maxteams):
                print('ERRORE, numero di squadre troppo alto. Riprova!')
            elif (nteams < 0):
                print('ERRORE, numero di squadre troppo basso. Riprova!')
        except ValueError:
            print("Input errato")
        

    # salva il numero di squadre nel file di configurazione
    competition_config['NumberOfTeams'] = nteams

    save_to_config(competition_config)

def choose_teams_number(maxteams):
    competition_config = load_from_config()

    if("NumberOfTeams" in competition_config):
        print("L'attuale numero di squadre è: %s" %
              (competition_config["NumberOfTeams"]))
        if yes_or_no():
            choose_teams_number_support(maxteams)
    else:
        choose_teams_number_support(maxteams)


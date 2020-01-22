import yaml
import json
import netifaces

configfile = "/home/alex/Desktop/git/stage/config/competition.config"
netplanfile = "/home/alex/Desktop/git/stage/yaml/50-cloud-init.yaml"

# dizionario per il file di configurazione
competition_config = {}

# dizionario per la configurazione netplan
netplan_config = {}
netplan_config['network'] = {}
netplan_config['network']['ethernets'] = {}
netplan_config['network']['ethernets']['version'] = {2}


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

#  
# def address_to(address):
#     i = len(address) - 1
#     while (address[i]) != '.':
#         address = address[:-1]
#         i = i-1
#     return address + '0'

# 
def load_from_config():
    with open(configfile) as f:
        try:
            temp_config = json.load(f)
            return temp_config
        except ValueError:
            return competition_config

# 
def save_to_config(config):
    with open(configfile, 'w') as f:
        json.dump(config, f)

# 
def load_from_netplanconfig():
    with open(netplanfile) as f:
        try:
            temp_config = json.load(f)
            return temp_config
        except ValueError:
            return netplan_config

# 
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

    return address

# 
def set_address(machine):
    competition_config = load_from_config()

    if (machine == 0):
        if("VirtualRouterAddress" in competition_config):
            print("L'indirizzo corrente del Virtual Router è: %s" %
                  (competition_config["VirtualRouterAddress"]))
            if yes_or_no():
                return set_address_support(0)
            else:
                return competition_config["VirtualRouterAddress"]
        else:
            return set_address_support(0)

    else:
        if("ManagementMachineAddress" in competition_config):
            print("L'indirizzo corrente della Macchina di Management è: %s" %
                  (competition_config["ManagementMachineAddress"]))
            if yes_or_no():
                return set_address_support(1)
            else:
                return competition_config["ManagementMachineAddress"]
        else:
            return set_address_support(1)

# def phase_two():
#     with open(configfile) as f:
#         competition_config = json.load(f)
#     nteams = competition_config["NumberOfTeams"]
#     vr_address = competition_config["VirtualRouterAddress"] + '/24'
#     mm_address = competition_config["ManagementMachineAddress"] + '/24'

#     netplan_config = yaml.load(open(f1, 'r'), Loader=yaml.FullLoader)

#     netplan_config['network']['ethernets']['ens33']['addresses'] = [vr_address]
#     netplan_config['network']['ethernets']['ens38']['addresses'] = [mm_address]

#     for i in range(0, nteams):
#         team_address = input("""Team %d address: """ % (i+1))
#         addresses = {'addresses': [str(team_address + '/24')]}
#         routes = [
#             {'to': address_to(team_address) + '/24', 'via': default_gateway}]
#         netplan_config['network']['ethernets']['ens' +
#                                        str(first_team_interface+i)] = addresses
#         netplan_config['network']['ethernets']['ens' +
#                                        str(first_team_interface+i)]['routes'] = routes
#         netplan_config['network']['ethernets']['ens' +
#                                        str(first_team_interface+i)]['dhcp4'] = False
#         netplan_config['network']['ethernets']['ens' +
#                                        str(first_team_interface+i)]['dhcp6'] = False

#     yaml.dump(netplan_config, open(f2, 'w'))
#     remove_quotes(f2)


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

# riceve una lista delle interfacce rimanenti insieme all'indirizzo del virtual router
# e dell'interfaccia della macchina di management
def set_teams_addresses(if_list, vr_address, mm_address):
    """
    Imposta gli indirizzi delle interfacce rimanenti

    Parameters:
    if_list (list): Lista delle interfacce rimanenti.
    vr_address (str): Indirizzo del Virtual Router
    mm_address (str): Indirizzo dell'interfaccia per la Macchina di Management
    """
    temp_config = load_from_config()
    nteams = temp_config['NumberOfTeams']

    vr = vr_address.split('.')[2]
    mm = mm_address.split('.')[2]

    ip = 1 #base of the second-last 8 bit of the IP
    # Assegna tutte le interfacce rimanenti

    for i in range(1, nteams+1):
        temp_config["Team%dInterface" % (i)] = if_list[i-1] #assegno l'interfaccia
        flag = False
        while not flag:
            if (ip not in (vr, mm)):
                temp_config["Team%dAddress" % (i)] = '172.168.%d.100' % (ip)
                flag = True
            ip += 1

    save_to_config(temp_config)



# 
def set_teams_number_support(maxteams):
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


def set_teams_number(maxteams):
    competition_config = load_from_config()

    if("NumberOfTeams" in competition_config):
        print("L'attuale numero di squadre è: %s" %
              (competition_config["NumberOfTeams"]))
        if yes_or_no():
            set_teams_number_support(maxteams)
    else:
        set_teams_number_support(maxteams)


# rimuove le virgolette
def remove_quotes(fname):
    file = open(fname, 'r')
    data = file.read()
    data = data.replace("'", "")
    file = open(fname, 'w')
    file.write(data)

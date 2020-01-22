import yaml
import json
import netifaces

configfile = "/home/alex/Desktop/git/stage/config/competition.config"
netplanfile = "/home/alex/Desktop/git/stage/yaml/50-cloud-init.yaml"

competition_config = {}


# dizionario per la configurazione netplan
netplan_config = {}
netplan_config['network'] = {}
netplan_config['network']['ethernets'] = {}
netplan_config['network']['ethernets']['version'] = 2


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


def load_from_config():
    with open(configfile) as f:
        try:
            temp_config = json.load(f)
            return temp_config
        except ValueError:
            return competition_config
#
# def load_from_config():
#     try:
#         with open(configfile) as f:
#             try:
#                 config = json.load(f)
#                 return config
#             except ValueError:
#                 config = {}
#                 return config
#     except FileNotFoundError:
#         print('Nessun file di configurazione trovato')


#
def save_to_config(config):
    with open(configfile, 'w') as f:
        json.dump(config, f)

#
def load_from_netplanconfig():
    with open(netplanfile) as f:
        try:
            config = json.load(f)
            return config
        except ValueError:
            return netplan_config

#
def save_to_netplanconfig(config):
    with open(netplanfile, 'w') as f:
        yaml.safe_dump(config, f)

# lettura da config
def read_config():
    try:
        with open(configfile) as f:
            config = json.load(f)
            try:
                nteams = config['NumberOfTeams']
            except KeyError:
                nteams = 0
            try:
                vinterface = config['VirtualRouterInterface']
            except KeyError:
                vinterface = ''
            try:
                vaddress = config['VirtualRouterAddress']
            except KeyError:
                vaddress = ''
            try:
                minterface = config['ManagementMachineInterface']
            except KeyError:
                minterface = ''
            try:
                maddress = config['ManagementMachineAddress']
            except KeyError:
                maddress = ''

            print('\n\n')
            print('VIRTUALROUTER: %s ::: %s'.center(100) %
                  (vinterface, vaddress))
            print('MANAGEMENT: %s ::: %s'.center(100) % (minterface, maddress))

            for i in range(1, nteams+1):
                interface = config['Team%dInterface' % (i)]
                address = config['Team%dAddress' % (i)]
                print('TEAM %d: %s ::: %s'.center(100) %
                      (i, interface, address))
            print('\n')
    except FileNotFoundError:
        print('Nessun file di configurazione trovato')


# recupera gli indirizzi di Router e interfaccia per management
# def get_address(machine):


# CREAZIONE DEL FILE NETPLAN PER LA FASE UNO
def phase_one():
    config = load_from_config()

    vr_address = config['VirtualRouterAddress'] + '/24'
    vr_interface = config['VirtualRouterInterface']
    mm_address = config['ManagementMachineAddress'] + '/24'
    mm_interface = config['ManagementMachineInterface']

    if_list = get_interfaces_list_noloopback()
    if_list.pop(if_list.index(vr_interface))
    if_list.pop(if_list.index(mm_interface))

    netplan_config['network']['ethernets'][vr_interface] = {}
    netplan_config['network']['ethernets'][mm_interface] = {}

    netplan_config['network']['ethernets'][vr_interface]['dhcp4'] = False
    netplan_config['network']['ethernets'][vr_interface]['dhcp6'] = False

    netplan_config['network']['ethernets'][mm_interface]['dhcp4'] = False
    netplan_config['network']['ethernets'][mm_interface]['dhcp6'] = False

    netplan_config['network']['ethernets'][vr_interface]['addresses'] = [
        vr_address]
    netplan_config['network']['ethernets'][mm_interface]['addresses'] = [
        mm_address]

    for interface in if_list:
        netplan_config['network']['ethernets'][interface] = {}
        netplan_config['network']['ethernets'][interface]['dhcp4'] = False
        netplan_config['network']['ethernets'][interface]['dhcp6'] = False

    save_to_netplanconfig(netplan_config)


# CREAZIONE DEL FILE DI NETPLAN PER LA FASE DUE
def phase_two():
    phase_one() #TODO perché con questo funziona?
    netplan_config = load_from_netplanconfig()
    config = load_from_config()

    nteams = config['NumberOfTeams']

    for i in range(1, nteams+1):
        interface = config['Team%dInterface' % (i)]
        address = config['Team%dAddress' % (i)]

        netplan_config['network']['ethernets'][interface] = {}
        netplan_config['network']['ethernets'][interface]['addresses'] = address

    save_to_netplanconfig(netplan_config)

# 0 for Virtual Router
# 1 for Management


def set_address_support(machine, config):
    address = ''

    if (machine == 0):
        while address == '':
            address = str(input("""Virtual Router address: """))
        config["VirtualRouterAddress"] = address

    else:
        while address == '':
            address = str(input("""Management Address: """))
        config["ManagementMachineAddress"] = address

    save_to_config(config)

    return address

#


def set_address(machine):
    config = load_from_config()

    if (machine == 0):
        if("VirtualRouterAddress" in config):
            print("L'indirizzo corrente del Virtual Router è: %s" %
                  (config["VirtualRouterAddress"]))
            if yes_or_no():
                return set_address_support(0, config)
            else:
                return config["VirtualRouterAddress"]
        else:
            return set_address_support(0, config)

    else:
        if("ManagementMachineAddress" in config):
            print("L'indirizzo corrente della Macchina di Management è: %s" %
                  (config["ManagementMachineAddress"]))
            if yes_or_no():
                return set_address_support(1, config)
            else:
                return config["ManagementMachineAddress"]
        else:
            return set_address_support(1, config)


def get_interfaces_list_noloopback():
    # salva in una lista il nome di tutte le interfacce disponibili
    if_list = netifaces.interfaces()

    # elimina l'interfaccia di loopback
    if_list.pop(if_list.index('lo'))

    return if_list


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
    config = load_from_config()
    nteams = config['NumberOfTeams']

    vr = int(vr_address.split('.')[2])
    mm = int(mm_address.split('.')[2])

    ip = 1  # base of the second-last 8 bit of the IP
    # Assegna tutte le interfacce rimanenti

    for i in range(1, nteams+1):
        config["Team%dInterface" % (i)] = if_list[i-1]  # assegno l'interfaccia
        flag = False
        while not flag:
            if (ip not in (vr, mm)):
                config["Team%dAddress" % (i)] = '172.168.%d.100' % (ip)
                flag = True
            ip += 1

    save_to_config(config)


#
def choose_interface_support(machine, if_list, config):
    print('Scegli tra le seguenti:\n')
    print(', '.join(if_list).center(100)+'\n')

    interface = ''

    if (machine == 0):
        interface = input('Interfaccia per VIRTUAL ROUTER: ')
        while (interface == '' or interface not in if_list):
            print('\nERRORE, interfaccia non presente. Scegli tra le seguenti:\n')
            print(', '.join(if_list).center(100)+'\n')
        config['VirtualRouterInterface'] = interface
    else:
        interface = input('Interfaccia per MANAGEMENT: ')
        while (interface == '' or interface not in if_list):
            print('\nERRORE, interfaccia non presente. Scegli tra le seguenti:\n')
            print(', '.join(if_list).center(100)+'\n')
        config['ManagementMachineInterface'] = interface

    save_to_config(config)
    return interface

#


def choose_interface(machine, if_list):
    config = load_from_config()

    if (machine == 0):
        str = 'VirtualRouterInterface'
    else:
        str = 'ManagementMachineInterface'

    if (machine == 0):
        str = 'VirtualRouterInterface'
        if ("VirtualRouterInterface" in config):
            print("L'interfaccia corrente del Virtual Router è: %s" %
                  (config[str]))
            if yes_or_no():
                return choose_interface_support(0, if_list, config)
            else:
                return config[str]
        else:
            return choose_interface_support(0, if_list, config)
    else:
        str = 'ManagementMachineInterface'
        if ("ManagementMachineInterface" in config):
            print("L'interfaccia corrente della Management Machine è: %s" %
                  (config[str]))
            if yes_or_no():
                return choose_interface_support(1, if_list, config)
            else:
                return config[str]
        else:
            return choose_interface_support(1, if_list, config)


#
def set_teams_number_support(maxteams, config):
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
    config['NumberOfTeams'] = nteams

    save_to_config(config)

#


def set_teams_number(maxteams):
    config = load_from_config()

    if("NumberOfTeams" in config):
        print("L'attuale numero di squadre è: %s" %
              (config["NumberOfTeams"]))
        if yes_or_no():
            set_teams_number_support(maxteams, config)
    else:
        set_teams_number_support(maxteams, config)


# rimuove le virgolette
def remove_quotes(fname):
    file = open(fname, 'r')
    data = file.read()
    data = data.replace("'", "")
    file = open(fname, 'w')
    file.write(data)

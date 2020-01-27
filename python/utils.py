import ipaddress
import json

import netifaces
import yaml

configfile = "competition.config"
netplanfile = "50-cloud-init.yaml"


# dizionario per la configurazione netplan
netplan_config = {}
netplan_config['network'] = {}
netplan_config['network']['version'] = 2
netplan_config['network']['renderer'] = 'networkd'
netplan_config['network']['ethernets'] = {}


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
    try:
        with open(configfile) as f:
            try:
                config = json.load(f)
                return config
            except:
                config = {}
                return config
    except:
        config = {}
        return config


#
def save_to_config(config):
    with open(configfile, 'w') as f:
        # json.dump(config, f)
        # json.dump(json.dumps(config, sort_keys=True, indent=4), f)
        f.write(json.dumps(config, indent=4, sort_keys=True))
        f.close()


#


def load_from_netplanconfig():
    try:
        with open(netplanfile) as f:
            try:
                config = yaml.load(f, Loader=yaml.FullLoader)
                return config
            except yaml.scanner.ScannerError:
                return False
                # print('ERRORE, file di configurazione .yaml corrotto. Riconfigurare fase 1')
    except FileNotFoundError:
        with open(netplanfile, 'w') as f:
            yaml.safe_dump(netplan_config, f)
        return False

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
        print('Nessun file di configurazione trovato.')
    except (json.decoder.JSONDecodeError, KeyError):
        print('Il file di configurazione è vuoto o corrotto.')


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
    return 'FASE 1: OK'

# CREAZIONE DEL FILE DI NETPLAN PER LA FASE DUE


def phase_two():
    # ripete la fase uno in ogni caso per accertarsi che il file .yaml sia
    # scritto correttamente e coerentemente con il file di configurazione (in caso di file corrotto,
    # scritto male, o scritto bene ma con parametri sbagliati non contenuti nel file di configurazione)
    phase_one()
    netplan_config = load_from_netplanconfig()
    # se il file .yaml è corrotto, lo corregge ripetendo la fase 1
    # e ricaricando la configurazione
    # if(not netplan_config):
    #     phase_one()
    #     netplan_config = load_from_netplanconfig()

    config = load_from_config()

    nteams = config['NumberOfTeams']

    for i in range(1, nteams+1):
        try:
            interface = config['Team%dInterface' % (i)]
            address = config['Team%dAddress' % (i)] + '/24'

            netplan_config['network']['ethernets'][interface] = {}
            netplan_config['network']['ethernets'][interface]['addresses'] = [
                address]
            netplan_config['network']['ethernets'][interface]['dhcp4'] = False
            netplan_config['network']['ethernets'][interface]['dhcp6'] = False
            save_to_netplanconfig(netplan_config)
        except:
            return 'FASE 2: ERRORE'
    # save_to_netplanconfig(netplan_config)
    return 'FASE 2: OK'

# 0 for Virtual Router
# 1 for Management


def set_address_support(machine, config):
    if (machine == 0):
        flag = False
        while not flag:
            address = str(input("""Virtual Router address: """))
            if check_ip(address):
                config["VirtualRouterAddress"] = address
                flag = True
            else:
                print('ERRORE, non è un indirizzo valido.')

    else:
        flag = False
        while not flag:
            address = str(input("""Management Address: """))
            if check_ip(address):
                config["ManagementMachineAddress"] = address
                flag = True
            else:
                print('ERRORE, non è un indirizzo valido.')

    save_to_config(config)

    return address

#


def set_address(machine):
    config = load_from_config()

    if (machine == 0):
        if("VirtualRouterAddress" in config and check_ip(config['VirtualRouterAddress'])):
            print("L'indirizzo corrente del Virtual Router è: %s" %
                  (config["VirtualRouterAddress"]))
            if yes_or_no():
                return set_address_support(0, config)
            else:
                return config["VirtualRouterAddress"]
        else:
            return set_address_support(0, config)

    else:
        if("ManagementMachineAddress" in config and check_ip(config['VirtualRouterAddress'])):
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

    try:
        vr = int(vr_address.split('.')[2])
        mm = int(mm_address.split('.')[2])

        ip = 1  # base of the second-last 8 bit of the IP
        # Assegna tutte le interfacce rimanenti

        for i in range(1, nteams+1):
            config["Team%dInterface" %
                   (i)] = if_list[i-1]  # assegno l'interfaccia
            flag = False
            while not flag:
                if (ip not in (vr, mm)):
                    config["Team%dAddress" % (i)] = '172.168.%d.100' % (ip)
                    flag = True
                ip += 1

        save_to_config(config)
        return True
    except IndexError:
        # print('ERRORE: Indirizzi del Router e/o Interfaccia di Management errati, ricontrolla.')
        return False

#


def choose_interface_support(machine, if_list, config):
    print('Scegli tra le seguenti:\n')
    print(', '.join(if_list).center(100)+'\n')

    # interface = ''

    if (machine == 0):
        interface = input('Interfaccia per VIRTUAL ROUTER: ')
        while (interface not in if_list):
            print('\nERRORE, interfaccia non presente. Scegli tra le seguenti:\n')
            print(', '.join(if_list).center(100)+'\n')
            interface = input('Interfaccia per VIRTUAL ROUTER: ')
        config['VirtualRouterInterface'] = interface
    else:
        interface = input('Interfaccia per MANAGEMENT: ')
        while (interface not in if_list):
            print('\nERRORE, interfaccia non presente. Scegli tra le seguenti:\n')
            print(', '.join(if_list).center(100)+'\n')
            interface = input('Interfaccia per MANAGEMENT: ')
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
        if (config and str in config):  # se dic vuoto ritorna false
            print("L'interfaccia corrente del Virtual Router è: %s" %
                  (config[str]))
            if yes_or_no():
                return choose_interface_support(0, if_list, config)
            else:
                return config[str]
        else:
            return choose_interface_support(0, if_list, config)
    else:
        if (config and str in config):  # se dic vuoto ritorna false
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


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

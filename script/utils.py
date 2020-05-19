import ipaddress
import json
import subprocess
import time
from pathlib import Path

import netifaces as ni
import yaml

configfile = "competition.config"
netplanfile = "/etc/netplan/50-cloud-init.yaml"


# dizionario per la configurazione netplan
netplan_config = {}
netplan_config['network'] = {}
netplan_config['network']['version'] = 2
netplan_config['network']['renderer'] = 'networkd'
netplan_config['network']['ethernets'] = {}


def yes_or_no():
    query = input('Do you want to edit? [y/n]: ')
    while (query not in ['y', 'n', 'Y', 'N'] or query == ''):
        print('Please answer with yes or no!'.center(50))
        query = input('Do you want to edit? [y/n]: ')
    Fl = query[0].lower()
    if Fl == 'y':
        return True
    if Fl == 'n':
        return False


def load_from_config():
    """
    Carica la configurazione dal file .config

    Returns
    -------
    config: dic
        la configurazione presente nel file .config oppure un dic vuoto
        se non è stata trovata alcuna configurazione (o file non presente).
    """
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


def save_to_config(config):
    """
    Salva la configurazione nel file .config 
    """
    with open(configfile, 'w') as f:
        f.write(json.dumps(config, indent=4, sort_keys=True))
        f.close()


def load_from_netplanconfig():
    """
    Carica la configurazione dal file *.yaml usato da Netplan

    Returns
    -------
    False
        se non è stato trovato alcun file *.yaml oppure se è corrotto (manomesso)

    config: dic
        l'attuale configurazione contenuta nel file *.yaml di Netplan
    """
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


def save_to_netplanconfig(config):
    """
    Salva la configurazione nel file *.yaml usato da Netplan

    Parameters
    ----------
    config : dic
        La configurazione (formato yaml) che verrà salvata su file.
    """
    with open(netplanfile, 'w') as f:
        yaml.safe_dump(config, f)


def print_config():
    """
    Legge la configurazione dal file .config


    FileNotFoundError
        Se non è stato trovato nessun file di configurazione.

    json.decoder.JSONDecodeError, KeyError
        Se il file di configurazione è vuoto oppure corrotto.
    """
    try:
        with open(configfile) as f:
            config = json.load(f)
            try:
                nteams = config['NumberOfTeams']
            except KeyError:
                nteams = 0
            try:
                vinterface = config['UplinkInterface']
            except KeyError:
                vinterface = ''
            try:
                vaddress = config['UplinkAddress']
            except KeyError:
                vaddress = ''
            try:
                minterface = config['ManagementInterface']
            except KeyError:
                minterface = ''
            try:
                maddress = config['ManagementInterfaceAddress']
            except KeyError:
                maddress = ''

            print('\n\n')
            print('UPLINK: %s ::: %s'.center(100) %
                  (vinterface, vaddress))
            print('MANAGEMENT: %s ::: %s'.center(100) % (minterface, maddress))

            for i in range(1, nteams+1):
                interface = config['Team%dInterface' % (i)]
                address = config['Team%dInterfaceAddress' % (i)]
                print('TEAM %d: %s ::: %s'.center(100) %
                      (i, interface, address))
            print('\n')
    except FileNotFoundError:
        print('No configurazione file found.')
    except (json.decoder.JSONDecodeError, KeyError):
        print('Configuration file is empty or corrupted.')


def set_address_support(machine, config):
    """
    Metodo di supporto per set_address()
    """

    if (machine == 0):
        flag = False
        while not flag:
            address = str(input("""UPLINK Address: """))
            # TODO inserire try/catch
            if check_ip(address):
                config["UplinkAddress"] = address
                flag = True
            else:
                print("ERROR, it's not a valid IP address.")

    else:
        flag = False
        while not flag:
            address = str(input("""Management Interface Address: """))
            if check_ip(address):
                config["ManagementInterfaceAddress"] = address
                flag = True
            else:
                print("ERROR, it's not a valid IP address.")

    save_to_config(config)

    return address


def set_address(machine):
    """
    Imposta l'indirizzo dell'interfaccia per la macchina.

    Parameters
    ----------
    machine: int
        0 : per l'interfaccia di UPLINK
        1 : per l'interfaccia usata dal Management
    """

    config = load_from_config()

    if (machine == 0):
        if("UplinkAddress" in config and check_ip(config['UplinkAddress'])):
            print("Current UPLINK address: %s" %
                  (config["UplinkAddress"]))
            if yes_or_no():
                return set_address_support(0, config)
            else:
                return config["UplinkAddress"]
        else:
            return set_address_support(0, config)

    else:
        if("ManagementInterfaceAddress" in config and check_ip(config['UplinkAddress'])):
            print("Current Management Interface address: %s" %
                  (config["ManagementInterfaceAddress"]))
            if yes_or_no():
                return set_address_support(1, config)
            else:
                return config["ManagementInterfaceAddress"]
        else:
            return set_address_support(1, config)


def get_interfaces_list_noloopback():
    """
    Restituisce tutte le interfacce del sistema, escludendo il 'loopback'

    Returns
    -------
    if_list : list
        con le interfacce disponibili per la gara
    """

    if_list = ni.interfaces()
    if_list.pop(if_list.index('lo'))

    return if_list


def set_teams_addresses(if_list, up_address, mm_address):
    """
    Imposta gli indirizzi delle interfacce rimanenti

    Parameters
    ----------
    if_list : list 
        Lista delle interfacce rimanenti.
    up_address : str
        Indirizzo di Uplink
    mm_address : str 
        Indirizzo dell'interfaccia per la Macchina di Management
    """

    config = load_from_config()
    nteams = config['NumberOfTeams']

    if_list = get_interfaces_list_noloopback()
    if_list.pop(if_list.index(config['ManagementInterface']))
    if_list.pop(if_list.index(config['UplinkInterface']))

    if (up_address):
        up = int(up_address.split('.')[2])
    else:
        print("Waiting 2 sec. for uplink to get the IP address.")
        time.sleep(2)
        up = ni.ifaddresses(config['UplinkInterface'])[
            ni.AF_INET][0]['addr']
        up = int(up.split('.')[2])

    mm = int(mm_address.split('.')[2])

    ip = 1  # base of the second-last 8 bit of the IP
    # Assegna tutte le interfacce rimanenti

    for i in range(1, nteams+1):
        config["Team%dInterface" %
               (i)] = if_list[0]  # assegno l'interfaccia
        # print(if_list)
        if_list.pop(0)  # rimuove l'interfaccia appena assegnata
        flag = False
        while not flag:
            if (ip not in (up, mm)):
                config["Team%dInterfaceAddress" %
                       (i)] = '172.168.%d.100' % (ip)
                flag = True
            ip += 1

    # print(if_list)

    disable_interfaces(if_list)

    save_to_config(config)


def choose_interface_support(machine, if_list, config):
    """
    Metodo di supporto per choose_interface()
    """

    print('Scegli tra le seguenti:\n')
    print(', '.join(if_list).center(100)+'\n')

    # interface = ''

    if (machine == 0):
        interface = input("UPLINK Interface: ")
        while (interface not in if_list):
            print('\nERROR, not a valid interface. Choose from those:\n')
            print(', '.join(if_list).center(100)+'\n')
            interface = input("UPLINK Interface: ")
        config['UplinkInterface'] = interface
    else:
        interface = input('Interfaccia per il MANAGEMENT: ')
        while (interface not in if_list):
            print('\nERROR, not a valid interface. Choose from those:\n')
            print(', '.join(if_list).center(100)+'\n')
            interface = input('MANAGEMENT Interface: ')
        config['ManagementInterface'] = interface

    save_to_config(config)
    return interface


def choose_interface(machine, if_list):
    """
    Permette la scelta delle interfacce da una lista.

    Parameters
    ----------
    machine : int
        0 : se per l'interfaccia di uplink
        1 : se per l'interfaccia usata dal management

    if_list : list
        la lista con le interfacce disponibili per la scelta.
    """
    config = load_from_config()

    if (machine == 0):
        str = 'UplinkInterface'
    else:
        str = 'ManagementInterface'

    if (machine == 0):
        if (config and str in config):  # se dic vuoto ritorna false
            print("Current UPLINK Interface: %s" %
                  (config[str]))
            if yes_or_no():
                return choose_interface_support(0, if_list, config)
            else:
                return config[str]
        else:
            return choose_interface_support(0, if_list, config)
    else:
        if (config and str in config):  # se dic vuoto ritorna false
            print("Current MANAGEMENT Interface: %s" %
                  (config[str]))
            if yes_or_no():
                return choose_interface_support(1, if_list, config)
            else:
                return config[str]
        else:
            return choose_interface_support(1, if_list, config)


def set_teams_number_interactive_support(maxteams, config):
    """
    Metodo di supporto per set_teams_number_interactive()
    """

    nteams = -1
    while (nteams < 0 or nteams > maxteams):
        try:
            nteams = int(input('Number of TEAMS (max %d): ' % (maxteams)))
            if (nteams > maxteams):
                print('ERROR, the number is too high. Retry!')
            elif (nteams < 0):
                print('ERROR, the number is too low. Retry!')
        except ValueError:
            print("Erroneous input.")

    config['NumberOfTeams'] = nteams

    save_to_config(config)


def set_teams_number_interactive(maxteams):
    """
    Permette la scelta del numero di squadre

    Parameters
    ----------
    maxteams : int
        Numero massimo di squadre
    """

    config = load_from_config()

    if("NumberOfTeams" in config):
        print("Current number of TEAMS: %s" %
              (config["NumberOfTeams"]))
        if yes_or_no():
            set_teams_number_interactive_support(maxteams, config)
    else:
        set_teams_number_interactive_support(maxteams, config)


def check_ip(ip):
    """
    Verifica se un indirizzo ip è valido.
    """

    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def fw_rules_interactive(phase):
    config = load_from_config()

    config['Masquerading'] = input("""
                Choose masquerading mode:

                false -> no masquerading
                true -> random masquerading
                single ip -> will be used to mask all teams with the same
                ip for every team -> each ip will be used to mask each team (in order)
                
                NOTE: There are %d teams!

                """ % (config['NumberOfTeams']))
    config['Log'] = input("""
                Chosse logging mode:
                true -> log all
                false -> no logging
                value -> set a limit (eg. 3/sec, 3/min). If you omit the time measure, the default wil be in seconds.
                
                """)

    save_to_config(config)

    fw_rules(phase)


def fw_rules(phase):
    try:
        config = load_from_config()
        u_interface = config['UplinkInterface']
        m_interface = config['ManagementInterface']
        log = config['Log']
        masquerading = config['Masquerading']
        tmp = []
        for i in range(1, config["NumberOfTeams"] + 1):
            tmp.append(config['Team%dInterface' % (i)])

        # teams_interfaces = "\"" + ' '.join(tmp) + "\""
        teams_interfaces = ' '.join(tmp)

        response = subprocess.run(
            ["sudo", "./fwrules", "-p", str(phase), "-u", u_interface, "-m", m_interface, "-r",
                masquerading, "-t", teams_interfaces, "-l", log],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        print(response.stdout)

    except KeyError as identifier:
        # print(identifier)
        print("ERROR! Check your config.")
    except subprocess.CalledProcessError as identifier:
        print(identifier)


def disable_interfaces(if_list):
    # TODO non disabilita le interfacce non usate perché if_list è vuoto
    # print(if_list)
    # if(len(if_list) > 0):
    print("\nDisabling unused interfaces...\n")
    for interface in if_list:
        subprocess.run(["ip", "link", "set", "dev", interface, "down"])
        print(interface + " disabled.")


def create_netplan_config_interactive(if_list):
    config = load_from_config()

    management_interface_addr = config['ManagementInterfaceAddress']
    up_address = config['UplinkAddress']

    set_teams_addresses(if_list, up_address, management_interface_addr)

    create_netplan_config()


def create_config_file(up_interface, up_address,
                       management_interface, masquerading, management_interface_addr, teams_interfaces, log):
    config = {}
    try:
        if(up_address):
            ipaddress.ip_address(up_address)
        ipaddress.ip_address(management_interface_addr)
        config['NumberOfTeams'] = len(teams_interfaces)
        config['UplinkInterface'] = up_interface
        config['UplinkAddress'] = up_address
        config['ManagementInterface'] = management_interface
        config['ManagementInterfaceAddress'] = management_interface_addr
        config['Masquerading'] = masquerading
        config['Log'] = log

        save_to_config(config)

        # TODO forse inutile il reset
        # reset_netplan(up_interface)

        set_teams_addresses(teams_interfaces, up_address,
                            management_interface_addr)

        create_netplan_config()

    except ValueError as identifier:
        print(identifier)


def reset_netplan(up_interface):
    netplan_config['network']['ethernets'][up_interface] = {}
    netplan_config['network']['ethernets'][up_interface]['dhcp4'] = True
    netplan_config['network']['ethernets'][up_interface]['dhcp6'] = True

    save_to_netplanconfig(netplan_config)
    subprocess.run(["sudo", "netplan", "apply"])


def create_netplan_config():
    """
    Creates *.yaml file for Netplan and applies Netplan config.
    """

    config = load_from_config()

    m_interface = config['ManagementInterface']
    m_interface_addr = config['ManagementInterfaceAddress'] + '/24'

    up_interface = config['UplinkInterface']
    up_address = config['UplinkAddress']

    netplan_config['network']['ethernets'][m_interface] = {}
    netplan_config['network']['ethernets'][m_interface]['dhcp4'] = False
    netplan_config['network']['ethernets'][m_interface]['dhcp6'] = False
    netplan_config['network']['ethernets'][m_interface]['addresses'] = [
        m_interface_addr]

    netplan_config['network']['ethernets'][up_interface] = {}
    # Se non è stato assegnao un indirizzo all'uplink, allora si usa il DHCP per prenderlo
    if (up_address):
        up_address = up_address + '/24'
        netplan_config['network']['ethernets'][up_interface]['dhcp4'] = False
        netplan_config['network']['ethernets'][up_interface]['dhcp6'] = False
        netplan_config['network']['ethernets'][up_interface]['addresses'] = [
            up_address]
    else:
        netplan_config['network']['ethernets'][up_interface]['dhcp4'] = True
        netplan_config['network']['ethernets'][up_interface]['dhcp6'] = True

    # SETTA INTERFACCE SQUADRE
    for i in range(1, config['NumberOfTeams'] + 1):
        interface = config['Team%dInterface' % (i)]
        address = config['Team%dInterfaceAddress' % (i)] + '/24'

        netplan_config['network']['ethernets'][interface] = {}
        netplan_config['network']['ethernets'][interface]['dhcp4'] = False
        netplan_config['network']['ethernets'][interface]['dhcp6'] = False

        netplan_config['network']['ethernets'][interface]['addresses'] = [
            address]

    save_to_netplanconfig(netplan_config)

    subprocess.run(["sudo", "netplan", "apply"])

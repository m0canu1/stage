import netifaces
import sys
import subprocess
import argparse

from utils import fw_rules_interactive, create_netplan_config_interactive, fw_rules, create_netplan_config, create_config_file, get_interfaces_list_noloopback, print_config, choose_interface, set_teams_number, set_teams_addresses, set_address

vr = ''
mngmt = ''


def change_config():
    # Imposta l'interfaccia per l'uplink e la rimuove
    vr = choose_interface(0, if_list)
    if_list.pop(if_list.index(vr))

    # Imposta l'interfaccia per il Management e la rimuove
    mngmt = choose_interface(1, if_list)
    if_list.pop(if_list.index(mngmt))

    # Scelta del numero di squadre
    set_teams_number(len(if_list))

    # Indirizzo del Virtual Router
    vr = set_address(0)

    # Indirizzo della Macchina di Management
    mngmt = set_address(1)


def second_menu():
    menu = -1
    while menu == -1 or menu == 1:
        try:
            menu = int(input("""
                1. Apply firewall rules for phase 1.
                2. Apply firewall rules for phase 2.
                3. Go back.
                0. Quit.
                """))
            if menu == 1:
                fw_rules_interactive(1)
            elif menu == 2:
                fw_rules_interactive(2)
            elif menu == 3:
                first_menu()
            elif (menu) == 0:
                sys.exit
            else:
                print("Your choice (%d) is wrong. Please, try again." % (menu))

        except ValueError:
            print('ERRORE di input.')


def first_menu():
    menu = -1
    while menu == -1 or menu == 1:
        try:
            menu = int(input("""
                1. Print current config.
                2. Config interfaces.
                3. Choose competition phase (Firewall rules).
                0. Quit.
            """))
            if menu == 1:
                print_config()
            elif menu == 2:
                change_config()
                create_netplan_config_interactive(if_list)
            elif menu == 3:
                second_menu()
            elif (menu) == 0:
                sys.exit
            else:
                print("Your choice (%d) is wrong. Please, try again." % (menu))
        except ValueError:
            print('ERRORE di input.')


parser = argparse.ArgumentParser()
parser.add_argument('-I', '--interactive',
                    help='configure in interactive mode', action='store_true')

parser.add_argument('-G', '--get',
                    help='get current configuration', action='store_true')

parser.add_argument('-L', '--listinterfaces',
                    help='list all available interfaces', action='store_true')

parser.add_argument('-p', '--phase',
                    help='phase of the competition (1 or 2)')

parser.add_argument('-ui', '--uplink_interface',
                    help='name of the uplink interface')

parser.add_argument('-ua', '--uplink_address',
                    help='address of the uplink interface')

parser.add_argument('-mi', '--management_interface',
                    help='name of the management interface')

parser.add_argument('-ma', '--management_interface_address',
                    help='address of the management interface')

parser.add_argument('-masq', '--masquerading',
                    help='masquerading mode')

parser.add_argument('-t', '--teams',
                    help='teams\' interfaces', nargs='+')

parser.add_argument('-l', '--loglimit',
                    help='log limit. If false logging disabled')

args = parser.parse_args()


if_list = get_interfaces_list_noloopback()


if(args.interactive):
    first_menu()
elif (args.get):
    print_config()
elif (args.listinterfaces):
    print('\n' + ', '.join(if_list).center(100)+'\n')
else:
    if(args.phase and args.uplink_interface and
            args.management_interface and args.management_interface_address and args.masquerading and args.teams and args.loglimit):
        try:
            if_list.pop(if_list.index(args.uplink_interface))
            if_list.pop(if_list.index(args.management_interface))

            for interface in args.teams:
                if_list.pop(if_list.index(interface))

            create_config_file(args.uplink_interface,
                               args.uplink_address, args.management_interface, args.masquerading, args.management_interface_address, args.teams, args.loglimit)

            if (args.phase == "1"):
                fw_rules(1)
            if (args.phase == "2"):
                fw_rules(2)

        except ValueError as identifier:
            # print("Some of the defined interfaces do not exist. Retry!")
            print(identifier)

    else:
        print("Some parameters missing. Retry!")

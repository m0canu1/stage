import netifaces
import sys
import subprocess
import argparse

from utils import enable_dhcp_uplink, get_interfaces_list_noloopback, print_config, choose_interface, set_teams_number, set_teams_addresses, set_address, phase_one, phase_two

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

    # if_list rimane con le interfacce disponibili per le squadre
    return set_teams_addresses(if_list, vr, mngmt)


def first_menu():
    menu = -1
    while menu == -1 or menu == 1:
        try:
            menu = int(input("""
                1. Visualizzare l'attuale configurazione.
                2. Scelta delle fasi
                3. Abilita dhcp per uplink.
                0. Quit.
            """))
            if menu == 1:
                print_config()
            elif menu == 2:
                second_menu()
            elif menu == 3:
                enable_dhcp_uplink()
            elif (menu) == 0:
                sys.exit
            else:
                print("Your choice (%d) is wrong. Please, try again." % (menu))
        except ValueError:
            print('ERRORE di input.')


def second_menu():
    # Scelta delle fasi
    menu = -1
    while menu == -1:
        try:
            menu = int(input("""
                1. Phase 1 (only management allowed).
                2. Phase 2 (All teams allowed).
                0. Go Back.
                """))
            if (menu) == 1:
                if(change_config()):
                    print(phase_one())
                    # subprocess.run(["sudo", "./fwrules", "1"])
                else:
                    print(
                        "ERRORE: Indirizzi di UPLINK e/o Interfaccia di Management errati, ricontrolla.")
            elif (menu) == 2:
                change_config()
                print(phase_two())

                # subprocess.run(["sudo", "./fwrules", "2"])

            elif (menu) == 0:
                first_menu()
            else:
                print("Your choice (%d) doesn't exit. Please, try again." % (menu))
        except ValueError:
            print('ERRORE di input.')


if_list = get_interfaces_list_noloopback()
# first_menu()


parser = argparse.ArgumentParser()
parser.add_argument('-I', '--interactive',
                    help='configure in interactive mode', action='store_true')

parser.add_argument('-G', '--get',
                    help='get current configuration', action='store_true')

parser.add_argument('-L', '--list',
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
                    help='teams\' interfaces')

parser.add_argument('-l', '--loglimit',
                    help='log limit. If not set, logging disabled')

parser.add_argument('-s', '--set',
                    help='configure competition directly from command line', nargs='?')
args = parser.parse_args()

# print(args.uplink)
# print(args.uplink_interface)

if(args.interactive):
    first_menu()
elif (args.get):
    print_config()
elif (args.list):
    print('\n' + ', '.join(if_list).center(100)+'\n')
else:
    if(args.phase and args.uplink_interface and args.uplink_address and 
        args.management_interface and args.management_interface_address and args.masquerading and args.teams):
        print("chefigo")
    else:
        print("Some parameters missing. Retry!")
    

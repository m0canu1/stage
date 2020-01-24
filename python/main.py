import netifaces
import sys
from utils import get_interfaces_list_noloopback, read_config, choose_interface, set_teams_number, set_teams_addresses, set_address, phase_one, phase_two

vr = ''
mngmt = ''

def change_config():
    # Imposta l'interfaccia per il Virtual Router e rimuove interfaccia scelta
    vr = choose_interface(0, if_list)
    if_list.pop(if_list.index(vr))

    # Imposta l'interfaccia per il Management e rimuove interfaccia scelta
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
                0. Quit.
            """))
            if menu == 1:
                read_config()
            elif menu == 2:
                second_menu()
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
                else:
                    print(
                        'ERRORE: Indirizzi del Router e/o Interfaccia di Management errati, ricontrolla.')
            elif (menu) == 2:
                change_config()
                print(phase_two())
            elif (menu) == 0:
                first_menu()
            else:
                print("Your choice (%d) doesn't exit. Please, try again." % (menu))
        except ValueError:
            print('ERRORE di input.')

if_list = get_interfaces_list_noloopback()
first_menu()

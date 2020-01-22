import netifaces
import sys
from utils import get_interfaces_list_noloopback, choose_interface, set_teams_number, set_teams_addresses, set_address, phase_one, phase_two

if_list = get_interfaces_list_noloopback()

print('\nImpostazione delle interfacce.\n')

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
set_teams_addresses(if_list, vr, mngmt)


# Scelta delle fasi
# TODO menu
menu = -1
print("Make a choice:")
while menu == -1:
    menu = int(input("""
        1. Phase 1 (only management allowed).
        2. Phase 2 (All teams allowed).
        0. Quit.
        """))
    if (menu) == 1:
        phase_one()
        print("Created configuration for Phase 1")
    elif (menu) == 2:
        phase_two()
        print("Created configuration for Phase 2")
    elif (menu) == 0:
        sys.exit
    else:
        print("Your choice (%d) is wrong. Please, try again." % (menu))
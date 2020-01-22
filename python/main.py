import netifaces
from utils import get_interfaces_list_noloopback, choose_interface, set_teams_number, set_teams_addresses, set_address
# dizionario per la configurazione netplan
config = {}
config['network'] = {}
config['network']['ethernets'] = {}
config['network']['ethernets']['version'] = {2}



if_list = get_interfaces_list_noloopback()

# aggiunta delle interfacce a config
for interface in if_list:
    config['network']['ethernets'][interface] = {}
print(config)

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

# creazione del file netplan

# FASE 1
    

# FASE 2
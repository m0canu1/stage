import yaml
import sys

# in_file = open("50-cloud-init.yaml", "r")
out_file = open("50-cloud-init.yaml", "w")

# parsed = yaml.load(stream, Loader=yaml.FullLoader)
# parsed = yaml.load(in_file)


phase_one = {'network': {'ethernets': {'ens33': {'dhcp4': False},
                                       'ens38': {'dhcp4': False},
                                       'ens39': {'dhcp4': False},
                                       'ens40': {'dhcp4': False}
                                       },
                         'version': 2}}

phase_two = {'network': {'ethernets': {'ens33': {'dhcp4': True},
                                       'ens38': {'dhcp4': True, 'dhcp6': False, 'gateway4': '172.16.128.1'},
                                       'ens39': {'dhcp4': True, 'dhcp6': False, 'gateway4': '172.16.128.1'},
                                       'ens40': {'dhcp4': True, 'dhcp6': False, 'gateway4': '172.16.128.1'}},
                         'version': 2}}

print("Choose Competition phase")
menu = -1  # initializes (menu) of type int to 0
while menu == -1:
    menu = int(input("""
        1. Phase 1 (only management allowed).
        2. Phase 2 (All teams allowed).
        0. Quit.
        """))
    if (menu) == 1:
        print("Created configuration for Phase 1")
        # print(phase_one)
        yaml.dump(phase_one, out_file)
    elif (menu) == 2:
        print("Created configuration for Phase 2")
        # print(phase_two)
        yaml.dump(phase_two, out_file)
    elif (menu) == 0:
        sys.exit
    else:
        print("Your choice (%d) is wrong. Please, try again." % (menu))



inserisci sottorete management
quanti team vuoi? inserisci indirizzo

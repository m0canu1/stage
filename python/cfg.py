import psutil
import yaml
import sys
import json
from phaseconfig import phase_one, phase_two, edit_vr_address, edit_mma_address, set_teams_number


menu = -1

print("Make a choice:")
while menu == -1:
    menu = int(input("""
        1. Phase 1 (only management allowed).
        2. Phase 2 (All teams allowed).
        3. Set Virtual Router Address
        4. Set Management Machine Address
        5. Set teams number
        0. Quit.
        """))
    if (menu) == 1:
        phase_one()
        print("Created configuration for Phase 1")
    elif (menu) == 2:
        phase_two()
        print("Created configuration for Phase 2")
    elif (menu) == 3:
        print("Not yet available.")
        # edit_config("VirtualRouterAddress")
    elif (menu) == 4:
        print("Not yet available.")
        # edit_config("ManagementMachineAddress")
    elif (menu) == 5:
        print("Not yet available.")
        # edit_config("NumberOfTeams")

    elif (menu) == 0:
        sys.exit
    else:
        print("Your choice (%d) is wrong. Please, try again." % (menu))

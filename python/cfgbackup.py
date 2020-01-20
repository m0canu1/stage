import yaml
import sys
from phaseconfig import phase_one, phase_two, remove_quotes

f1 = "/home/alex/Desktop/git/stage/yaml/phaseone.yaml"
f2 = "/home/alex/Desktop/git/stage/yaml/phasetwo.yaml"
configfile = "/home/alex/Desktop/git/stage/config/competition.config"


config = {'network': 'ethernets'}

menu = -1
nteams = 0
nteams = int(input("""Number of teams: """))
print("Choose Competition phase")
while menu == -1:
    menu = int(input("""
        1. Phase 1 (only management allowed).
        2. Phase 2 (All teams allowed).
        0. Quit.
        """))
    if (menu) == 1:
        out_file = open(f1, 'w')
        yaml.dump(phase_one(nteams), out_file)
        print("Created configuration for Pha6se 1")
    elif (menu) == 2:
        config = yaml.load(open(f1, 'r'), Loader=yaml.FullLoader)
        yaml.dump(phase_two(config, nteams), open(f2, 'w'))
        remove_quotes(f2)
        print("Created configuration for Phase 2")
    elif (menu) == 0:
        sys.exit
    else:
        print("Your choice (%d) is wrong. Please, try again." % (menu))

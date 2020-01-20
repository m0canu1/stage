import yaml
import json

configfile = "/home/alex/Desktop/git/stage/config/competition.config"
f1 = "/home/alex/Desktop/git/stage/yaml/phaseone.yaml"
f2 = "/home/alex/Desktop/git/stage/yaml/phasetwo.yaml"

default_config = {'network': {'ethernets': {'ens33': {'dhcp4': False, 'dhcp6': False},
                                            'ens38': {'dhcp4': False, 'dhcp6': False},
                                            'version': 2}}}

competition_config = {'VirtualRouterAddress': 0,
                      'ManagementMachineAddress': 0,
                      'NumberOfTeams': 0}

default_gateway = '0.0.0.0'

first_team_interface = 39


def address_to(address):
    i = len(address) - 1
    while (address[i]) != '.':
        address = address[:-1]
        i = i-1
    return address + '0'


def phase_one():
    nteams = int(input("""Number of teams: """))
    competition_config['NumberOfTeams'] = nteams

    address = str(input("""Virtual Router address: """))
    default_config['network']['ethernets']['ens33']['addresses'] = [
        address + '/24']
    competition_config['VirtualRouterAddress'] = address

    address = str(input("""Management Machine address: """))
    default_config['network']['ethernets']['ens38']['addresses'] = [
        address + '/24']
    competition_config['ManagementMachineAddress'] = address

    with open(configfile, 'w') as f:
        json.dump(competition_config, f)

    for i in range(0, nteams):
        dhcp = {'dhcp4': False, 'dhcp6': False}
        default_config['network']['ethernets']['ens' +
                                               str(first_team_interface+i)] = [dhcp]
    
    with open(f1,'w') as phase_one:
        yaml.safe_dump(default_config, phase_one)

def phase_two():
    with open(configfile) as f:
        competition_config = json.load(f)
    nteams = competition_config["NumberOfTeams"]
    vr_address = competition_config["VirtualRouterAddress"] + '/24'
    mma_address = competition_config["ManagementMachineAddress"] + '/24'

    config = yaml.load(open(f1, 'r'), Loader=yaml.FullLoader)

    config['network']['ethernets']['ens33']['addresses'] = [vr_address]
    config['network']['ethernets']['ens38']['addresses'] = [mma_address]


    for i in range(0, nteams):
        team_address = input("""Team %d address: """ % (i+1))
        addresses = {'addresses': [str(team_address + '/24')]}
        routes = [
            {'to': address_to(team_address) + '/24', 'via': default_gateway}]
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)] = addresses
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['routes'] = routes
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['dhcp4'] = False
        config['network']['ethernets']['ens' +
                                       str(first_team_interface+i)]['dhcp6'] = False
    
    yaml.dump(config, open(f2, 'w'))
    remove_quotes(f2)

    # return config2


def remove_quotes(fname):
    file = open(fname, 'r')
    data = file.read()
    data = data.replace("'", "")
    file = open(fname, 'w')
    file.write(data)


def edit_vr_address():
    with open(configfile,'r') as f:
        conf = json.load(f)
    new_val = str(input("Address of Virtual Router: "))
    conf["VirtualRouterAddress"] = new_val
    with open(configfile,'w') as f:
        json.dump(conf, f)

def edit_mma_address():
    with open(configfile, 'r') as f:
        conf = json.load(f)
    new_val = str(input("Address of Management machine: "))
    conf["ManagementMachineAddress"] = new_val
    with open(configfile, 'w') as f:
        json.dump(conf, f)

def set_teams_number():
    with open(configfile, 'r') as f:
        conf = json.load(f)
    new_val = str(input("Number of teams: "))
    conf["NumberOfTeams"] = new_val
    with open(configfile, 'w') as f:
        json.dump(conf, f)

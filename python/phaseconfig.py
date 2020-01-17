import yaml

config = {'network': {'ethernets': {'ens33': {'dhcp4': False, 'dhcp6': False},
                                    'ens38': {'dhcp4': False, 'dhcp6': False}#,
                                    # 'ens39': {'dhcp4': False, 'dhcp6': False},
                                    # 'ens40': {'dhcp4': False, 'dhcp6': False},
                                    # 'ens41': {'dhcp4': False, 'dhcp6': False}
                                    },
                      'version': 2}}

gateway = '0.0.0.0'

first_team_interface = 39


def address_to(address):
    i = len(address)-1
    while (address[i]) != '.':
        address = address[:-1]
        i = i-1
    return address + '0'


def phase_one(nteams):
    address = str(input("""Virtual Router address: """))
    config['network']['ethernets']['ens33']['addresses'] = [address + '/24']
    address = str(input("""Management Machine address: """))
    config['network']['ethernets']['ens38']['addresses'] = [address + '/24']

    for i in range(0, nteams):
        dhcp = {'dhcp4': False, 'dhcp6': False}
        config['network']['ethernets']['ens%d'%(first_team_interface+i)] = [dhcp]
    return config


def phase_two(config2, nteams):
    
    # TODO problema col for
    for i in range(0,nteams):
        address = input("""Team %d address: """ %(i))
        config2['network']['ethernets']['ens%d'%(first_team_interface+i)]['addresses'] = [address + '/24']
        routes = {'to': address_to(address), 'via': gateway}
        config2['network']['ethernets']['ens%d'%(first_team_interface+i)]['routes'] = [routes]


    # address = input("""Team 2 address: """)
    # config2['network']['ethernets']['ens40']['addresses'] = [address + '/24']
    # # print(address_to(address))
    # routes = {'to': address_to(address), 'via': gateway}
    # config2['network']['ethernets']['ens40']['routes'] = [routes]

    # address = input("""Team 3 address: """)
    # config2['network']['ethernets']['ens41']['addresses'] = [address + '/24']
    # # print(address_to(address))
    # routes = {'to': address_to(address), 'via': gateway}
    # config2['network']['ethernets']['ens41']['routes'] = [routes]

    return config2


def remove_quotes(fname):
    file = open(fname, 'r')
    data = file.read()
    data = data.replace("'", "")
    file = open(fname, 'w')
    file.write(data)

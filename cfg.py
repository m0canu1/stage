import yaml

fname = "phase1.yaml"

#  init_config: {}
#  instances:
#         - host: < IP >
#         username: < username >
#         password: < password >

stream = open(fname, 'r')
data = yaml.load(stream, Loader=yaml.FullLoader)

data['ens33'][0]['dhcp4'] = 'false'
data['ens38'][0]['dhcp4'] = 'true'
data['ethernets'][0]['password'] = 'Password'

with open(fname, 'w') as yaml_file:
    yaml_file.write(yaml.dump(data, default_flow_style=False))

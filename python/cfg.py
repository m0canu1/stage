import yaml
from nesteddictionary import get_value, set_value, del_entry

fname = "/home/alex/Desktop/git/stage/yaml/phase2.yaml"

#  init_config: {}
#  instances:
#         - host: < IP >
#         username: < username >
#         password: < password >

stream = open(fname, 'r')
data = yaml.load(stream, Loader=yaml.FullLoader)


print(get_value("network.ethernets.ens33", data))
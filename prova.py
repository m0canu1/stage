import yaml

in_file = open("50-cloud-init.yaml", "r")
out_file = open("output.yaml", "w")

parsed = yaml.load(stream, Loader=yaml.FullLoader)
parsed = yaml.load(in_file)
yaml.dump(parsed, out_file)
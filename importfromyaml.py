import yaml

in_file = open("phase2.yaml", "r")
out_file = open("imported.yaml", "w")

# parsed = yaml.load(stream, Loader=yaml.FullLoader)
parsed = yaml.load(in_file)


print(parsed)

yaml.dump(parsed, out_file)

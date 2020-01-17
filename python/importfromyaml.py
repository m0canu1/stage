import yaml

in_file = open("/home/alex/Desktop/git/stage/yaml/imported.yaml", "r")
out_file = open("imported.yaml", "w")

# parsed = yaml.load(stream, Loader=yaml.FullLoader)
parsed = yaml.load(in_file)


print(parsed)

# yaml.dump(parsed, out_file)

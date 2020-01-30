import subprocess

ip = "172.168.1.128"

# sends 2 packets
result = subprocess.run(["ping", ip, "-c", "2"])
print(result.stdout)
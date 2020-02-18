import subprocess

try:
    response = subprocess.run(
        ['dhcp-lease-list', '--parsable'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True  # return string not bytes
    )

    # print(response.stdout)

    list = response.stdout.split()
    # print(list)

    while True:
        try:
            index = list.index("IP")
            ip = list[(list.index("IP")+1)]
            print (ip)
            list.pop(index)
        except ValueError as identifier:
            # print(identifier)
            break


except subprocess.CalledProcessError as identifier:
    print(identifier)
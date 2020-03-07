from utils import load_from_config

config = load_from_config()

path_to_dhcpd_conf = "/etc/dhcp/dhcpd.conf"
path_to_isc = "/etc/default/isc-dhcp-server"


def subnet_settings(address):
    return """\nsubnet %s netmask 255.255.255.0 {
    option routers %s;
    range %s %s;\n}
    """ % (".".join(address.split('.')[0:3]) + ".0", address, ".".join(address.split('.')[0:3]) + ".128", ".".join(address.split('.')[0:3]) + ".150")



with open(path_to_dhcpd_conf, "w") as f:
    f.write("""option domain-name-servers 8.8.8.8, 8.8.4.4;
        \ndefault-lease-time 600;
        \nmax-lease-time 7200;
        \nddns-update-style none;
        \nauthoritative;
        """)
        
    f.write(subnet_settings(config['ManagementInterfaceAddress']))

    for i in range(1, config['NumberOfTeams'] + 1):
        f.write(subnet_settings(config['Team%dInterfaceAddress' % (i)]))


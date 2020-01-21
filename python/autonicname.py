import netifaces

# AF_LINK - link layer interface (mac address)
# AF_INET - normal internet addresses

# stampa solo il nome delle interfacce
if_list = netifaces.interfaces()
print(if_list)

# stampa tutti gli indirizzi di tutte le interfacce
# for i in if_list:
#     print(netifaces.ifaddresses(i))

# per ogni interfaccia i stampa i relativi indirizzi
for i in if_list:
    if_address = netifaces.ifaddresses(i)
    print(if_address[netifaces.AF_INET])


['lo', 'ens33', 'ens37', 'ens38', 'ens39', 'ens40']


# salva in una lista il nome di tutte le interfacce disponibili
if_list = netifaces.interfaces()

# stampa le interfacce una ad una
for interface in if_list:
    print(interface)

# stampa le interfacce senza parentesi
print(', '.join(if_list))

#esclude l'interfaccia di loopback
for i in range(1, len(if_list)):
    print(if_list[i])


# stampa
# for i in if_list:
#     print(netifaces.ifaddresses(i))

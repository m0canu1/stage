import subprocess
import json
import socket


def ping_test(ip):
    try:
        response = subprocess.run(
            ['ping', '-c', '3', ip],
            stdout=subprocess.PIPE,
            universal_newlines=True  # return string not bytes
        )
        if " 0% packet loss" in response.stdout:
            return True

    except subprocess.CalledProcessError:
        response = None
        return False


def iperf_udp_test(ip):
    try:
        response = subprocess.run(
            ['iperf', '-c', ip, '-u'],
            # timeout=10, # NON SERVE TIMEOUT PER LA TIPOLOGIA DI RISPOSTA DI UDP
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # return string not bytes
        )

        if "Server Report:" in response.stdout:
            return True

    except subprocess.CalledProcessError:
        return False

def iperf_tcp_test(ip):
    try:
        response = subprocess.run(
            ['iperf', '-c', ip],
            timeout=10,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # return string not bytes
        )

        if " connected " in response.stdout:
            return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        # print("timeout")
        return False


ip_list = [
    "172.168.1.128",
    "172.168.2.100",
    "172.168.2.128",
    "172.168.3.100",
    "172.168.3.130",
    "172.168.4.100",
    "172.168.4.128",
    "172.168.5.100",
    "172.168.5.128"
]

print("TEST FROM " + socket.gethostname() + ":\n\n")

for ip in ip_list:

    if(ping_test(ip)):
        print("PING: " + ip + " -> OK.\n")
    else:
        print("PING: " + ip + " -> NOPE.\n")
    if(iperf_udp_test(ip)):
        print("UDP: " + ip + " -> OK.\n")
    else:
        print("UDP: " + ip + " -> NOPE.\n")
    if(iperf_tcp_test(ip)):
        print("TCP: " + ip + " -> OK.\n")
    else:
        print("TCP: " + ip + " -> NOPE. \n")

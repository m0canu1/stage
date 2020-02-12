import subprocess
import json
import socket
import argparse


def ping_test(ip):
    try:
        response = subprocess.run(
            ['ping', '-c', '3', ip],
            stdout=subprocess.PIPE,
            universal_newlines=True  # return string not bytes
        )

        if(args.verbose):
            print(response.stdout)

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

        if(args.verbose):
            print(response.stdout)

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

        if(args.verbose):
            print(response.stdout)

        if " connected " in response.stdout:
            return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        # print("timeout")
        return False


def run_test(str, flag):
    if(flag):
        print(str + ip + " -> OK.\n")
        if(args.verbose):
            print('='*80 + "\n")
    else:
        print(str + ip + " -> NOPE.\n")
        if(args.verbose):
            print('='*80 + "\n")


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

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose',
                    help='increase output verbosity', action='store_true')
args = parser.parse_args()


print("\nTEST FROM " + socket.gethostname() + ":\n\n")


for ip in ip_list:
    run_test("PING: ", ping_test(ip))
    run_test("UDP: ", iperf_udp_test(ip))
    run_test("TCP: ", iperf_tcp_test(ip))

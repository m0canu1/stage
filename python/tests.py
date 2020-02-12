import subprocess
import json
import socket
import argparse
import datetime


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
            stderr=subprocess.STDOUT,
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
            timeout=15,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
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
parser.add_argument('-t', '--test',
                    help='which test to perform (different combinations between tcp, udp, ping)', nargs='+')
args = parser.parse_args()

# print (args.verbose)
# print (args.test)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("\nTEST FROM " + socket.gethostname() + ":\n\n")


for ip in ip_list:

    for test in args.test:
        if (test == 'ping'):
            run_test("PING: ", ping_test(ip))
        elif (test == 'tcp'):
            run_test("TCP: ", iperf_tcp_test(ip))
        elif (test == 'udp'):
            run_test("UDP: ", iperf_udp_test(ip))

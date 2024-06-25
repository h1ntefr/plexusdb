import base64
from datetime import datetime
import socket
import requests
import argparse
from colorama import init, Fore
import keyboard
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--arg1", type=int, help="Port (default: 3304)", default=3304)
parser.add_argument("-r", "--arg2", type=int, help="Receive buffer (default: 1024)", default=1024)
parser.add_argument("-f", "--arg3", type=str, help="Database file", default="db.xml")
parser.add_argument("-k", "--arg4", type=str, help="Password", default="PDB")
parser.add_argument("-l", "--arg5", type=str, help="Logging (true/false)", default="false")
parser.add_argument("-s", "--arg6", type=str, help="Host (default: localhost)", default="localhost")
parser.add_argument("-c", "--arg7", type=int, help="Max clients (default: 100)", default=100)
args = parser.parse_args()

started_time = f"{datetime.now().year}.{datetime.now().month}.{datetime.now().day} -- {datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"


def globIP():
    return requests.get('https://api.ipify.org').text

init()

def log(t):
    d = datetime.now()
    now_m = d.minute
    now_h = d.hour
    now_s = d.second
    now_d = d.day
    now_mt = d.month
    now_y = d.year
    if now_m < 10:
        now_m = "0"+str(d.minute)
    if now_d < 10:
        now_d = "0"+str(d.day)
    if now_h < 10:
        now_h = "0"+str(d.hour)
    if now_s < 10:
        now_s = "0"+str(d.second)
    if now_mt < 10:
        now_mt = "0"+str(d.month)
    if now_y < 10:
        now_y = "0"+str(d.year)
    print(f"{Fore.GREEN}[{now_d}.{now_mt}.{now_y} / {now_h}:{now_m}:{now_s}]{Fore.YELLOW} {t}", flush=True)

    if args.arg6 == "true":
        with open(f'{started_time}.log', 'a', encoding="utf-8") as file:
            file.write(f"\n{Fore.GREEN}[{now_d}.{now_mt}.{now_y} / {now_h}:{now_m}:{now_s}]{Fore.YELLOW} {t}")
            file.close()


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((str(args.arg6), args.arg1))
ss.listen(args.arg7)
log(f"Port:{Fore.CYAN}{args.arg1} ({ss.getsockname()[1]}){Fore.YELLOW}")
log(f"Recv:{Fore.CYAN}{args.arg2}{Fore.YELLOW}")
log(f"DB:{Fore.CYAN}{args.arg3}{Fore.YELLOW}")
log(f"PWD:{Fore.CYAN}{args.arg4}{Fore.YELLOW}")
log(f"LOG:{Fore.CYAN}{args.arg5}{Fore.YELLOW}")
log(f"Host:{Fore.CYAN}{args.arg6}{Fore.YELLOW}")
log(f"MaxClients:{Fore.CYAN}{args.arg7}{Fore.YELLOW}")
log(f"PlexusDB Server started on port {Fore.CYAN}localhost:{args.arg1}{Fore.YELLOW} and listen {Fore.CYAN}{args.arg7}{Fore.YELLOW} clients.")


while True:
    cs, ca = ss.accept()
    data = cs.recv(args.arg2)

    def ret(data):
        cs.send(str(data).encode())

    d = data.decode().split(';s;')
    if data:
        if args.arg4 == d[0]:

            db = ET.parse(args.arg3)
            x = db.getroot()

            def apply():
                tree = ET.ElementTree(x)
                return tree.write(args.arg3)


            if d[1] == "CREATE_GROUP":
                group = ET.SubElement(x, "group")
                group.set("sys-name", d[2])
                x.append(group)
                apply()
                if x.find(f'.//group[@sys-name="{d[2]}"]') != None:
                    ret("<pdb.SUCCESS>")
                else:
                    ret('<pdb.ERR_REQUEST_MISS>')
                log(f"Action {Fore.CYAN}CREATE_GROUP{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            elif d[1] == "REMOVE_GROUP":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                x.remove(group)
                apply()
                if x.find(f'.//group[@sys-name="{d[2]}"]') == None:
                    ret("<pdb.SUCCESS>")
                else:
                    ret('<pdb.ERR_REQUEST_MISS>')
                log(f"Action {Fore.CYAN}CREATE_COLUMN{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            elif d[1] == "WRITE":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = ET.SubElement(group, "item")
                item.set("sys-name", d[3])
                apply()
                if x.find(f'.//group[@sys-name="{d[2]}"]').find(f'.//item[@sys-name="{d[3]}"]') != None:
                    ret("<pdb.SUCCESS>")
                else:
                    ret('<pdb.ERR_REQUEST_MISS>')
                log(f"Action {Fore.CYAN}WRITE{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            elif d[1] == "ERASE":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = group.find(f'.//item[@sys-name="{d[3]}"]')
                group.remove(item)
                apply()
                if x.find(f'.//group[@sys-name="{d[2]}"]').find(f'.//item[@sys-name="{d[3]}"]') == None:
                    ret("<pdb.SUCCESS>")
                else:
                    ret('<pdb.ERR_REQUEST_MISS>')
                log(f"Action {Fore.CYAN}ERASE{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            elif d[1] == "ITEM_COUNT":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = group.findall("item")
                a = len(item)
                ret(a)
                log(f"Action {Fore.CYAN}ITEM_COUNT{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")

            elif d[1] == "GROUP_COUNT":
                group = x.findall("group")
                a = len(group)
                ret(a)
                log(f"Action {Fore.CYAN}GROUP_COUNT {Fore.YELLOW}from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")

            elif d[1] == "ITEMS":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                items = group.findall("item")
                a = []

                for i in items:
                    a.append(i.get("sys-name"))

                ret(a)
                log(f"Action {Fore.CYAN}ITEMS{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")

            elif d[1] == "GROUPS":
                groups = x.findall("group")
                a = []

                for g in groups:
                    a.append(g.get("sys-name"))

                ret(a)
                log(f"Action {Fore.CYAN}GROUPS {Fore.YELLOW}from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")


            elif d[1] == "CHECK":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = group.find(f'.//item[@sys-name="{d[3]}"]')
                if item != None:
                    a = "true"
                else:
                    a = "false"
                ret(a)
                log(f"Action {Fore.CYAN}CHECK{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")

            elif d[1] == "SETATTRIB":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = group.find(f'.//item[@sys-name="{d[3]}"]')
                item.set(d[4], d[5])
                apply()
                if x.find(f'.//group[@sys-name="{d[2]}"]').find(f'.//item[@sys-name="{d[3]}"]').get(d[4]) == d[5]:
                    ret("<pdb.SUCCESS>")
                else:
                    ret("<pdb.ERR_REQUEST_MISS>")
                log(f"Action {Fore.CYAN}SETATTRIB{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            elif d[1] == "GETATTRIB":
                group = x.find(f'.//group[@sys-name="{d[2]}"]')
                item = group.find(f'.//item[@sys-name="{d[3]}"]')
                a = item.get(d[4])
                ret(a)
                log(f"Action {Fore.CYAN}GETATTRIB{Fore.YELLOW} from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}. Sent: {Fore.CYAN}{a}")

            else:
                log(f"{Fore.YELLOW}Bad request from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")

            cs.close()



    else:
        log(f"Wrong password from {Fore.CYAN}{ca[0]}:{ca[1]}{Fore.YELLOW}.")
        ret("<pdb.ERR_WRONG_PWD>")
        cs.close()
#   <pdb.ERR_SERVER_SUSPENDED>          server suspended
#   <pdb.SUCCESS>                       operation successfully
#   <pdb.ERR_REQUEST_MISS>              request missed
#   <pdb.ERR_WRONG_PWD>                 wrong password

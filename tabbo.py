import requests
import json
import os
import time
import sys
from colorama import Fore, init

init(autoreset=True)

AUTH_SERVER = "https://tabbo-auth.vercel.app/api/auth"
LOOKUP_API = "https://tabbo-proxy.vercel.app/api/search?mobile="

USERS_FILE = "users.json"
LOG_FILE = "logs.json"


def clear():
    os.system("clear")


def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}


def save_json(file,data):
    with open(file,"w") as f:
        json.dump(data,f,indent=2)


def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


def login():

    clear()

    print(Fore.CYAN + """
🔐 TOOL LOGIN

Generate password contact admin
Telegram : @tabbo73
""")

    password = input("🔑 Password : ")

    try:

        r = requests.get(AUTH_SERVER, params={"pass": password}).json()

        if r.get("status") != "ok":

            print("❌ Invalid password")
            sys.exit()

    except:

        print("❌ Server error")
        sys.exit()


def banner(user,credits):

    clear()

    print(Fore.MAGENTA + """

████████╗ █████╗ ██████╗ ██████╗  ██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
   ██║   ███████║██████╔╝██████╔╝██║   ██║
   ██║   ██╔══██║██╔══██╗██╔══██╗██║   ██║
   ██║   ██║  ██║██████╔╝██████╔╝╚██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═════╝  ╚═════╝

""")


    print(Fore.CYAN + "⚡ TABBO OSINT TOOL\n")

    print(Fore.GREEN + f"👤 User : {user}")
    print(Fore.GREEN + f"💳 Credits : {credits}\n")


def search(user,users):

    if users[user]["credits"] <= 0:

        print("❌ No credits left")
        input()
        return

    number = input("📱 Mobile Number : ")

    print("🔎 Searching...\n")

    time.sleep(1)

    try:

        r = requests.get(LOOKUP_API + number)

        data = r.json()

        if isinstance(data,dict):

            for k in data:

                r = data[k]

                if r.get("name"):
                    print("👤 Name :",r["name"])

                if r.get("fname"):
                    print("👨 Father :",r["fname"])

                if r.get("address"):
                    print("🏠 Address :",r["address"])

                if r.get("circle"):
                    print("📡 Circle :",r["circle"])

                print()

    except:
        pass

    users[user]["credits"] -= 1
    users[user]["used"] += 1

    save_json(USERS_FILE,users)

    logs = load_json(LOG_FILE)

    logs[user] = {
        "ip": users[user]["ip"],
        "used": users[user]["used"]
    }

    save_json(LOG_FILE,logs)

    input("Press Enter...")


def menu(user,users):

    while True:

        banner(user,users[user]["credits"])

        print("""
1 Search
2 Exit
""")

        op = input("Select : ")

        if op == "1":
            search(user,users)

        elif op == "2":
            exit()


login()

users = load_json(USERS_FILE)

username = input("Username : ")

ip = get_ip()

if username not in users:

    users[username] = {
        "credits":5,
        "used":0,
        "ip":ip
    }

save_json(USERS_FILE,users)

menu(username,users)

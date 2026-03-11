import requests
import sys
import os
import time
import json
from colorama import Fore, Style, init

init(autoreset=True)

AUTH_SERVER = "https://tabbo-auth.vercel.app/api/auth"
LOOKUP_API = "https://tabbo-info.vercel.app/api/lookup?key=tabbo02&mobile="


def clear():
    os.system("clear")


def banner():

    clear()

    print(Fore.CYAN + """

████████╗ █████╗ ██████╗ ██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗
   ██║   ███████║██████╔╝██████╔╝
   ██║   ██╔══██║██╔══██╗██╔══██╗
   ██║   ██║  ██║██████╔╝██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═════╝

╔════════════════════════════════╗
║         TABBO INFO TOOL        ║
║      Cyber OSINT Scanner       ║
║      Credit ❤️ tabbo73         ║
║      Contact @tabbo73          ║
╚════════════════════════════════╝

""")


def loading():

    print(Fore.GREEN + "🔎 Scanning database", end="")

    for i in range(5):
        time.sleep(0.4)
        print(".", end="")

    print("\n")


def verify_password():

    password = input(Fore.YELLOW + "🔒 Enter Tool Password: ")

    try:

        r = requests.get(AUTH_SERVER, params={"pass": password})
        data = r.json()

        if data.get("status") != "ok":

            print(Fore.RED + "\n❌ Invalid password\n")
            sys.exit()

        print(Fore.GREEN + "\n✅ Access granted\n")
        time.sleep(1)

    except:

        print(Fore.RED + "\n❌ Server connection failed\n")
        sys.exit()


def load_users():

    try:
        with open("users.json") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):

    with open("users.json","w") as f:
        json.dump(data,f,indent=2)


def show_results(data):

    print(Fore.YELLOW + "\n📊 DATABASE RESULTS\n")

    if isinstance(data, dict):

        for i, key in enumerate(data,1):

            r = data[key]

            print(Fore.CYAN + "╔══════════════════════════════╗")
            print(Fore.CYAN + f"        📂 RECORD {i}")
            print(Fore.CYAN + "╚══════════════════════════════╝")

            print(Fore.GREEN + f"👤 Name     : {r.get('name','N/A')}")
            print(Fore.GREEN + f"👨 Father   : {r.get('fname','N/A')}")
            print(Fore.GREEN + f"🏠 Address  : {r.get('address','N/A')}")
            print(Fore.GREEN + f"☎ Alt Num   : {r.get('alt','N/A')}")
            print(Fore.GREEN + f"📡 Circle   : {r.get('circle','N/A')}")
            print(Fore.GREEN + f"🆔 ID       : {r.get('id','N/A')}")

            print(Fore.MAGENTA + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    else:

        print(data)


def search():

    users = load_users()

    user = input(Fore.YELLOW + "👤 Username : ")

    if user not in users:
        users[user] = 5

    if users[user] <= 0:

        print(Fore.RED + "\n❌ No credits left\n")
        time.sleep(2)
        return

    number = input(Fore.YELLOW + "\n📱 Enter mobile number: ")

    loading()

    try:

        r = requests.get(LOOKUP_API + number)

        data = r.json()

        show_results(data)

    except:

        print(Fore.RED + "\n❌ API Error\n")

    users[user] -= 1

    save_users(users)

    print(Fore.YELLOW + f"\n💳 Credits left : {users[user]}\n")

    input(Fore.CYAN + "Press ENTER to return dashboard...")


def dashboard():

    while True:

        banner()

        print(Fore.GREEN + """

1️⃣  Search Number
2️⃣  Exit Tool

""")

        op = input(Fore.YELLOW + "Select option: ")

        if op == "1":

            search()

        elif op == "2":

            clear()

            print(Fore.RED + """

Tool Closed Successfully

Goodbye Hacker 👋
""")

            sys.exit()

        else:

            print("Invalid option")
            time.sleep(1)


def main():

    banner()

    verify_password()

    dashboard()


main()

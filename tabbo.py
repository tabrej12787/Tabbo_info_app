import requests
import sys
import os
import time
from colorama import Fore, Style, init

init()

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

╔══════════════════════════════╗
║        TABBO INFO TOOL       ║
║      Credit ❤️ tabbo73       ║
║      Contact @tabbo73        ║
╚══════════════════════════════╝

""")


def loading():

    print(Fore.GREEN + "🔎 Searching", end="")

    for i in range(4):
        time.sleep(0.4)
        print(".", end="")

    print("\n")


def verify_password():

    password = input("🔒 Enter Tool Password: ")

    try:

        r = requests.get(AUTH_SERVER, params={"pass": password})
        data = r.json()

        if data.get("status") != "ok":

            print(Fore.RED + "\n❌ Invalid password\n")
            sys.exit()

        print(Fore.GREEN + "\n✅ Access granted\n")

    except:

        print(Fore.RED + "\n❌ Server connection failed\n")
        sys.exit()


def show_result(data):

    print(Fore.YELLOW + "\n📊 RESULT\n")

    if isinstance(data, list):

        for i, r in enumerate(data, 1):

            print(Fore.CYAN + f"━━━━ RECORD {i} ━━━━")

            print(Fore.GREEN + f"👤 Name   : {r.get('name','N/A')}")
            print(f"👨 Father : {r.get('fname','N/A')}")
            print(f"🏠 Address: {r.get('address','N/A')}")
            print(f"☎ Alt    : {r.get('alt','N/A')}")
            print(f"🆔 ID     : {r.get('id','N/A')}")

            print(Fore.CYAN + "━━━━━━━━━━━━━━━━\n")

    else:
        print(data)


def lookup():

    while True:

        print(Fore.GREEN + """
1️⃣ Search Number
2️⃣ Exit
""")

        op = input("Select option: ")

        if op == "1":

            number = input("\n📱 Enter mobile number: ")

            loading()

            try:

                r = requests.get(LOOKUP_API + number)

                data = r.json()

                show_result(data)

            except:

                print(Fore.RED + "\n❌ API error\n")

        elif op == "2":

            print("\nBye 👋")
            sys.exit()


def main():

    banner()

    verify_password()

    lookup()


main()
def main():

    banner()

    verify_password()

    lookup()

main()

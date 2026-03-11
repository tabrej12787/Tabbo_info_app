import requests
import sys
import os
import json
import time
from colorama import Fore, init

init(autoreset=True)

AUTH_SERVER = "https://tabbo-auth.vercel.app/api/auth"
LOOKUP_API = "https://tabbo-proxy.vercel.app/api/search?mobile="

HISTORY_FILE = "history.json"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


def load_history():

    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except:
        return []


def save_history(data):

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def banner(user, ip):

    clear()

    print(Fore.MAGENTA + """

████████╗ █████╗ ██████╗ ██████╗  ██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
   ██║   ███████║██████╔╝██████╔╝██║   ██║
   ██║   ██╔══██║██╔══██╗██╔══██╗██║   ██║
   ██║   ██║  ██║██████╔╝██████╔╝╚██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═════╝  ╚═════╝

""")

    print(Fore.CYAN + "🚀 TABBO OSINT TOOL\n")

    print(Fore.GREEN + f"👤 User : {user}")
    print(Fore.GREEN + f"🌐 IP   : {ip}\n")


def login():

    clear()

    print(Fore.YELLOW + """
🔐 ACCESS LOGIN

📩 Generate password contact admin
Telegram : @tabbo73
""")

    password = input("🔑 Enter Password : ")

    try:

        r = requests.get(AUTH_SERVER, params={"pass": password}).json()

        if r.get("status") != "ok":

            print(Fore.RED + "\n❌ Access denied\n")
            sys.exit()

    except:

        print("⚠️ Server error")
        sys.exit()


def show_results(data, number):

    print(Fore.YELLOW + f"\n📊 RESULTS FOR : {number}\n")

    if not isinstance(data, dict):

        print("❌ No data found")
        return

    for key in data:

        r = data[key]

        print(Fore.CYAN + "━━━━━━━━ PERSONAL INFO ━━━━━━━━")

        print("👤 Name      :", r.get("name","N/A"))
        print("👨 Father    :", r.get("fname","N/A"))

        print(Fore.CYAN + "━━━━━━━━ ADDRESS INFO ━━━━━━━━")

        print("🏠 Address   :", r.get("address","N/A"))

        print(Fore.CYAN + "━━━━━━━━ NETWORK INFO ━━━━━━━━")

        print("📡 Circle    :", r.get("circle","N/A"))
        print("🆔 ID        :", r.get("id","N/A"))

        print(Fore.MAGENTA + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def lookup():

    number = input(Fore.YELLOW + "📱 Enter Mobile Number : ")

    print(Fore.CYAN + "\n🔎 Searching database...\n")

    time.sleep(1)

    try:

        r = requests.get(LOOKUP_API + number)

        data = r.json()

        show_results(data, number)

        history = load_history()

        history.append(number)

        save_history(history)

    except:

        print("❌ No result found")

    input("↩ Press ENTER to return...")


def show_history():

    history = load_history()

    clear()

    print(Fore.YELLOW + "\n📜 SEARCH HISTORY\n")

    if not history:

        print("❌ No history found")

    else:

        for i, num in enumerate(history,1):

            print(f"{i}. {num}")

    input("\nPress ENTER...")


def clear_history():

    save_history([])

    print("🧹 History cleared")

    time.sleep(1)


def menu(user, ip):

    while True:

        banner(user, ip)

        print(Fore.GREEN + """

1️⃣  🔍 Search Mobile Number
2️⃣  📜 Search History
3️⃣  🧹 Clear History
4️⃣  ❌ Exit Tool

""")

        op = input("👉 Select option : ")

        if op == "1":

            lookup()

        elif op == "2":

            show_history()

        elif op == "3":

            clear_history()

        elif op == "4":

            print("👋 Tool closed")

            sys.exit()

        else:

            print("⚠️ Invalid option")

            time.sleep(1)


def main():

    login()

    user = os.getlogin()

    ip = get_ip()

    menu(user, ip)


if __name__ == "__main__":

    main()

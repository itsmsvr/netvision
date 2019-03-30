import winsound, requests, time, subprocess, sys
from requests.exceptions import SSLError, ConnectionError
from colorama import Fore, Style, Back, init

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end = '')

def clear():
    subprocess.call('cls', shell = True)

clear()
print(Fore.BLACK + Back.WHITE + '------------------------------URL WATCHER---------------------------')
color_reset()
print('URL to monitor         ->', end = ' ')
url = input()
url = 'https://' +  url
print('Frequency (in seconds) ->', end = ' ')
intensity = int(input())
print('Want sound ? (y/n)     ->', end = ' ')
sound_choice = input()

try:
    my_request = requests.get(url)
except SSLError :
    print(Fore.RED + '\n [-] ERROR - SSL verification failed')
    winsound.Beep(2500,300)
    winsound.Beep(1000,500)
    color_reset()
    print(' [-] Exiting...')
    sys.exit()
except ConnectionError:
    print(Fore.RED + '\n [-] ERROR - No internet connection')
    winsound.Beep(1300,500)
    color_reset()
    print(' [-] Exiting...')
    sys.exit()

print('\nStarting monitoring process...')
time.sleep(intensity)

try:

    while True:
        time.sleep(intensity)

        if my_request.status_code == 200:
            init()
            color_reset()
            seconds = time.time()
            print(' [+] At ' + time.ctime(seconds), end = ' | ')
            print(Fore.YELLOW + 'Reply from ' + url, end = ' ')
            color_reset()
            print('| Status - ' + Fore.CYAN + str(my_request.status_code) + Fore.WHITE, end = ' | ')
            print(Fore.GREEN + 'Site is up')
            color_reset()
            
            if sound_choice == 'y':
                winsound.Beep(4000,200)
            else:
                continue

        else:
            print('Response failure')

            #plays the sound for failure
            winsound.Beep(1300,3000)
            y = 'MB_ICONEXCLAMATION'
            x = int(y)

except KeyboardInterrupt:
    print('\nProgram halted by keyboard interuption\nExiting...')
        


#checks for import error and if not any persists, imports 4 built-in and 2 3rd party packages...
try:
    import winsound, requests, smtplib, time, subprocess, sys
    from requests.exceptions import SSLError, ConnectionError
    from colorama import Fore, Style, Back, init
except ImportError:
    print(" [-] One or more packages required to run this program are missing on this computer...")
    print(' [-] Exiting...')
    sys.exit()

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end = '')

def clear():
    subprocess.call('cls', shell = True)

#if ssl error is found, and user selects to go with simple http, this method is executed,
#which in turn calls the main_monitor_loop without setting the url as https...
def continue_without_encryption(url, intensity, sound_choice):
    url = url.replace('https://','http://')
    print('\n [!] Continuing without encryption...')
    main_monitor_loop(url, intensity, sound_choice)

#main loop
def main_monitor_loop(url, intensity, sound_choice):
    try:
        
        my_request = requests.get(url)

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
                print(Fore.RED + ' [!] Response failure | ' + Fore.WHITE + 'Status - ' + Fore.RED + str(my_request.status_code))
                color_reset()

                #plays the sound for failure
                winsound.Beep(1300,3000)

                #mail sending process, calls send_mail method
                send_mail('dudhbiscuit@gmail.com','bhagalpur','sonumsvr@gmail.com', url, my_request.status_code)
                break

    except KeyboardInterrupt:
        print('\n [-] Program halted by keyboard interuption\n [-] Exiting...')

def send_mail(senderid, senderpswd, recieverid, url, status_code):
    print(Fore.YELLOW + ' [+] Sending alert e-mail to ' + senderid)
    color_reset()
    subject = 'CRITICAL SITE FAILURE'
    message = 'Warning, ' + url + 'failed to respond...\nError code - ' + status_code
    message = "Subject: " + subject +'\n' + message
    #smtp object definition part
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.ehlo()
    connection.starttls()
    connection.login(senderid, senderpswd)
    connection.ehlo()
    connection.sendmail(senderid,recieverid, message + '\n\n\n\n sent via URLWatcher')
    print(' [+] Mail sent...')
    connection.close()


clear()
print(Fore.BLACK + Back.WHITE + '------------------------------PORTAL MONITOR---------------------------')
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
    print(' [+] Do you want to continue (y/n) ', end = ' ')
    http_choice = input()
    
    if http_choice == 'y' or 'Y':
        continue_without_encryption(url, intensity, sound_choice)
    else:
        print(' [-] Exiting...')
        sys.exit()

except ConnectionError:
    print(Fore.RED + '\n [-] ERROR - No internet connection')
    winsound.Beep(1300,500)
    color_reset()
    print(' [-] Exiting...')
    sys.exit()

print('\n Starting monitoring process...\n')
time.sleep(intensity)
print(' |         Time/Date             |        Source                 |     Status   | Site Status |')

try:

    i = 1
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
    print('\n [-] Program halted by keyboard interruption\n [-] Exiting...')
        


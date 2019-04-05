#checks for import error and if not any persists, imports 4 built-in and 2 3rd party packages...
#!/usr/bin/env python3
try:
    import winsound, requests, smtplib, time, subprocess, sys, os
    from requests.exceptions import SSLError, ConnectionError, ConnectTimeout, InvalidURL
    from colorama import Fore, Style, Back, init
except ImportError:
    print(" [-] One or more packages required to run this program are missing on this computer...")
    print(' [-] Exiting...')
    sys.exit()

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end = '')

def clear():
    if os.name == 'nt':
        subprocess.call('cls', shell = True)
    elif os.name == 'posix':
        subprocess.call('clear', shell = True)
    else:
        subprocess.call('clear', shell = True)

def restart_self():
    subprocess.call('python site_monitor.py', shell = True)

def continue_without_encryption(url, intensity, sound_choice):
    url = url.replace('https://','http://')
    my_request = requests.get(url)
    status = str(my_request.status_code)
    print(' [!] Continuing without encryption...')
    winsound.PlaySound('step_sound.wav', winsound.SND_FILENAME)
    main_monitor_loop(url, intensity, sound_choice, status)

#main loop
def main_monitor_loop(url, intensity, sound_choice, status):
    print('\n [+] Starting monitoring process...\n')
    winsound.PlaySound('step_sound.wav', winsound.SND_FILENAME)
    time.sleep(1)

    try:
        
        #my_request = requests.get(url)

        while True:
            time.sleep(intensity)

            if status == '200':
                init()
                color_reset()
                seconds = time.time()
                print(' [+] At ' + time.ctime(seconds), end = ' | ')
                print(Fore.YELLOW + 'Reply from ' + url, end = ' ')
                color_reset()
                print('| Status - ' + Fore.CYAN + str(my_request.status_code) + Fore.WHITE, end = ' | ')
                print(Fore.GREEN + 'NORMAL')
                color_reset()
                
                if sound_choice == '-s' or '-S':
                    winsound.PlaySound('step_sound.wav', winsound.SND_FILENAME)
                else:
                    continue

            else:
                print(Fore.RED + ' [!] Response failure | ' + Fore.WHITE + 'Status - ' + Fore.RED + status)
                color_reset()

                #plays the sound for failure
                winsound.Beep(1300,3000)

                #mail sending process, calls send_mail method
                send_mail('dudhbiscuit@gmail.com','bhagalpur','sonumsvr@gmail.com', url, status)
                print(' [+] Attempting automatic reboot in 10 seconds...')
                time.sleep(10)
                restart_self()


    except KeyboardInterrupt:
        if sound_choice == '-s' or '-S':
            winsound.PlaySound('startup_sound.wav', winsound.SND_FILENAME)
        print('\n [-] Program halted by keyboard interruption (^C)\n [-] Exiting...\n [-] Developed by MSVR - github.com/itsmsvr/urlwatcher')
        sys.exit()

def send_mail(senderid, senderpswd, recieverid, url, status_code):
    try:
        print(Fore.YELLOW + ' [+] Sending alert e-mail to ' + recieverid)
        color_reset()
        subject = 'CRITICAL SITE FAILURE'
        message = 'Warning,' + url + 'failed to respond...\nError code - ' + str(status_code)
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
    except KeyboardInterrupt:
        if sound_choice == '-s' or '-S':
            winsound.PlaySound('startup_sound.wav', winsound.SND_FILENAME)
        print('\n [-] Program halted by keyboard interruption (^C)\n [-] Exiting...\n [-] Developed by MSVR - github.com/itsmsvr/urlwatcher')
        sys.exit()


################################ MAIN EXECUTION BEGINS HERE #####################################

#the beginning process of input
try:
    url           = str(sys.argv[1])
    url = 'https://' +  url
    intensity     = int(sys.argv[2])
    sound_choice  = str(sys.argv[3])
    automation    = str(sys.argv[4])

except IndexError:
    print(' One or more arguments provided are either missing or out of order...')
    sys.exit()
try:
    clear()
    print(Fore.BLACK + Back.WHITE + '------------------------------PORTAL MONITOR---------------------------')
    color_reset()
    #print(url)
    #print(' [~] URL to monitor         ->', end = ' ')
    winsound.PlaySound('startup_sound.wav', winsound.SND_FILENAME)
    print('\n >>> Monitoring - ' + url + '\n >>> Frequency  - ' + str(intensity) + ' seconds', end = '\t\t\t')
    if automation == '-a':
        print(' >>> Mode - Automatic')
    else:
        print(' >>> Mode - Manual')

except KeyboardInterrupt:
    print('\n [-] Program halted by keyboard interruption (^C)\n [-] Exiting...\n [-] Developed by MSVR - github.com/itsmsvr/urlwatcher')
    
#send request process that sends https request
try:
    my_request = requests.get(url)
    status = str(my_request.status_code)
except SSLError :
    print(Fore.RED + '\n [!] WARNING - SSL verification failed')
    winsound.Beep(2500,300)
    winsound.Beep(1000,500)
    color_reset()
    if automation == '-a' or '-A':
        continue_without_encryption(url, intensity, sound_choice)
    else:
        print(' [+] Do you want to continue (y/n) ', end = ' ')
        http_choice = input()

        if http_choice == '-s' or '-S':
            continue_without_encryption(url, intensity, sound_choice)
        else:
            print(' [-] Exiting...')
            sys.exit()
except InvalidURL:
    print(Fore.RED + ' [!] The URL you entered was invalid')
    color_reset()
except ConnectionError:
    print(Fore.RED + '\n [-] ERROR - No internet connection' + status)
    winsound.Beep(1300,500)
    color_reset()
    print(' [-] Exiting...')
    if automation == '-a' or '-A':
        restart_self()
    else:
        sys.exit()


#start the monitoring process
main_monitor_loop(url, intensity, sound_choice, status)


"""
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
print('\n [-] Program halted by keyboard interruption (^C)\n [-] Exiting...')
    """




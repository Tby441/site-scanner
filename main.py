import requests
import argparse
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True)
parser.add_argument("-c", "--cookies", required=False, action="store_true")
parser.add_argument("-sH", "--secHeaders", required=False, action="store_true")
parser.add_argument("-rT", "--reflectionTest", required=False, action="store_true")
args = parser.parse_args()

if args.url:
    try:
        get_url = args.url.strip()
        
        start = time.time()
        get_req = requests.get(get_url, timeout=10)
        end = time.time()

        response_time = round((end - start) * 1000, 2)

        get_headers = get_req.headers

        print("[>] Website fetched")
        time.sleep(0.5)
        print(f"[⏱️] Response time: {response_time} ms")
        time.sleep(0.5)
        print(f"[>] Status: {get_req.status_code}")
        time.sleep(0.5)
        date = get_headers.get("Date")
        if date:
            print(f"[>] Get date: {date}")
            time.sleep(0.5)

        server = get_headers.get("Server")
        if server:
            print(f"[>] Server: {server}")
            time.sleep(0.5)

        content_type = get_headers.get("Content-Type")
        if content_type:
            print(f"[>] Content Type: {content_type}")
            time.sleep(0.5)
        
        if args.secHeaders:
            security_headers = [
                "X-Frame-Options",
                "Content-Security-Policy",
                "X-Content-Type-Options",
                "Strict-Transport-Security",
            ]

            for header in security_headers:
                if get_headers.get(header):
                    print(f"[+] Found security header: {header}")
                else:
                    print(f"[!] Missing security header: {header}")
                time.sleep(0.5)

        if args.cookies:
            cookies = get_req.cookies
            if cookies:
                for cookie in cookies:
                    print(f"[🍪] Found cookie: {cookie.name}")
                    time.sleep(0.5)
        
            if not cookies:
                print(f"[!] No cookies collected in the request")

        if args.reflectionTest:
            marker = "ssliRefelctionTest"

            parsed = urlparse(get_url)

            if parsed.query:
                params = parse_qs(parsed.query)

                for param in params:
                    params[param] = [marker]

                new_query = urlencode(params, doseq=True)

                test_url = urlunparse(parsed._replace(query=new_query))

                test_req = requests.get(test_url, timeout=10)

                if marker in test_req.text:
                    print("[🪞] Reflection detected in param(s) [POSSIBLE XSS/HTML INJECTION]")
                    print(f"  └── [>] Test URL: {test_url}")       

    except Exception as e:
        print(f"[*] Error fetching page: {e}")


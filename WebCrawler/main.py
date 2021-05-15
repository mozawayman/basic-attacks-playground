
import requests
import argparse as pars

def send_request(url):
    try:
        return requests.get("http://"+url, timeout=0.05)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.InvalidURL):
        pass

def read_WordList(file_path, base_url):
    test_list = []
    with open(file_path, "r") as wlist:
        for line in wlist:
            test_url = line.strip() + "." + base_url
            test_list.append(test_url)
        return test_list

def operation_menu():
    print("\t\tBasic Web Crawler\n")
    parse = pars.ArgumentParser()
    parse.add_argument("-t", "--target_url", dest="target_url", help="target url to scan")
    parse.add_argument("-sb", "--list_sub_domain", dest="target_sub_domains", help="List of words to test against the target")
    parse.add_argument("-d", "--directories", dest="list_dirs", help="List directories on subdomains")
    parse.add_argument("-l", "--links", dest="links_on_domains", help="links on target domain")
    options = parse.parse_args()
    if not options.target_url:
        parse.error("target_url")
    return options

def main():
    while True:
        operation_menu()

if __name__ == "__main__":
    main()


url = "google.com"
list = read_WordList("subdomains-wodlist.txt",url)
subs_processed = 0
subs_found = 0
for subdom in list:
    subs_processed += 1
    response = send_request(subdom)
    if response:
        subs_found += 1
        print("Found subdomain ---> " + subdom + " Found: " + str(subs_found))
print("Found: " + str(subs_found) + " SubDomains, out of " + str(subs_processed) +" tested")
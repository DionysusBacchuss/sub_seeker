import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import httpx


class RapidDns():
    def __init__(self): 
         self.Domain_list = []
    def fetch_rapiddns(self, domain):
        url = f"https://rapiddns.io/subdomain/{domain}?full=1"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url,headers=headers,timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for link in soup.find_all('td'):
            text = link.get_text(strip=True)
            self.Domain_list.append(text)
            Domain = []
            ip = []
        
        for data  in range(0, len(self.Domain_list), 4):
            Domain.append(self.Domain_list[data])
            ip.append(self.Domain_list[data+1])
            type_rec = self.Domain_list[data+2]
            
        seen = set()
        uninqe_domains = []
        for each_item in Domain :
            if each_item in seen:
                pass
            else:
                seen.add(each_item)
                uninqe_domains.append(each_item)
        
        uninqe_ips = []
        seen = set()
        for each_item in ip :
            if each_item in seen:
                pass
            else:
                seen.add(each_item)
                uninqe_ips.append(each_item)        

        up_domains = []
        for each_uninqe_domain in uninqe_domains: 
            try:
                with httpx.Client(timeout=10.0, follow_redirects=True) as httpx_request :
                    response = httpx_request.get('http://'+each_uninqe_domain)
                            
                    if response.status_code in range(200,310):
                        print(f"domain is up ==>{each_uninqe_domain}")
                        up_domains.append(each_uninqe_domain)
                    else:
                        response = httpx_request.get('https://'+each_uninqe_domain)
                        if response.status_code in range(200,310):  
                            print(f"domain is up ==>{each_uninqe_domain}")
                            up_domains.append(each_uninqe_domain)


            except (httpx.RequestError, httpx.ConnectTimeout, httpx.ReadTimeout) as error:
                print(str(error)+f"on ==> {each_uninqe_domain}")

        try : 
            ##### saving result into txt file #####
            dom_result = open(output, "a")
            for each_domain in up_domains : 
                dom_result.write(each_domain+'\n')
            print("finished result saving ")

            ##### saving ip into txt file #####
            ip_result = open(f"ip_"+output, "a")
            for each_ip in uninqe_ips :
                ip_result.write(each_ip+'\n')
            print("finished ip result saving ")
        except Exception as error : 
            print(error)

from main_file import Main
main_obj = Main()
domain = main_obj.return_args()[0]
output  = main_obj.return_args()[2]


obj = RapidDns()
data = obj.fetch_rapiddns(domain)


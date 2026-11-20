import requests
import argparse
import json
import httpx



class Crtsh():
    def __init__(self):
        self.Domain_list = []
        
    def fetch_crtsh(self,domain):
        
        
        url = f"https://crt.sh/json?q={domain}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Sec-Ch-Ua": "\"Not-A.Brand\";v=\"24\", \"Chromium\";v=\"146\"", 
            "Sec-Ch-Ua-Mobile": "?0", 
            "Sec-Ch-Ua-Platform": "\"Windows\"", 
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1", 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
            "Sec-Fetch-Site": "none", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-User": "?1", 
            "Sec-Fetch-Dest": "document", 
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i"
        }
        
        try:
            global domain_list
            request = requests.get(url, headers=headers, timeout=30)
            data_list = json.loads(request.text)
            domain_list = []
            for each_data in data_list : 
                domain_list.append(each_data['common_name'])

            seen = set()
            uninqe_domains = []

            for each_item in domain_list : 

                if each_item in seen:
                    pass
                else:
                    seen.add(each_item)
                    uninqe_domains.append(each_item)
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
                result = open(output, "a")
                for Each_data in up_domains : 
                    result.write(Each_data+'\n')
        
                print("finished result saving ")
            except Exception as error : 
                print(error)
            self.Domain_list = domain_list

        except Exception as error:
            print(error)
    


from  main_file import Main
main_obj = Main()
domain = main_obj.return_args()[0]
output  = main_obj.return_args()[2]


obj = Crtsh()
data = obj.fetch_crtsh(domain)




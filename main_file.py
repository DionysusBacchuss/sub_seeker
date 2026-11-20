import requests
import argparse
import json
import httpx
from tqdm import tqdm



class Main(): 
    def __init__(self):
        parser = argparse.ArgumentParser(description="Fetch and check subdomains from CRT.SH")

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-d", "--domain", help="Single domain to check")
        group.add_argument("-f", "--file", help="File containing domains (one per line)")

        parser.add_argument("-o", "--output", required=True, help="Output file")

        try:
            args = parser.parse_args()
        except SystemExit:
            print("[ERROR] Missing required arguments. Use -h for help.")
            exit(1)

        self.domain = args.domain
        self.file = args.file
        self.output = args.output
        if args.file:
            try:
                with open(args.file, "r") as f:
                    domains = [line.strip() for line in f if line.strip()] 
            except FileNotFoundError:
                print(f"[ERROR] File not found: {args.file}")
                exit(1)
            except Exception as e:
                print(f"[ERROR] Reading file error: {e}")
                exit(1)

        else:
            domains = [args.domain]


    def return_args(self):
        return self.domain , self.file , self.output

obj = Main()

from crt_sh import Crtsh
from Rapiddns import RapidDns

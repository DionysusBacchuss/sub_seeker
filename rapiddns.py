import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_subdomains(domain):
    url = f"https://rapiddns.io/subdomain/{domain}?full=1"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    subdomains = set()

    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)

        if domain in text:
            subdomains.add(text)

    return sorted(subdomains)


def main():
    parser = argparse.ArgumentParser(
        description="Collect subdomains from RapidDNS"
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain, example.com"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="subdomains.txt",
        help="Output TXT file"
    )

    args = parser.parse_args()

    try:
        subdomains = get_subdomains(args.domain)

        with open(args.output, "a", encoding="utf-8") as f:
            for subdomain in subdomains:
                f.write(subdomain + "\n")

        print(f"[+] Found: {len(subdomains)} subdomains")
        print(f"[+] Saved to: {args.output}")

    except requests.RequestException as e:
        print(f"[-] Request error: {e}")


if __name__ == "__main__":
    main()
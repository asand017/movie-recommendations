import requests
from bs4 import BeautifulSoup

def fetch_free_proxies():
    url = 'https://www.free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    
    for row in soup.find('table').find_all('tr')[1:]:
        cols = row.find_all('td')
        if cols[4].text == 'elite proxy' and cols[6].text == 'yes':
            proxy = f"{cols[0].text}:{cols[1].text}"
            proxies.append(proxy)
    
    return proxies

# Fetch proxies and print them
proxies = fetch_free_proxies()
print(proxies)
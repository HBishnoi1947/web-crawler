import csv
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
import urllib.parse
from my_api_key import my_key


def update_csv(data):
    with open(r'E:\Internship Task\data.csv', 'a',  newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    f.close()


def strin_to_url(query, num, pagenumber):
    base_url = "https://www.google.com/search?"
    query_params = {"q": query, "num": num, "start": (pagenumber - 1) * num}
    encoded_params = urllib.parse.urlencode(query_params)
    url = base_url + encoded_params
    return url



def youtubeLinks(query, num_results):
    print("harsh: Started execution")
    client = ScrapingBeeClient(api_key=my_key)
    results_count = 0
    page = 1

    params = {
            "custom_google": True
    }
    while results_count < num_results:
        ans= []
        try:
            response = client.get(strin_to_url(query,10,page), params=params)
            response.raise_for_status()
            print("harsh: next 10 links fetched, page: ",page)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.select("div.g")
            for index, result in enumerate(results, 1):
                link = result.select_one("a[href]")["href"]
                link = str(link)
                # print(link)
                if 'www.youtube.com' in str(link):
                    ans.append([(results_count + index),link])
                
            results_count +=10
            page+=1
            update_csv(ans)
            if results_count >= num_results:
                return
            
                
        except:
            print("harsh: error")
            return




query = "site:youtube.com openinapp.co"
num_results = 10000
# ans = []
youtubeLinks(query, num_results)
print("harsh: Execution complete")
print("harsh: Data.csv file updated")
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_external_links_within_time_period(domain, start_date, end_date):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    end_date = datetime.strptime(end_date, "%d-%m-%Y")
    
    # Set up the web crawler
    base_url = "https://www.google.com/search?q=site:{}+{}&start={}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = []
    found_urls = set()
    
    # Crawl the web to find all pages that link to the domain
    for i in range(0, 100, 10):
        url = base_url.format(domain, "link", i)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        for link in soup.find_all('a'):
            url = link.get('href')
            if "http" in url and domain not in url and url not in found_urls:
                urls.append(url)
                found_urls.add(url)
    
    # Filter out internal links and save external links in a list
    external_links = []
    for url in urls:
        if domain not in url:
            external_links.append(url)
    
    # Check the last modified date of each external link to see if it falls within the specified time period
    links_within_time_period = []
    for link in external_links:
        res = requests.get(link, headers=headers)
        last_modified = res.headers.get('last-modified')
        if last_modified:
            last_modified = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
            if last_modified >= start_date and last_modified <= end_date:
                links_within_time_period.append(link)
    
    return links_within_time_period

# Call the function for https://fairgocasinoaus.com/ and the time period 01-04-2023 to 05-04-2023
start_date = "01-04-2023"
end_date = "05-04-2023"
domain = "fairgocasinoaus.com"
links_within_time_period = get_external_links_within_time_period(domain, start_date, end_date)

# Print the list of external links within the specified time period
print(links_within_time_period)

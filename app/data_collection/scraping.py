import requests
from bs4 import BeautifulSoup


def get_top_attractions_info(url):

    # Send a GET request to the TripAdvisor URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        print(soup.h1)
    else:
        print(f"Failed to fetch TripAdvisor page. Status code: {response.status_code}")
        return None


get_top_attractions_info("https://www.netflix.com/helloworld")

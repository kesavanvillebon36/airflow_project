import requests
import json

def main():
    URL = f'https://billboard-api2.p.rapidapi.com/hot-100?date=2019-05-11&range=1-10'
    headers = {
        "x-rapidapi-host": "billboard-api2.p.rapidapi.com"
    }

    page = requests.get(URL, headers=headers )
    print(page.status_code)


if __name__ == "__main__":
   main()
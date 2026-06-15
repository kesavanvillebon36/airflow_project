
#https://public-api.meteofrance.fr/public/DPObs/v1

# Import Module
import requests
import json
import datetime
import os
from dotenv import dotenv_values
import pathlib
from airflow.sdk import Variable

"""
    Get Bearer Token
"""


client_id = Variable.get("client_id_spotify")
client_secret =  Variable.get("client_secret_spotify")


def get_token():
    data = {
            "grant_type": "client_credentials",
            "client_id": f"{client_id}",
            "client_secret": f"{client_secret}"
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=data)
    answer = response.json()
    token_bearer = answer['access_token']
    return token_bearer

def request_page_top_tracks(URL, token_bearer): 
    headers = {
        "Authorization": f"Bearer {token_bearer}",
        "Accept": "application/json"
    }
    return requests.get(URL, headers=headers )

def json_formatted_file(page):
    #print(my_json)
    #print('- ' * 20)
    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(page.content)
    return json.dumps(data, indent=4, sort_keys=True)


def fetch_data():
    print(pathlib.Path(__file__).parent.resolve())
    token_bearer = get_token()
    dico_artists = {"Bad_Bunny": "4q3ewBCX7sLwd24euuV69X",
                    "Taylor_Swift" : "06HL4z0CvFAxyc27GXpf02",
                    "The_Weekend" : "1Xyo4u8uXC1ZmMpatF05PJ",
                    "Drake" : "3TVXtAsR1Inumwj472S9r4",
                    "Billie_Eilish" : "6qqNVTkY8uBg9cP3Jd7DAH",
                    "Kendrick_Lamar" : "2YZyLoL8N0Wb9xBt1NhZWg",
                    "Bruno_Mars" : "0du5cEVh5yTK9QJze8zA0C",
                    "Ariana_Grande" : "66CXWjxzNUsdJxJ2JdwvnR",
                    "Arijit_Singh" : "4YRxDV8wJFPHPTeXepOstw",
                    "Fuerza_Regida" : "0ys2OFYzWYB5hRDLCsBqxt",
                    "Anirudh_Ravichander" : "4zCH9qm4R2DADamUHMCa6O",
                    "Sabrina_Carpenter" : "74KM79TiuVKeVCqs8QtB0B",
                    "Kendrick_Lamar" : "2YZyLoL8N0Wb9xBt1NhZWg",
                    "HUNTRX" : "2yNNYQBChuox9A5Ka93BIn"
                    }
    print("Je commence l'écriture des top_tracks")
    for name, id in dico_artists.items():
        # Website URL
        URL = f'https://api.spotify.com/v1/artists/{id}/top-tracks?market=US'
        
        
        
        page = request_page_top_tracks(URL, token_bearer=token_bearer)
        # Ajouter une exception en prenant en compte le page status, s'il vaut 200
        s = json_formatted_file(page)
        #print(s)
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        with open(f"/home/kesav/airflow_project/raw/spotify/artist/{current_date}_top_tracks_{name}.json", "w") as f:
            f.write(s)
        print(f"{name} FAIT")
"""
if __name__ == "__main__":
   fetch_data()
"""





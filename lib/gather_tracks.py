import pandas as pd
import json
import pyarrow as pa
import pyarrow.parquet as pq
import requests
import pendulum
import sys
import os
import re



def fetch_list_of_file():
    
    # On affiche le chemin
    print(os.getcwd())
    # On change le répertoire en cours
    os.chdir('/home/kesav/airflow_project/raw/spotify/artist')
    # On affiche le chemin pour vérifier le changement
    print(os.getcwd())
    # On crée une liste vide
    name_file_to_analyze = []
    # On récupère tous les fichiers qui contiennent 2026 dans le répertoire Spotify
    with os.scandir(".") as d:
        for e in d:
            if "2026-04-15" in e.name:
                name_file_to_analyze.append(e.name)
    return name_file_to_analyze




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

def gather_all_top_tracks(name_file_to_analyze):
    gather_tracks_2 = pd.DataFrame()
    for i in name_file_to_analyze:
        # On va lire le ficheir de l'artiste avec la date concernée
        f = pd.read_json(f'/home/kesav/airflow_project/raw/spotify/artist/{i}')
        # On normalise le fichier pour récupérer tout au format colonne
        tracks = pd.json_normalize(f.tracks)
        # On utilise le Regex pour sélectionner la partie spécifique de texte dont on a besoin (ie. nom de l'artiste)
        x = re.findall(r"s_(.+).json$", i)
        # On ajoute une colonne avec le nom de l'artiste
        tracks["artist.name"] = x[0]
        # On ajoute un colonne avec l'id de l'artiste
        tracks["artist.id"] = dico_artists[x[0]]
        # On sélectionne les colonnes dont on a besoin
        columns = ["artist.name", "artist.id", "id", "name", "popularity", "duration_ms"]
        # On concatène le dataframe dans notre dataframe principal
        gather_tracks_2 = pd.concat([gather_tracks_2, tracks[columns]])
    gather_tracks_2 = gather_tracks_2.reset_index(drop = True)
    gather_tracks_2.to_json("/home/kesav/airflow_project/raw/spotify/gather_tracks/top_tracks_spotify_transformed.json")

def write_gather_top_tracks():
    gather_tracks_2 = pd.read_json("/home/kesav/airflow_project/raw/spotify/gather_tracks/top_tracks_spotify_transformed.json")
    table = pa.Table.from_pandas(gather_tracks_2)
    pq.write_table(table, "/home/kesav/airflow_project/raw/spotify/gather_tracks/top_tracks_spotify.parquet")
    gather_tracks_2.to_json("/home/kesav/airflow_project/raw/spotify/gather_tracks/top_tracks_spotify.json")
    gather_tracks_2.to_csv("/home/kesav/airflow_project/raw/spotify/gather_tracks/top_tracks_spotify.csv", index=False)


def gather_tracks_spotify():
    list_of_file = fetch_list_of_file()
    gather_all_top_tracks(list_of_file)
    write_gather_top_tracks()


if __name__ == "__main__":
    gather_tracks_spotify()

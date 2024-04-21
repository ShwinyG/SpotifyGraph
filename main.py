import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx
from networkx.readwrite import json_graph

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id='d14e7c8a8068419ab464546864e7096a', client_secret='429835d6722f4b10ae78070ab4be4a69')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get related artists for a given artist
def get_related_artists(artist_id):
    related_artists = sp.artist_related_artists(artist_id)
    return [(artist['id'], artist['name']) for artist in related_artists['artists']]

# Function to build the graph
def build_artist_graph(seed_artist, max_depth=2):
    G = nx.Graph()
    seed_id = sp.search(q='artist:' + seed_artist, type='artist')['artists']['items'][0]['id']
    seed_name = sp.search(q='artist:' + seed_artist, type='artist')['artists']['items'][0]['name']
    G.add_node(seed_id, name=seed_name)
    explore_queue = [(seed_id, 0)]  # Queue to explore related artists with depth
    while explore_queue:
        current_artist, depth = explore_queue.pop(0)
        if depth < max_depth:
            related_artists = get_related_artists(current_artist)
            for artist_id, artist_name in related_artists:
                G.add_node(artist_id, name=artist_name)
                G.add_edge(current_artist, artist_id)
                explore_queue.append((artist_id, depth + 1))
    return G

# Example usage
seed_artist_name = "Michael Jackson"
G = build_artist_graph(seed_artist_name)
nx.write_adjlist(G, "test.adjlist")

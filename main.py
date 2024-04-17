import os
import json
from typing import List, Dict

def get_json_files(dir: str, name: str) -> List[str]:
    return [f for f in os.listdir(dir) if name in f]


def get_top_track(file: str) -> Dict[str, int]:
    # Just use track uri for now

    top_track = None
    null = None
    with open(file, "r", encoding="utf-8") as json_file:
        tracks = json.load(json_file)

        for track in tracks:
            count = 0
            for count_track in tracks:
                if count_track.get("spotify_track_uri") == null:
                    continue
                if track.get("spotify_track_uri") == count_track.get("spotify_track_uri"):
                    count+=1

            if not top_track or count > top_track.get('plays'):
                top_track = {
                    "name": track.get("master_metadata_track_name"),
                    "album": track.get("master_metadata_album_album_name"),
                    "plays": count
                }
    
    return top_track


"""
    Get most played song of all time:

    IDEA
    for each json:
        for each track:
            new_json's = count occurrences of that track 
        
    for each new_json:
        for each track:
            overall_counts_json = add up the plays from each new_json    
    
    most_played_song = max_overall_counts_json

"""

def main():
    ext_history_dir = ".\\Spotify Extended Streaming History"
    json_name       = "Streaming_History_Audio"

    files = get_json_files(dir=ext_history_dir, name=json_name)
    
    # Get the top track and how many times they were played in each json
    top_tracks_per_json = []
    for file in files:
        file = os.path.join(ext_history_dir, file)
        top_track = get_top_track(file=file)
        top_tracks_per_json.append(top_track)
        print(f"Top track from {file}:\n{json.dumps(top_track, indent=3)}")

    print(top_tracks_per_json)
    winner = top_tracks_per_json[0]
    for t in top_tracks_per_json:
        if t.get("plays") > winner.get("plays"):
            winner = t
    
    print("Top track all time: ", json.dumps(winner, indent=3))   # This isn't my all time top track this is the track i've listened to most in one year

if __name__ == "__main__":
    main()
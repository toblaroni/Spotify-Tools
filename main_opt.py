import os
import json
from typing import List, Dict

def get_json_files(dir: str, name: str) -> List[str]:
    return [f for f in os.listdir(dir) if name in f]


def get_top_track(file: str) -> Dict[str, int]:
    # Just use track uri for now

    top_track = {}
    null = None
    with open(file, "r", encoding="utf-8") as json_file:
        tracks = json.load(json_file)
        total = len(tracks)

        for i, track in enumerate(tracks):
            content = f"Scanning track number {i} / {total}  |  Current top track = {top_track.get('name')}  |  Plays = {top_track.get('plays')}"
            padded_content = content.ljust(100)  # Adjust the width based on the maximum length of the printed content
            
            # Print the new content with carriage return to overwrite the previous line
            print(padded_content, end='\r', flush=True)

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


def combine_jsons(json_dir, files):

    # Combine all the json's into one big one
    new_json = []

    for file in files:
        file_path = os.path.join(json_dir, file)
        print("Adding", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            json_string = json.load(f)
            new_json.extend(json_string)
    
    with open(".\\combined_json.json", "w") as f:
        json.dump(new_json, f, indent=3)





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

    # combine_jsons(ext_history_dir, files)
    # return
    
    winner = get_top_track(".\\combined_json.json")
    
    print("Top track all time: ", json.dumps(winner, indent=3))   # This isn't my all time top track this is the track i've listened to most in one year

if __name__ == "__main__":
    main()
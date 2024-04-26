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


# Top song = When u came into my life - folamore
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



def how_many_songs(combined_json):
    song_ids = []

    null = None
    with open(combined_json, "r", encoding="utf-8") as f:
        json_string = json.load(f)

    for track in json_string:
        id = track.get("spotify_track_uri")
        if id == null:
            continue
        else:
            song_ids.append(id)

    return len(set(song_ids))

def total_listening_time(combined_json):
    total_played = 0

    null = None
    with open(combined_json, "r", encoding="utf-8") as f:
        json_string = json.load(f)

    for track in json_string:
        ms_played = track.get("ms_played")
        if ms_played == null:
            continue
        else:
            total_played += int(ms_played)

    return total_played

def ms_to_days_hours_minutes(milliseconds):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000

    # Calculate days, hours, and minutes
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return days, hours, minutes

def main():
    ext_history_dir = ".\\Spotify Extended Streaming History"
    json_name       = "Streaming_History_Audio"
    combined_jsons_path = ".\\combined_json.json"

    files = get_json_files(dir=ext_history_dir, name=json_name)

    # combine_jsons(ext_history_dir, files)
    # return
    
    # winner = get_top_track(".\\combined_json.json")
    total_time_ms = total_listening_time(combined_jsons_path)
    days, hours, minutes = ms_to_days_hours_minutes(total_time_ms)
    
    print("Total tracks listened to:", how_many_songs(combined_jsons_path))   
    print(f"Total listening time: {days} days, {hours} hours and {minutes} minutes.")   


if __name__ == "__main__":
    main()
import requests

def get_lyrics(title, artist, album, duration_ms):
    response = requests.get(
        "https://lrclib.net/api/get",
        params={
            "track_name":  title,
            "artist_name": artist,
            "album_name":  album,
            "duration":    duration_ms // 1000,
        }
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if not data.get("syncedLyrics"):
        return None

    return data["syncedLyrics"]

def parse_lrc(lrc_string):
    lines = []
    for line in lrc_string.strip().split("\n"):
        try:
            time_str = line[1:9]       
            text     = line[10:].strip() 
            
            parts    = time_str.split(":")
            minutes  = int(parts[0])
            seconds  = float(parts[1])
            ms       = int((minutes * 60 + seconds) * 1000)
            
            lines.append((ms, text))
        except:
            continue

    return lines

if __name__ == "__main__":
    lrc = get_lyrics("Learning to Fly", "Pink Floyd", "A Momentary Lapse of Reason", 291000)
    if lrc:
        lines = parse_lrc(lrc)
        for ms, text in lines:
            print(f"{ms}ms: {text}")
    else:
        print("Letra não encontrada")
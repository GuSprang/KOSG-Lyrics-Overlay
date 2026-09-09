import time
import threading
from overlay import LyricsOverlay
from lyrics import get_lyrics, parse_lrc
from spotify_client import create_client, get_current_track

import time
import ctypes

def boost_priority():
    ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, ABOVE_NORMAL_PRIORITY_CLASS)


def spotify_loop(sp, app):
    current_id = None
    lyrics_lines = []

    while True:
        fetch_time = time.time()
        track = get_current_track(sp)

        if track:
            app.set_track(track["artist"], track["title"])

            if track["id"] != current_id:
                current_id = track["id"]
                lrc = get_lyrics(
                    track["title"],
                    track["artist"],
                    track["album"],
                    track["duration"]
                )
                if lrc:
                    lyrics_lines = parse_lrc(lrc)
                    app.set_lyrics(lyrics_lines)
                else:
                    lyrics_lines = []
                    app.set_lyrics([(0, "Letra não encontrada")])

            if lyrics_lines:
                elapsed = (time.time() - fetch_time) * 1000
                progress = track["progress"] + elapsed + 600
                index = 0
                for i, (ms, _) in enumerate(lyrics_lines):
                    if ms <= progress:
                        index = i
                app.highlight_line(index)

        time.sleep(0.3)
def main():
    boost_priority()
    sp = create_client()
    app = LyricsOverlay(sp)

    thread = threading.Thread(target=spotify_loop, args=(sp, app), daemon=True)
    thread.start()

    app.run()


if __name__ == "__main__":
    main()
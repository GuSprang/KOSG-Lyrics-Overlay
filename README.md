# KOSG Lyrics Overlay

A lightweight desktop overlay that displays real-time synchronized lyrics for the track currently playing on Spotify, with playback controls (play/pause, previous, next). The window stays on top of every app, in a compact, borderless, always-visible panel.

🇧🇷 [Versão em português aqui](README.pt-br.md)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🎵 Detects the track currently playing on Spotify in real time
- 📝 Displays synchronized lyrics (fetched from [LRCLIB](https://lrclib.net))
- ⏯️ Playback controls: play/pause, next, previous
- 🖼️ Borderless, draggable, always-on-top overlay window
- 🎨 Custom rounded UI built with Tkinter + Pillow (antialiased shapes)

## How it works

1. Authenticates with the Spotify Web API (OAuth2) via [spotipy](https://github.com/spotipy-dev/spotipy)
2. Polls the currently playing track (title, artist, album, progress)
3. Fetches synced lyrics from LRCLIB using exact track metadata
4. Renders the lyrics on a floating overlay, highlighting the current line based on playback progress
5. Sends play/pause/skip commands back to Spotify through the Web API

## Requirements

- Python 3.10+
- A Spotify account (Free or Premium)
- A registered app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Installation

```bash
git clone https://github.com/GuSprang/KOSG-Lyrics-Overlay.git
cd KOSG-Lyrics-Overlay
pip install -r requirements.txt
```

### Spotify App Setup

1. Create an app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Add `http://127.0.0.1:8888/callback` as a Redirect URI in the app settings
3. Copy your **Client ID** and **Client Secret**

### Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Usage

```bash
python main.py
```

On first run, a browser window will open asking you to authorize the app with your Spotify account.

## Building an executable

```bash
python -m PyInstaller --onefile --windowed --name kosg main.py
```

The `.exe` will be generated inside the `dist/` folder. Remember to place your `.env` file in the same folder as the executable when distributing it.

> **Note:** Spotify apps start in *Development Mode*, which only allows pre-authorized accounts to log in. To let other people use your build, add their Spotify account email under **User Management** in your app's dashboard settings.

## Tech Stack

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — overlay UI
- [Pillow](https://python-pillow.org/) — antialiased rendering
- [spotipy](https://github.com/spotipy-dev/spotipy) — Spotify Web API wrapper
- [LRCLIB](https://lrclib.net) — synchronized lyrics database

## License

This project is licensed under the MIT License.

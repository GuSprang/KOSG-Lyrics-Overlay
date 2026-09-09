# KOSG Lyrics Overlay

Um overlay de desktop leve que exibe a letra sincronizada em tempo real da música que está tocando no Spotify, com controles de reprodução (play/pause, próxima, anterior). A janela fica sempre por cima de todos os apps, num painel compacto, sem bordas e sempre visível.

🇺🇸 [English version here](README.md)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Funcionalidades

- 🎵 Detecta em tempo real a música que está tocando no Spotify
- 📝 Exibe a letra sincronizada (buscada no [LRCLIB](https://lrclib.net))
- ⏯️ Controles de reprodução: play/pause, próxima, anterior
- 🖼️ Janela sem bordas, arrastável e sempre no topo
- 🎨 Interface arredondada personalizada, feita com Tkinter + Pillow (formas com antialiasing)

## Screenshots

<!-- Adicione aqui um print ou GIF do app -->

## Como funciona

1. Autentica com a Spotify Web API (OAuth2) via [spotipy](https://github.com/spotipy-dev/spotipy)
2. Consulta periodicamente a música atual (título, artista, álbum, progresso)
3. Busca a letra sincronizada no LRCLIB usando os metadados exatos da faixa
4. Exibe a letra no overlay flutuante, destacando a linha atual com base no progresso da reprodução
5. Envia comandos de play/pause/pular de volta ao Spotify pela Web API

## Requisitos

- Python 3.10+
- Uma conta Spotify (Free ou Premium)
- Um app registrado no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Instalação

```bash
git clone https://github.com/GuSprang/KOSG-Lyrics-Overlay.git
cd KOSG-Lyrics-Overlay
pip install -r requirements.txt
```

### Configurando o app no Spotify

1. Crie um app no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Adicione `http://127.0.0.1:8888/callback` como Redirect URI nas configurações do app
3. Copie seu **Client ID** e **Client Secret**

### Variáveis de ambiente

Copie o `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

```
SPOTIPY_CLIENT_ID=seu_client_id_aqui
SPOTIPY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Uso

```bash
python main.py
```

Na primeira execução, uma janela do navegador vai abrir pedindo autorização da sua conta Spotify.

## Gerando o executável

```bash
python -m PyInstaller --onefile --windowed --name kosg main.py
```

O `.exe` será gerado dentro da pasta `dist/`. Não esqueça de colocar o arquivo `.env` na mesma pasta do executável ao distribuí-lo.

> **Observação:** apps do Spotify nascem em *Modo de Desenvolvimento*, que só permite login de contas pré-autorizadas. Para que outras pessoas usem o seu executável, adicione o e-mail da conta Spotify delas em **User Management**, nas configurações do app no dashboard.

## Tecnologias

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — interface do overlay
- [Pillow](https://python-pillow.org/) — renderização com antialiasing
- [spotipy](https://github.com/spotipy-dev/spotipy) — wrapper da Spotify Web API
- [LRCLIB](https://lrclib.net) — banco de letras sincronizadas

## Licença

Este projeto está sob a licença MIT.

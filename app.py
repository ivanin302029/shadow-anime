from flask import Flask, render_template_string, request

app = Flask(__name__)

CATALOGUE_ANIMES = [
    {
        "id": 1, 
        "title": "Chainsaw Man", 
        "image": "https://placehold.co", 
        "player_url": "https://franime.fr/anime/chainsaw-man?s=1&lang=vf&anime_id=43806"
    },
    {
        "id": 2, 
        "title": "One Piece", 
        "image": "https://placehold.co", 
        "player_url": "https://onrender.com"
    },
    {
        "id": 3, 
        "title": "Naruto", 
        "image": "https://placehold.co", 
        "player_url": "https://onrender.com"
    }
]

HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow Anime — Catalogue</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 10px; font-weight: bold; letter-spacing: 2px;">SHADOW ANIME</h1>
    <p style="color: #a4b0be; margin-bottom: 30px; font-size: 14px;">Votre catalogue de streaming en ligne</p>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto; padding: 15px;">
        {% for anime in animes %}
        <a href="/video/{{ anime.id }}" style="text-decoration: none; color: white; background: #1e222b; padding: 12px; border-radius: 8px; width: 210px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
            <img src="{{ anime.image }}" style="width: 100%; border-radius: 6px;">
            <h3>{{ anime.title }}</h3>
        </a>
        {% endfor %}
    </div>
</body>
</html>
"""

HTML_PLAYER = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} — Shadow Anime</title>
    <style>
        html, body { background-color: #11141a !important; color: white !important; margin: 0; padding: 0; font-family: 'Arial', sans-serif; overflow-y: auto; min-height: 100vh; }
        .shadow-player { display: flex; justify-content: center; align-items: center; background: #1e222b; padding: 15px; border-radius: 8px; margin: 20px auto; width: 95%; max-width: 900px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .video-wrapper { width: 100%; aspect-ratio: 16 / 9; position: relative; border-radius: 4px; background: #000; overflow: hidden; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">&larr; Retour au catalogue</a>
        <h1 style="margin: 20px 0 5px 0; font-size: 32px;">{{ title }}</h1>
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 20px 0;">Shadow Player Original Réintégré</p>
        
        <section class="shadow-player">
            <div class="video-wrapper" id="player-target">
                <!-- L'iframe va être injectée ici de manière dynamique pour détruire le cache -->
            </div>
        </section>
    </div>

    <script>
        // Injection forcée du lien réel de ton shdw-player au chargement de l'écran
        window.addEventListener('DOMContentLoaded', () => {
            const container = document.getElementById('player-target');
            const ifr = document.createElement('iframe');
            ifr.src = "https://shdw-player.onrender.com";
            ifr.width = "100%";
            ifr.height = "100%";
            ifr.frameBorder = "0";
            ifr.scrolling = "no";
            ifr.setAttribute('allowfullscreen', 'true');
            ifr.style.position = "absolute";
            ifr.style.top = "0";
            ifr.style.left = "0";
            ifr.style.width = "100%";
            ifr.style.height = "100%";
            ifr.style.border = "none";
            container.appendChild(ifr);
        });
    </script>
</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(HTML_ACCUEIL, animes=CATALOGUE_ANIMES)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    anime = next((a for a in CATALOGUE_ANIMES if a["id"] == anime_id), None)
    return render_template_string(HTML_PLAYER, title=anime["title"], player_url=anime["player_url"])

from flask import Flask, render_template_string, request

app = Flask(__name__)

# ==========================================================
# SÉCURITÉ CONTRE L'ÉCRAN BLANC : On autorise le chargement des Iframes
# ==========================================================
@app.after_request
def remove_security_headers(response):
    response.headers.remove('X-Frame-Options')
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://shadow-anime.onrender.com https://shdw-player.onrender.com;"
    return response

# BASE DE DONNÉES DU CATALOGUE
CATALOGUE_ANIMES = [
    {"id": 1, "title": "Chainsaw Man", "https://franime.fr/anime/chainsaw-man?s=1&lang=vf&anime_id=43806"},
    {"id": 2, "title": "One Piece", "https://franime.fr/anime/chainsaw-man?s=1&lang=vf&anime_id=43806"},
    {"id": 3, "title": "Naruto", "https://franime.fr/anime/chainsaw-man?s=1&lang=vf&anime_id=43806"}
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
            <div style="width: 100%; aspect-ratio: 2/3; overflow: hidden; border-radius: 6px; background-color: #000;">
                <img src="{{ anime.image }}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <h3 style="font-size: 15px; margin: 12px 0 0 0; text-align: left;">{{ anime.title }}</h3>
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
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">← Retour au catalogue</a>
        <h1 style="margin: 20px 0 5px 0; font-size: 32px;">{{ title }}</h1>
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 20px 0;">Shadow Player Original Réintégré</p>
        
        <!-- BLOC BRUT DE TON IFRAME MOT POUR MOT INCORPORÉ SANS TOUCHER À L'ADRESSE -->
        <div style="position: relative; width: 100%; max-width: 850px; margin: 0 auto; aspect-ratio: 16 / 9; background-color: #000; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
            <iframe 
                src="https://shadow-anime.onrender.com" 
                width="100%" 
                height="100%" 
                frameborder="0" 
                scrolling="true" 
                allowfullscreen="true"
                webkitallowfullscreen="true" 
                mozallowfullscreen="true"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
            </iframe>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(HTML_ACCUEIL, animes=CATALOGUE_ANIMES)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    anime = next((a for a in CATALOGUE_ANIMES if a["id"] == anime_id), None)
    titre_anime = anime["title"] if anime else "Épisode"
    return render_template_string(HTML_PLAYER, title=titre_anime)

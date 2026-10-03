from flask import Flask, render_template_string, request

app = Flask(__name__)

# BASE DE DONNÉES SHADOW ANIME
CATALOGUE_ANIMES = [
    {"id": 1, "title": "Naruto", "image": "https://placehold.co"},
    {"id": 2, "title": "Naruto Shippuden", "image": "https://placehold.co+SHIPPUDEN"},
    {"id": 3, "title": "Boruto: Naruto Next Generations", "image": "https://placehold.co"},
    {"id": 4, "title": "One Piece", "image": "https://placehold.co"},
    {"id": 5, "title": "Bleach", "image": "https://placehold.co"},
    {"id": 6, "title": "Chainsaw Man", "image": "https://placehold.co"},
    {"id": 7, "title": "Jujutsu Kaisen", "image": "https://placehold.co"},
    {"id": 8, "title": "Demon Slayer", "image": "https://placehold.co"},
    {"id": 9, "title": "Solo Leveling", "image": "https://placehold.co"}
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
    <p style="color: #a4b0be; margin-bottom: 30px; font-size: 14px;">Votre plateforme de streaming d'animes gratuite et illimitée</p>
    
    <form action="/" method="get" style="margin-bottom: 50px;">
        <input type="text" name="search" value="{{ recherche }}" placeholder="Rechercher un anime (ex: Naruto, One Piece)..." style="padding: 14px 25px; width: 400px; border-radius: 25px; border: none; background: #1e222b; color: white; outline: none; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <button type="submit" style="padding: 14px 30px; border-radius: 25px; border: none; background: #ff4757; color: white; font-weight: bold; cursor: pointer; margin-left: 10px; font-size: 16px;">Rechercher</button>
    </form>

    <h2 style="text-align: left; max-width: 1200px; margin: 0 auto 25px auto; padding-left: 15px; border-left: 5px solid #ff4757; font-size: 22px;">
        {% if recherche %}Résultats pour "{{ recherche }}"{% else %}🔥 Catalogue des Animes Populaires{% endif %}
    </h2>

    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto; padding: 15px;">
        {% for anime in animes %}
        <a href="/video/{{ anime.id }}" style="text-decoration: none; color: white; background: #1e222b; padding: 12px; border-radius: 8px; width: 210px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: space-between;">
            <div style="width: 100%; aspect-ratio: 2/3; overflow: hidden; border-radius: 6px; background-color: #000;">
                <img src="{{ anime.image }}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <h3 style="font-size: 15px; margin: 12px 0 0 0; text-align: left; height: 38px; overflow: hidden; line-height: 1.3;">{{ anime.title }}</h3>
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
        .shadow-player { display: flex; justify-content: center; align-items: center; background: #1e222b; padding: 15px; border-radius: 8px; margin: 20px auto; width: 95%; max-width: 850px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .video-wrapper { width: 100%; aspect-ratio: 16 / 9; position: relative; border-radius: 4px; background: #000; overflow: hidden; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">&larr; Retour au catalogue</a>
        <h1 style="margin: 20px 0 5px 0; font-size: 32px;">{{ title }}</h1>
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 20px 0;">Épisode 1 — SHADOW PLAYER</p>
        
        <!-- INTÉGRATION MOT POUR MOT DE TON CODE D'IFRAME COPIÉ AVEC L'ADRESSE OFFICIELLE NETTOYÉE -->
        <section class="shadow-player">
            <div class="video-wrapper">
                <iframe 
                    src="https://render.com" 
                    width="100%" 
                    height="100%" 
                    frameborder="0" 
                    scrolling="no" 
                    allowfullscreen="true"
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
                </iframe>
            </div>
        </section>
    </div>
</body>
</html>
"""

@app.route("/")
def accueil():
    mot_clef = request.args.get("search", "").strip().lower()
    if mot_clef:
        animes_a_afficher = [a for a in CATALOGUE_ANIMES if mot_clef in a["title"].lower()]
    else:
        animes_a_afficher = CATALOGUE_ANIMES
    return render_template_string(HTML_ACCUEIL, animes=animes_a_afficher, recherche=request.args.get("search", ""))

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    anime = next((a for a in CATALOGUE_ANIMES if a["id"] == anime_id), None)
    titre_anime = anime["title"] if anime else "Épisode"
    return render_template_string(HTML_PLAYER, title=titre_anime)

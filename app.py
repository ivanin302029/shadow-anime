import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Modèle de la page d'accueil avec une barre de recherche automatique
HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadow Anime — Catalogue Automatique</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 10px;">SHADOW ANIME</h1>
    <p style="color: #a4b0be; margin-bottom: 30px;">Recherche et streaming automatique (ANMX-Style)</p>
    
    <!-- Barre de recherche fonctionnelle -->
    <form action="/" method="get" style="margin-bottom: 40px;">
        <input type="text" name="search" placeholder="Rechercher un anime (ex: Naruto, One Piece)..." style="padding: 12px 20px; width: 350px; border-radius: 25px; border: none; background: #1e222b; color: white; outline: none; font-size: 16px;">
        <button type="submit" style="padding: 12px 25px; border-radius: 25px; border: none; background: #ff4757; color: white; font-weight: bold; cursor: pointer; margin-left: 10px;">Rechercher</button>
    </form>

    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto;">
        {% for anime in animes %}
        <a href="/video/{{ anime.id }}" style="text-decoration: none; color: white; background: #1e222b; padding: 15px; border-radius: 8px; width: 220px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
            <img src="{{ anime.image }}" style="width: 100%; border-radius: 6px; aspect-ratio: 2/3; object-fit: cover;">
            <h3 style="font-size: 16px; margin: 12px 0 5px 0; text-align: left; height: 40px; overflow: hidden;">{{ anime.title }}</h3>
        </a>
        {% else %}
        <p style="color: #a4b0be;">Entrez un nom d'anime pour lancer la recherche automatique !</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Modèle du lecteur universel autonome
HTML_PLAYER = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} — Shadow Anime</title>
    <style>
        html, body { background-color: #11141a !important; color: white !important; margin: 0; padding: 0; font-family: 'Arial', sans-serif; overflow-y: auto; min-height: 100vh; }
        .shadow-player { display: flex; justify-content: center; align-items: center; background: #1e222b; padding: 15px; border-radius: 8px; margin: 20px auto; width: 95%; max-width: 950px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .video-wrapper { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; position: relative; border-radius: 4px; background: #000; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">← Retour au catalogue</a>
        <h1 style="margin: 20px 0 5px 0; font-size: 32px;">{{ title }}</h1>
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 10px 0;">Shadow Player Indépendant</p>
        
        <section class="shadow-player">
            <div class="video-wrapper">
                <!-- Ton lecteur autonome connecté à un flux cloud mondial stable -->
                <video src="https://zencdn.net" controls autoplay muted width="100%" height="100%" style="display: block; background: #000; border: none; outline: none;"></video>
            </div>
        </section>
    </div>
</body>
</html>
"""

@app.route("/")
def accueil():
    mot_clef = request.args.get("search", "").strip()
    animes_trouves = []
    
    # Si l'utilisateur fait une recherche, on interroge une API publique d'animes
    if mot_clef:
        try:
            url = f"https://jikan.moe{mot_clef}&limit=10"
            reponse = requests.get(url, timeout=5).json()
            for item in reponse.get("data", []):
                animes_trouves.append({
                    "id": item["mal_id"],
                    "title": item["title_french"] if item.get("title_french") else item["title"],
                    "image": item["images"]["jpg"]["large_image_url"]
                })
        except Exception:
            # En cas de coupure de l'API, on met une liste de secours
            animes_trouves = [{"id": 1, "title": "Erreur de connexion API", "image": ""}]
            
    return render_template_string(HTML_ACCUEIL, animes=animes_trouves)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    # On récupère automatiquement les infos de l'anime cliqué via son ID unique
    titre_anime = "Épisode de Streaming"
    try:
        url = f"https://jikan.moe{anime_id}"
        item = requests.get(url, timeout=5).json().get("data", {})
        titre_anime = item["title_french"] if item.get("title_french") else item["title"]
    except Exception:
        pass

    return render_template_string(HTML_PLAYER, title=titre_anime)

if __name__ == "__main__":
    app.run(debug=True)

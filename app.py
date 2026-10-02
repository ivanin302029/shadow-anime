import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Modèle de la page d'accueil avec catalogue automatique géant (Style Anime-Sama / FRanime)
HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow Anime — Votre Catalogue Streaming</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    
    <!-- NAVBAR / HEADER -->
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 10px; font-weight: bold; letter-spacing: 2px;">SHADOW ANIME</h1>
    <p style="color: #a4b0be; margin-bottom: 30px; font-size: 14px;">Votre plateforme de streaming d'animes gratuite et illimitée</p>
    
    <!-- BARRE DE RECHERCHE -->
    <form action="/" method="get" style="margin-bottom: 50px;">
        <input type="text" name="search" value="{{ recherche }}" placeholder="Rechercher un anime (ex: One Piece, Naruto, Jujutsu)..." style="padding: 14px 25px; width: 400px; border-radius: 25px; border: none; background: #1e222b; color: white; outline: none; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <button type="submit" style="padding: 14px 30px; border-radius: 25px; border: none; background: #ff4757; color: white; font-weight: bold; cursor: pointer; margin-left: 10px; font-size: 16px; transition: 0.2s; box-shadow: 0 4px 10px rgba(255,71,87,0.3);">Rechercher</button>
    </form>

    <!-- TITRE DE LA SECTION DYNAMIQUE -->
    <h2 style="text-align: left; max-width: 1200px; margin: 0 auto 25px auto; padding-left: 15px; border-left: 5px solid #ff4757; font-size: 22px;">
        {% if recherche %}Résultats de recherche pour "{{ recherche }}"{% else %}🔥 Animes Populaires du Moment{% endif %}
    </h2>

    <!-- GRILLE DU CATALOGUE AUTOMATIQUE -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto; padding: 15px;">
        {% for anime in animes %}
        <a href="/video/{{ anime.id }}" style="text-decoration: none; color: white; background: #1e222b; padding: 12px; border-radius: 8px; width: 210px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: space-between;">
            <div style="width: 100%; aspect-ratio: 2/3; overflow: hidden; border-radius: 6px;">
                <img src="{{ anime.image }}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <h3 style="font-size: 15px; margin: 12px 0 0 0; text-align: left; height: 38px; overflow: hidden; line-height: 1.3;">{{ anime.title }}</h3>
        </a>
        {% else %}
        <p style="color: #a4b0be; margin-top: 20px;">Aucun anime trouvé. Réessayez avec un autre mot-clef !</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Modèle du Shadow Player avec lecteur universel incassable (Zéro écran noir)
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
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 15px 0;">Épisode 1 — Lecteur Universel Sécurisé</p>
        
        <section class="shadow-player">
            <div class="video-wrapper">
                <!-- Flux vidéo universel ultra-fluide qui ne coupe jamais en local ni sur Render -->
                <video src="https://googleapis.com" controls autoplay muted width="100%" height="100%" style="display: block; background: #000; border: none; outline: none;"></video>
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
    
    if mot_clef:
        # Action de recherche initiée par l'utilisateur
        try:
            url = f"https://jikan.moe{mot_clef}&limit=24"
            reponse = requests.get(url, timeout=5).json()
            for item in reponse.get("data", []):
                animes_trouves.append({
                    "id": item["mal_id"],
                    "title": item["title_french"] if item.get("title_french") else item["title"],
                    "image": item["images"]["jpg"]["large_image_url"]
                })
        except Exception:
            pass
    else:
        # AU CHARGEMENT INITIAL : On affiche le top 24 des meilleurs animes mondiaux automatiquement !
        try:
            url = "https://jikan.moe"
            reponse = requests.get(url, timeout=5).json()
            for item in reponse.get("data", []):
                animes_trouves.append({
                    "id": item["mal_id"],
                    "title": item["title_french"] if item.get("title_french") else item["title"],
                    "image": item["images"]["jpg"]["large_image_url"]
                })
        except Exception:
            pass
            
    return render_template_string(HTML_ACCUEIL, animes=animes_trouves, recherche=mot_clef)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    titre_anime = "Épisode de Visionnage"
    try:
        url = f"https://jikan.moe{anime_id}"
        item = requests.get(url, timeout=5).json().get("data", {})
        titre_anime = item["title_french"] if item.get("title_french") else item["title"]
    except Exception:
        pass

    return render_template_string(HTML_PLAYER, title=titre_anime)

if __name__ == "__main__":
    app.run(debug=True)

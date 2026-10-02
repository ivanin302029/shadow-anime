import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Modèle HTML de l'accueil (Style Anime-Sama / FRanime / 9anime)
HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow Anime — Catalogue Automatique</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 10px; font-weight: bold; letter-spacing: 2px;">SHADOW ANIME</h1>
    <p style="color: #a4b0be; margin-bottom: 30px; font-size: 14px;">Votre plateforme de streaming d'animes gratuite et illimitée</p>
    
    <!-- BARRE DE RECHERCHE CONNECTÉE À DES MILLIERS D'ANIMES -->
    <form action="/" method="get" style="margin-bottom: 50px;">
        <input type="text" name="search" value="{{ recherche }}" placeholder="Rechercher parmi des milliers d'animes (ex: Naruto, One Piece)..." style="padding: 14px 25px; width: 400px; border-radius: 25px; border: none; background: #1e222b; color: white; outline: none; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <button type="submit" style="padding: 14px 30px; border-radius: 25px; border: none; background: #ff4757; color: white; font-weight: bold; cursor: pointer; margin-left: 10px; font-size: 16px;">Rechercher</button>
    </form>

    <h2 style="text-align: left; max-width: 1200px; margin: 0 auto 25px auto; padding-left: 15px; border-left: 5px solid #ff4757; font-size: 22px;">
        {% if recherche %}Résultats pour "{{ recherche }}"{% else %}🔥 Animes Populaires Tendances{% endif %}
    </h2>

    <!-- GRILLE D'AFFICHAGE GÉANTE -->
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

# Modèle du lecteur en Iframe universel fluide (Zéro écran noir de 0:00)
HTML_PLAYER = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadow Player</title>
    <style>
        html, body { background-color: #11141a !important; color: white !important; margin: 0; padding: 0; font-family: 'Arial', sans-serif; overflow-y: auto; min-height: 100vh; }
        .shadow-player { display: flex; justify-content: center; align-items: center; background: #1e222b; padding: 15px; border-radius: 8px; margin: 20px auto; width: 95%; max-width: 950px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .video-wrapper { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; position: relative; border-radius: 4px; background: #000; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">← Retour au catalogue</a>
        <h1 style="margin: 20px 0 15px 0; font-size: 32px;">Lecteur de Streaming</h1>
        
        <section class="shadow-player">
            <div class="video-wrapper">
                <!-- Iframe d'intégration propre compatible avec Render pour charger la vidéo instantanément -->
                <iframe 
                    src="https://youtube.com" 
                    scrolling="no" 
                    frameborder="0" 
                    width="100%" 
                    height="100%" 
                    allowfullscreen="true" 
                    allow="autoplay; fullscreen"
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
    mot_clef = request.args.get("search", "").strip()
    animes_trouves = []
    
    url_anilist = "https://anilist.co"
    
    # Correction de la syntaxe de la requête GraphQL pour éviter les conflits d'échappement Python
    if mot_clef:
        query = """
        query ($search: String) {
          Page(page: 1, perPage: 24) {
            media(search: $search, type: ANIME) {
              id
              title { romaji english }
              coverImage { large }
            }
          }
        }
        """
        variables = {'search': mot_clef}
    else:
        query = """
        query {
          Page(page: 1, perPage: 24) {
            media(sort: POPULARITY_DESC, type: ANIME) {
              id
              title { romaji english }
              coverImage { large }
            }
          }
        }
        """
        variables = {}

    try:
        reponse = requests.post(url_anilist, json={'query': query, 'variables': variables}, timeout=5).json()
        elements = reponse.get("data", {}).get("Page", {}).get("media", [])
        for item in elements:
            titre = item["title"]["english"] if item["title"].get("english") else item["title"]["romaji"]
            animes_trouves.append({
                "id": item["id"],
                "title": titre,
                "image": item["coverImage"]["large"]
            })
    except Exception:
        pass
        
    return render_template_string(HTML_ACCUEIL, animes=animes_trouves, recherche=mot_clef)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    return render_template_string(HTML_PLAYER)

if __name__ == "__main__":
    app.run(debug=True)

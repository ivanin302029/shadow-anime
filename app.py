from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.after_request
def remove_security_headers(response):
    response.headers.remove('X-Frame-Options')
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://onrender.com https://onrender.com;"
    return response

# CATALOGUE AVEC DE VRAIS LIENS VIDÉOS DE TEST HD (SANS YOUTUBE, SANS PUB)
CATALOGUE_ANIMES = [
    {
        "id": 1, 
        "title": "Chainsaw Man", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
    },
    {
        "id": 2, 
        "title": "One Piece", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
    },
    {
        "id": 3, 
        "title": "Naruto", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
    },
    {
        "id": 4, 
        "title": "Solo Leveling", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
    },
    {
        "id": 5, 
        "title": "That Time I Got Reincarnated as a Slime", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
    },
    {
        "id": 6, 
        "title": "Re:Zero", 
        "image": "https://placehold.co",
        "video": "https://googleapis.com"
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
    <p style="color: #a4b0be; margin-bottom: 30px; font-size: 14px;">Votre catalogue de streaming d'animes en ligne</p>
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
        .shadow-player-wrapper { display: flex; justify-content: center; align-items: center; margin: 20px auto; width: 95%; max-width: 900px; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">&larr; Retour au catalogue</a>
        <h1 style="margin: 20px 0 25px 0; font-size: 32px;">{{ title }}</h1>
        
        <div class="shadow-player-wrapper">
            <!-- Envoi du lien vidéo au lecteur via le paramètre ?play= -->
            <iframe 
                src="https://shadow-anime.onrender.com" play={{ video_url }}" 
                width="100%" 
                height="650px; border: none; overflow: hidden;">
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
    return render_template_string(HTML_PLAYER, title=anime["title"], video_url=anime["video"])

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.after_request
def remove_security_headers(response):
    response.headers.remove('X-Frame-Options')
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://shadow-anime.onrender.com https://shdw-player.onrender.com;"
    return response

# REPERTOIRE AVEC DE VRAIS FLUX DE LECTURE STABLES INTERNATIONAUX
CATALOGUE_ANIMES = [
    {"id": 1, "title": "Chainsaw Man", "image": "https://placehold.co", "video": "https://unified-streaming.com"},
    {"id": 2, "title": "One Piece", "image": "https://placehold.co", "video": "https://unified-streaming.com"},
    {"id": 3, "title": "Naruto", "image": "https://placehold.co", "video": "https://unified-streaming.com"}
]

HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow Anime</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 30px;">SHADOW ANIME</h1>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto;">
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
        html, body { background-color: #11141a !important; margin: 0; padding: 0; font-family: 'Arial', sans-serif; }
        .shadow-player { position: relative; width: 100%; max-width: 850px; margin: 20px auto; aspect-ratio: 16 / 9; background-color: #000; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold;">&larr; Retour au catalogue</a>
        <h1 style="color: white; margin: 20px 0;">{{ title }}</h1>
        <div class="shadow-player">
            <!-- APPEL DIRECT DU LECTEUR UNIQUE DE MANIÈRE DYNAMIQUE -->
            <iframe 
                src="https://onrender.com{{ video_url }}" 
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
    return render_template_string(HTML_PLAYER, title=anime["title"], video_url=anime["video"])

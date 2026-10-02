from flask import Flask, render_template_string

app = Flask(__name__)

CATALOGUE_ANIMES = [
    {"id": 1, "titre": "Chainsaw Man", "image": "https://unsplash.com", "episode_numero": "1", "lien": "https://franime.fr"},
    {"id": 2, "titre": "One Piece", "image": "https://unsplash.com", "episode_numero": "1100", "lien": "https://franime.fr"},
    {"id": 3, "titre": "Naruto", "image": "https://unsplash.com", "episode_numero": "1", "lien": "https://franime.fr"},
    {"id": 4, "titre": "Solo Leveling", "image": "https://unsplash.com", "episode_numero": "1", "lien": "https://franime.fr"},
    {"id": 5, "titre": "That Time I Got Reincarnated as a Slime", "image": "https://unsplash.com", "episode_numero": "1", "lien": "https://franime.fr"},
    {"id": 6, "titre": "Re:Zero", "image": "https://unsplash.com", "episode_numero": "1", "lien": "https://franime.fr"}
]

# Modèle de la page d'accueil sombre
HTML_ACCUEIL = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadow Anime</title>
</head>
<body style="background-color: #11141a; color: white; font-family: Arial, sans-serif; text-align: center; padding: 40px; margin: 0;">
    <h1 style="color: #ff4757; font-size: 42px; margin-bottom: 30px;">SHADOW ANIME</h1>
    <p style="color: #a4b0be; margin-bottom: 40px;">Votre catalogue de streaming gratuit en ligne</p>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; max-width: 1200px; margin: 0 auto;">
        {% for anime in animes %}
        <a href="/video/{{ anime.id }}" style="text-decoration: none; color: white; background: #1e222b; padding: 15px; border-radius: 8px; width: 220px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); transition: transform 0.2s;">
            <img src="{{ anime.image }}" style="width: 100%; border-radius: 6px; aspect-ratio: 2/3; object-fit: cover;">
            <h3 style="font-size: 16px; margin: 12px 0 5px 0; text-align: left; height: 40px; overflow: hidden;">{{ anime.titre }}</h3>
        </a>
        {% endfor %}
    </div>
</body>
</html>
"""

# Modèle du grand Shadow Player avec roulette (scroll) active
HTML_PLAYER = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{{ anime.titre }} — Shadow Anime</title>
    <style>
        html, body { background-color: #11141a !important; color: white !important; margin: 0; padding: 0; font-family: 'Arial', sans-serif; overflow-y: auto; min-height: 100vh; }
        .shadow-player { display: flex; justify-content: center; align-items: center; background: #1e222b; padding: 15px; border-radius: 8px; margin: 20px auto; width: 95%; max-width: 950px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .video-wrapper { width: 100%; aspect-ratio: 16 / 9; overflow-y: auto !important; position: relative; border-radius: 4px; background: #000; }
        .video-wrapper::-webkit-scrollbar { width: 10px; }
        .video-wrapper::-webkit-scrollbar-track { background: #1e222b; }
        .video-wrapper::-webkit-scrollbar-thumb { background: #ff4757; border-radius: 5px; }
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center;">
        <a href="/" style="color: #ff4757; text-decoration: none; font-weight: bold; font-size: 16px;">← Retour au catalogue</a>
        <h1 style="margin: 20px 0 5px 0; font-size: 32px;">{{ anime.titre }}</h1>
        <p style="color: #1e90ff; font-weight: bold; margin: 0 0 10px 0;">Épisode {{ anime.episode_numero }}</p>
        
        <section class="shadow-player">
            <div class="video-wrapper">
                <iframe 
                    src="{{ lien_video }}" 
                    scrolling="yes" 
                    frameborder="0" 
                    width="100%" 
                    height="140%" 
                    sandbox="allow-scripts allow-same-origin allow-forms"
                    allowfullscreen="true" 
                    allow="autoplay; fullscreen"
                    style="width: 100%; height: 140%; border: none;">
                </iframe>
            </div>
        </section>
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
    if not anime:
        return "Anime introuvable", 404
    return render_template_string(HTML_PLAYER, anime=anime, lien_video=anime["lien"])

if __name__ == "__main__":
    app.run(debug=True)

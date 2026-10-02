from flask import Flask, render_template, request

app = Flask(__name__)

# Catalogue complet restauré avec la variable d'épisode pour corriger l'erreur 500
CATALOGUE_ANIMES = [
    {
        "id": 1,
        "titre": "Chainsaw Man",
        "image": "https://unsplash.com",
        "genres": ["Action", "Surnaturel", "Horreur"],
        "episode_numero": "1",
        "lien": "https://franime.fr"
    },
    {
        "id": 2,
        "titre": "One Piece",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Fantastique"],
        "episode_numero": "1100",
        "lien": "https://franime.fr"
    },
    {
        "id": 3,
        "titre": "Naruto",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Ninja"],
        "episode_numero": "1",
        "lien": "https://franime.fr"
    },
    {
        "id": 4,
        "titre": "Solo Leveling",
        "image": "https://unsplash.com",
        "genres": ["Action", "Fantasy", "Système"],
        "episode_numero": "1",
        "lien": "https://franime.fr"
    },
    {
        "id": 5,
        "titre": "That Time I Got Reincarnated as a Slime",
        "image": "https://unsplash.com",
        "genres": ["Isekai", "Fantasy", "Action"],
        "episode_numero": "1",
        "lien": "https://franime.fr"
    },
    {
        "id": 6,
        "titre": "Re:Zero",
        "image": "https://unsplash.com",
        "genres": ["Isekai", "Fantasy", "Drame"],
        "episode_numero": "1",
        "lien": "https://franime.fr"
    }
]

@app.route("/")
def accueil():
    return render_template("index.html", animes=CATALOGUE_ANIMES)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    anime = next((a for a in CATALOGUE_ANIMES if a["id"] == anime_id), None)
    if not anime:
        return "Anime introuvable", 404
    
    return render_template("player.html", anime=anime, lien_video=anime["lien"])

if __name__ == "__main__":
    app.run(debug=True)

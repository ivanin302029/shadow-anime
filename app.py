from flask import Flask, render_template, request

app = Flask(__name__)

# Catalogue officiel de ton site ://onrender.com
CATALOGUE_ANIMES = [
    {
        "id": 1,
        "titre": "Chainsaw Man",
        "image": "https://unsplash.com",
        "genres": ["Action", "Surnaturel", "Horreur"],
        "lien": "https://franime.fr"
    },
    {
        "id": 2,
        "titre": "One Piece",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Fantastique"],
        "lien": "https://franime.fr"
    },
    {
        "id": 3,
        "titre": "Naruto",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Ninja"],
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
    
    # Envoi direct du lien FRanime configuré sans aucun calcul complexe
    return render_template("player.html", anime=anime, lien_video=anime["lien"])

if __name__ == "__main__":
    app.run(debug=True)

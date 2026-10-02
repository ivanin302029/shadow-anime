from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================================
# CATALOGUE DE SHADOW-ANIME.FR (AVEC VRAIS VISUELS HD)
# ==========================================================
CATALOGUE_ANIMES = [
    {
        "id": 1,
        "titre": "Chainsaw Man",
        # Remplacement par de vrais posters officiels en haute résolution
        "image": "https://unsplash.com",
        "genres": ["Action", "Surnaturel", "Horreur"],
        "episodes": [
            {
                "numero": 1,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    },
    {
        "id": 2,
        "titre": "One Piece",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Fantastique"],
        "episodes": [
            {
                "numero": 1100,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    },
    {
        "id": 3,
        "titre": "Naruto",
        "image": "https://unsplash.com",
        "genres": ["Action", "Aventure", "Ninja"],
        "episodes": [
            {
                "numero": 1,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    },
    {
        "id": 4,
        "titre": "Solo Leveling",
        "image": "https://unsplash.com",
        "genres": ["Action", "Fantasy", "Système"],
        "episodes": [
            {
                "numero": 1,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    },
    {
        "id": 5,
        "titre": "That Time I Got Reincarnated as a Slime",
        "image": "https://unsplash.com",
        "genres": ["Isekai", "Fantasy", "Action"],
        "episodes": [
            {
                "numero": 1,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    },
    {
        "id": 6,
        "titre": "Re:Zero",
        "image": "https://unsplash.com",
        "genres": ["Isekai", "Fantasy", "Drame"],
        "episodes": [
            {
                "numero": 1,
                "langues": {
                    "VOSTFR": {
                        "Vidmoly": "https://franime.fr"
                    }
                }
            }
        ]
    }
]

@app.route("/")
def accueil():
    mot_clef = request.args.get("search", "").strip().lower()
    if mot_clef:
        animes_a_afficher = [anime for anime in CATALOGUE_ANIMES if mot_clef in anime["titre"].lower()]
    else:
        animes_a_afficher = CATALOGUE_ANIMES
    return render_template("index.html", animes=animes_a_afficher, recherche=mot_clef)

@app.route("/video/<int:anime_id>")
def regarder_video(anime_id):
    anime = next((a for a in CATALOGUE_ANIMES if a["id"] == anime_id), None)
    if not anime:
        return "Anime introuvable", 404
    
    ep_index = int(request.args.get("ep", 0))
    if ep_index >= len(anime["episodes"]) or ep_index < 0:
        ep_index = 0
    episode_actuel = anime["episodes"][ep_index]
    
    langues_disponibles = list(episode_actuel["langues"].keys())
    
    langue_choisie = request.args.get("langue", "")
    if not langue_choisie or langue_choisie not in episode_actuel["langues"]:
        langue_choisie = langues_disponibles[0] if langues_disponibles else ""
    
    serveurs_disponibles = episode_actuel["langues"].get(langue_choisie, {})
    liste_noms_serveurs = list(serveurs_disponibles.keys())
    
    serveur_choisi = request.args.get("serveur", "")
    if not serveur_choisi or serveur_choisi not in serveurs_disponibles:
        serveur_choisi = liste_noms_serveurs[0] if liste_noms_serveurs else ""
    
    lien_video = serveurs_disponibles.get(serveur_choisi, "")
    
    return render_template(
        "player.html", 
        anime=anime, 
        episode_actuel=episode_actuel,
        ep_index=ep_index,
        langue_choisie=langue_choisie, 
        langues_disponibles=langues_disponibles,
        serveur_choisi=serveur_choisi, 
        serveurs=liste_noms_serveurs, 
        lien_video=lien_video,
        nombre_langues=len(langues_disponibles),
        nombre_lecteurs=len(liste_noms_serveurs)
    )

if __name__ == "__main__":
    # Configuration DNS pour écouter sur votre serveur de production
    app.run(debug=True, host="0.0.0.0", port=5000)

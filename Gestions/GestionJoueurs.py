import json
from Classes.Joueur import Joueur

# Cette fonction est utilisée pour sérialiser un objet Joueur en JSON
def joueur_serializer(obj):
    if isinstance(obj, Joueur):  # Si l'objet est une instance de la classe Joueur
        return obj.to_dict()  # On retourne le dictionnaire correspondant à l'objet Joueur
    raise TypeError("Type not serializable")  # Si l'objet n'est pas une instance de Joueur, on lève une exception

# Cette classe gère les opérations liées aux joueurs
class GestionJoueurs:
    def __init__(self, nom_fichier):  # Constructeur de la classe
        self.nom_fichier = nom_fichier  # Nom du fichier où sont stockés les joueurs
        self.joueurs = self.charger_joueurs()  # Liste des joueurs chargés depuis le fichier

    # Cette méthode sauvegarde la liste des joueurs dans le fichier
    def sauvegarder_joueurs(self):
        with open(self.nom_fichier, 'w') as fichier:  # On ouvre le fichier en mode écriture
            # On écrit la liste des joueurs dans le fichier en format JSON
            json.dump([joueur.to_dict() for joueur in self.joueurs], fichier, default=joueur_serializer)

    # Cette méthode charge la liste des joueurs depuis le fichier
    def charger_joueurs(self):
        try:  # On tente d'ouvrir le fichier et de charger les joueurs
            with open(self.nom_fichier, 'r') as fichier:  # On ouvre le fichier en mode lecture
                joueurs_data = json.load(fichier)  # On charge les données JSON depuis le fichier
                # On convertit chaque dictionnaire en objet Joueur et on retourne la liste des joueurs
                return [Joueur.from_dict(joueur_data) for joueur_data in joueurs_data]
        except (FileNotFoundError, json.JSONDecodeError):  # Si le fichier n'existe pas ou si les données JSON sont mal formées
            return []  # On retourne une liste vide

    def creer_joueur(self, nom, prenom, date_naissance, elo):
        # Cette méthode crée un nouveau joueur et l'ajoute à la liste des joueurs
        identifiant = len(self.joueurs) + 1  # L'identifiant du joueur est le nombre actuel de joueurs plus un
        joueur = Joueur(identifiant, nom, prenom, date_naissance, elo)  # Crée un nouvel objet Joueur
        self.joueurs.append(joueur)  # Ajoute le nouveau joueur à la liste des joueurs
        self.sauvegarder_joueurs()  # Sauvegarde la liste des joueurs dans le fichier
        return joueur  # Retourne le nouveau joueur

    def modifier_joueur(self, identifiant, nom=None, prenom=None, date_naissance=None, elo=None):
        # Cette méthode modifie les informations d'un joueur existant
        for joueur in self.joueurs:  # Parcourt la liste des joueurs
            if joueur.identifiant == identifiant:  # Si l'identifiant du joueur correspond à l'identifiant recherché
                # Modifie les informations du joueur si elles sont fournies
                if nom:
                    joueur.nom = nom
                if prenom:
                    joueur.prenom = prenom
                if date_naissance:
                    joueur.date_naissance = date_naissance
                if elo:
                    joueur.elo = elo
                self.sauvegarder_joueurs()  # Sauvegarde la liste des joueurs dans le fichier
                return joueur  # Retourne le joueur modifié
        raise ValueError("Joueur non trouvé")  # Si aucun joueur avec l'identifiant recherché n'est trouvé, lève une exception

    def supprimer_joueur(self, identifiant):
        # Cette méthode supprime un joueur de la liste des joueurs
        self.joueurs = [joueur for joueur in self.joueurs if joueur.identifiant != identifiant]  # Supprime le joueur avec l'identifiant recherché de la liste des joueurs
        self.sauvegarder_joueurs()  # Sauvegarde la liste des joueurs dans le fichier

    def joueur_serializer(obj):
        # Cette fonction est utilisée pour sérialiser un objet Joueur en JSON
        if isinstance(obj, Joueur):  # Si l'objet est une instance de la classe Joueur
            return obj.to_dict()  # On retourne le dictionnaire correspondant à l'objet Joueur
        raise TypeError("Type not serializable")  # Si l'objet n'est pas une instance de Joueur, on lève une exception
import json
from Classes.Joueur import Joueur
from Classes.Match import Match
from Gestions.GestionTournoi import GestionTournois

class GestionMatchs:
    def __init__(self, fichier):
        # Constructeur de la classe
        # Initialise le dernier numéro de match à 0, le nom du fichier et charge les matchs depuis le fichier
        self.dernier_numero_match = 0
        self.fichier = fichier
        self.matchs = self.charger_matchs()

    def ajouter_match(self, match):
        # Ajoute un match à la liste des matchs et sauvegarde la liste dans le fichier
        self.matchs.append(match)
        self.sauvegarder_matchs()

    def sauvegarder_matchs(self):
        # Sauvegarde la liste des matchs dans le fichier en format JSON
        with open(self.fichier, 'w') as fichier:
            json.dump([match.to_dict() for match in self.matchs], fichier)

    def charger_matchs(self):
        # Charge la liste des matchs depuis le fichier
        # Si le fichier n'existe pas, retourne une liste vide
        try:
            with open(self.fichier, 'r') as fichier:
                matchs_data = json.load(fichier)
                return [Match.from_dict(match_data) for match_data in matchs_data]
        except FileNotFoundError:
            return []

    def choisir_match(self, tournoi):
        # Demande à l'utilisateur de choisir un numéro de match
        # Si le numéro est valide, retourne le match correspondant
        # Sinon, affiche un message d'erreur et retourne None
        try:
            match_number = int(input("Choisissez le numéro du match (appuyez sur Entrée pour ignorer) : "))
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier.")
            return None

        for match in tournoi.matchs:
            if match.numero == match_number:
                return match

        print("Erreur: Aucun match trouvé avec le numéro spécifié.")
        return None

    def planifier_match(self, joueur1, joueur2):
        # Planifie un nouveau match entre deux joueurs
        # Si les deux joueurs sont les mêmes, affiche un message d'erreur et retourne None
        # Sinon, crée un nouveau match et l'ajoute à la liste des matchs
        if joueur1 == joueur2:
            print("Erreur: Un joueur ne peut pas jouer contre lui-même dans un match.")
            return None

        nouveau_numero_match = self.dernier_numero_match + 1
        self.dernier_numero_match = nouveau_numero_match

        nouveau_match = Match(joueur1, joueur2, nouveau_numero_match)
        return nouveau_match

    def afficher_matchs(self, matchs):
        # Affiche la liste des matchs
        print("===== LISTE DES MATCHS =====")
        for match in matchs:
            print(f"{match.numero}. {match.joueur1.nom} vs {match.joueur2.nom}")

    def enregistrer_resultat(self, numero, tournoi, resultat):
        # Enregistre le résultat d'un match
        # Si le match n'existe pas, affiche un message d'erreur
        # Sinon, met à jour le résultat du match et sauvegarde la liste des matchs
        match = next((m for m in self.matchs if m.numero == numero), None)

        if match is None:
            print(f"No match found with numero: {numero}")
            return

        gestion_tournoi = GestionTournois("Model/tournois.json")

        for m in tournoi.matchs:
            if m.numero == numero:
                print(f"Match {numero} from {tournoi.nom} updated with result: {resultat}")
                m.resultat = resultat
                break

        self.sauvegarder_matchs()
        tournoi.sauvegarder(gestion_tournoi)
        gestion_tournoi.sauvegarder_tournois()
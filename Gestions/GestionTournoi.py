import json
from Classes.Tournoi import Tournoi
import csv
from datetime import datetime

class GestionTournois:
    def __init__(self, fichier):
        # Initialiser l'objet GestionTournois avec un fichier et charger les tournois depuis ce fichier
        self.fichier = fichier
        self.tournois = self.charger_tournois()

    def sauvegarder_tournois(self):
        # Sauvegarder les tournois dans un fichier JSON
        with open('Model/tournois.json', 'w') as f:
            json.dump([tournoi.to_dict() for tournoi in self.tournois], f)

    def charger_tournois(self):
        try:
            # Charger les données des tournois depuis le fichier JSON
            with open(self.fichier, 'r') as fichier:
                tournois_data = json.load(fichier)
                return [Tournoi.from_dict(tournoi_data) for tournoi_data in tournois_data]
        except FileNotFoundError:
            # Retourner une liste vide si le fichier n'est pas trouvé
            return []

    def creer_tournoi(self, nom, date):
        # Vérifier si le nom du tournoi est vide
        if not nom:
            print("Erreur: Le nom du tournoi ne peut pas être vide.")
            return
        while True:
            try:
                # Vérifier si la date du tournoi est au format correct (YYYY-MM-DD)
                datetime.strptime(date, '%Y-%m-%d')  # Utiliser datetime.strptime après l'import
                break
            except ValueError:
                # Afficher un message d'erreur et demander à l'utilisateur de saisir une date valide
                print("Erreur: La date du tournoi doit être une date valide au format YYYY-MM-DD.")
                date = input("Entrez la date du tournoi (YYYY-MM-DD): ")
        # Créer un nouvel objet Tournoi et l'ajouter à la liste des tournois
        tournoi = Tournoi(nom, date)
        self.tournois.append(tournoi)
        # Sauvegarder les tournois dans le fichier après création d'un nouveau tournoi
        self.sauvegarder_tournois()
        # Retourner l'objet Tournoi nouvellement créé
        return tournoi


   
    def modifier_tournoi(self, nom, date):
        # Vérifier si le nom du tournoi est vide
        if not nom:
            print("Erreur: Le nom du tournoi ne peut pas être vide.")
            return
        while True:
            try:
                # Vérifier si la date du tournoi est au format correct (YYYY-MM-DD)
                datetime.strptime(date, '%Y-%m-%d')  # Utiliser datetime.strptime après l'import
                break
            except ValueError:
                # Afficher un message d'erreur et demander à l'utilisateur de saisir une date valide
                print("Erreur: La date du tournoi doit être une date valide au format YYYY-MM-DD.")
                date = input("Entrez la date du tournoi (YYYY-MM-DD): ")
        # Parcourir les tournois pour trouver celui avec le nom correspondant et mettre à jour sa date
        for tournoi in self.tournois:
            if tournoi.nom == nom:
                tournoi.date = date
                return
        # Afficher un message d'erreur si aucun tournoi n'est trouvé avec le nom spécifié
        print(f"Erreur: Aucun tournoi trouvé avec le nom '{nom}'.")

    def supprimer_tournoi(self, nom):
        # Vérifier si le nom du tournoi est vide
        if not nom:
            print("Erreur: Le nom du tournoi ne peut pas être vide.")
            return
        # Vérifier si un tournoi avec le nom spécifié existe dans la liste des tournois
        if not any(tournoi.nom == nom for tournoi in self.tournois):
            print(f"Erreur: Aucun tournoi trouvé avec le nom '{nom}'.")
            return
        # Supprimer le tournoi de la liste des tournois
        self.tournois = [tournoi for tournoi in self.tournois if tournoi.nom != nom]
        # Sauvegarder la liste mise à jour des tournois dans le fichier
        self.sauvegarder_tournois()

    def mettre_a_jour_tournoi(self, tournoi):
        # Trouver le tournoi dans la liste des tournois et le mettre à jour
        for i, t in enumerate(self.tournois):
            if t.nom == tournoi.nom:
                self.tournois[i] = tournoi
        # Sauvegarder la liste mise à jour des tournois dans le fichier
        self.sauvegarder_tournois()

    @staticmethod
    def trouver_tournoi_par_match(tournois, match_numero):
        # Rechercher un tournoi parmi une liste de tournois en fonction du numéro de match
        for i, tournoi in enumerate(tournois):
            if any(match.numero == match_numero for match in tournoi.matchs):
                return tournoi, i
        # Retourner None si aucun tournoi n'est trouvé avec le numéro de match spécifié
        return None, None

    def exporter_resultats_csv(self, nom_fichier):
        # Vérifier si le nom du fichier est vide
        if not nom_fichier:
            raise ValueError("Le nom du fichier ne peut pas être vide.")

        # Compter le nombre de victoires pour chaque joueur
        victoires = self.compter_victoires()

        # Écrire les données dans le fichier CSV
        with open(nom_fichier, 'w', newline='') as csvfile:
            fieldnames = ['Identifiant', 'Nom', 'Prenom', 'Victoires']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Écrire l'en-tête du fichier CSV
            writer.writeheader()

            # Écrire les données de chaque joueur dans le fichier CSV
            for identifiant, nb_victoires in victoires.items():
                joueur = next(j for j in self.joueurs_participants if j.identifiant == identifiant)
                writer.writerow({'Identifiant': identifiant, 'Nom': joueur.nom, 'Prenom': joueur.prenom, 'Victoires': nb_victoires})

import json
import os
from Classes.Joueur import Joueur
from Classes.Match import Match

import csv
import itertools

class Tournoi:
    def __init__(self, nom, date, joueurs_participants=None, matchs=None):
        # Initialisation de l'objet Tournoi
        if not nom:
            raise ValueError("Le nom du tournoi ne peut pas être vide.")
        if not date:
            raise ValueError("La date du tournoi ne peut pas être vide.")
        self.nom = nom
        self.date = date
        self.joueurs_participants = joueurs_participants or []  # Liste des joueurs participants (par défaut, une liste vide)
        self.matchs = matchs or []  # Liste des matchs (par défaut, une liste vide)
        self.dernier_numero_match = len(matchs) if matchs else 1  # Initialise le dernier numéro de match


    def planifier_match(self, joueur1, joueur2, gestion_tournois):
        # Planifie un nouveau match entre deux joueurs
        if joueur1 is None or joueur2 is None:
            raise ValueError("Les joueurs ne peuvent pas être None.")
         
        # Crée un nouveau match
        nouveau_match = Match(joueur1, joueur2, self.dernier_numero_match + 1)  # Crée un nouveau match
        self.matchs.append(nouveau_match)  # Ajoute le match à la liste des matchs du tournoi
        self.dernier_numero_match += 1  # Met à jour le dernier numéro de match généré

        # Sauvegarde le tournoi dans le fichier tournois.json
        self.sauvegarder(gestion_tournois)

        return nouveau_match
        
    def sauvegarder(self, gestion_tournois):
        # Met à jour le tournoi dans la liste des tournois de gestion_tournois
        gestion_tournois.mettre_a_jour_tournoi(self)

    def enregistrer_resultat(self, match, resultat):
        # Enregistre le résultat d'un match
        if not match:
            raise ValueError("Le match ne peut pas être None.")
        if resultat not in ['1-0', '0-1', '0.5-0.5']:
            raise ValueError("Le résultat doit être '1-0', '0-1' ou '0.5-0.5'.")
        match.resultat = resultat

    def afficher_classement(self):
        # Affiche le classement des joueurs en fonction du nombre de victoires
        victoires = self.compter_victoires()
        classement = sorted(victoires.items(), key=lambda x: x[1], reverse=True)
        for i, (identifiant, victoires) in enumerate(classement, start=1):
            joueur = next(j for j in self.joueurs_participants if j.identifiant == identifiant)
            print(f"{i}. {joueur.nom} {joueur.prenom} - Victoires: {victoires}")
    
    def compter_victoires(self):
        # Compte le nombre de victoires pour chaque joueur
        victoires = {joueur.identifiant: 0 for joueur in self.joueurs_participants}
        for match in self.matchs:
            if match.resultat == '1-0':
                victoires[match.joueur1.identifiant] += 1
            elif match.resultat == '0-1':
                victoires[match.joueur2.identifiant] += 1
        return victoires
    
    def exporter_resultats_csv(self):
        # Demander à l'utilisateur d'entrer le nom du fichier CSV
        nom_fichier = input("Entrez le nom du fichier CSV (appuyez sur Entrée pour ignorer) : ")
        
        # Vérifier si le nom du fichier est vide
        if not nom_fichier:
            print("Erreur: Le nom du fichier ne peut pas être vide.")
            return None

        # Ajouter l'extension .csv au nom du fichier
        nom_fichier += ".csv"
        
        # Définir le sous-répertoire et le chemin complet du fichier CSV
        sous_repertoire = "csv"
        chemin_complet = os.path.join(sous_repertoire, nom_fichier)

        try:
            # Créer le sous-répertoire s'il n'existe pas
            os.makedirs(sous_repertoire, exist_ok=True)
        except Exception as e:
            # Gérer les erreurs liées à la création du sous-répertoire
            print(f"Erreur: Impossible de créer le sous-répertoire. Détails de l'erreur : {e}")
            return None

        # Compter le nombre de victoires pour chaque joueur
        victoires = self.compter_victoires()

        try:
            # Écrire les données dans le fichier CSV
            with open(chemin_complet, 'w', newline='') as csvfile:
                fieldnames = ['Nom', 'Prénom', 'Elo', 'Victoires']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Écrire l'en-tête du fichier CSV
                writer.writeheader()
                
                # Écrire les données de chaque joueur dans le fichier CSV
                for joueur in self.joueurs_participants:
                    writer.writerow({
                        'Nom': joueur.nom, 
                        'Prénom': joueur.prenom, 
                        'Elo': joueur.elo,
                        'Victoires': victoires.get(joueur.identifiant, 0)
                    })
        except Exception as e:
            # Gérer les erreurs liées à l'écriture dans le fichier CSV
            print(f"Erreur: Impossible d'écrire dans le fichier CSV. Détails de l'erreur : {e}")
            return None

        # Afficher un message de réussite
        print("Exportation réussie.")
        
        # Retourner le chemin complet du fichier CSV
        return chemin_complet

    

    def jumeler_matchs_par_elo(self, gestion_tournois):
        # Triez les joueurs par leur score Elo de manière décroissante
        joueurs_tries = sorted(self.joueurs_participants, key=lambda joueur: joueur.elo, reverse=True)

        # Initialisez joueur_sans_match à None
        joueur_sans_match = None

        # Vérifiez si le nombre de joueurs est impair
        if len(joueurs_tries) % 2 != 0:
            # Retirez le dernier joueur de la liste
            joueur_sans_match = joueurs_tries.pop()

        # Planifiez les matchs pour les autres joueurs par paires
        for i in range(0, len(joueurs_tries), 2):
            joueur1 = joueurs_tries[i]
            joueur2 = joueurs_tries[i + 1]
            self.planifier_match(joueur1, joueur2, gestion_tournois)

        # Informez l'utilisateur si un joueur n'a pas de match
        if joueur_sans_match:
            print(f"Le nombre de joueurs est impair. {joueur_sans_match.nom} n'aura pas de match.")
        
    
    def visualiser_statistiques_joueur(self, joueur):
        if not joueur:
            raise ValueError("Le joueur ne peut pas être None.")
        matchs_joues = [match for match in self.matchs if joueur in [match.joueur1, match.joueur2] and match.resultat is not None]
        victoires = matchs_joues.count(lambda match: match.resultat == '1-0')
        defaites = matchs_joues.count(lambda match: match.resultat == '0-1')
        matchs_nuls = matchs_joues.count(lambda match: match.resultat == '0.5-0.5')
        total_matchs = len(matchs_joues)

        pourcentage_victoires = (victoires / total_matchs) * 100 if total_matchs > 0 else 0

        print(f"Statistiques pour {joueur.nom} {joueur.prenom}:")
        print(f"Nombre total de matchs joués: {total_matchs}")
        print(f"Nombre de victoires: {victoires}")
        print(f"Nombre de défaites: {defaites}")
        print(f"Nombre de matchs nuls: {matchs_nuls}")
        print(f"Pourcentage de victoire: {pourcentage_victoires}%")

    @classmethod
    def from_dict(cls, tournoi_dict):
        if not tournoi_dict:
            raise ValueError("Le dictionnaire du tournoi ne peut pas être None.")
        nom = tournoi_dict.get('nom')
        date = tournoi_dict.get('date')
        joueurs_participants = tournoi_dict.get('joueurs_participants', [])
        matchs = tournoi_dict.get('matchs', [])
        if not nom:
            raise ValueError("Le nom du tournoi ne peut pas être vide.")
        if not date:
            raise ValueError("La date du tournoi ne peut pas être vide.")
        if not isinstance(joueurs_participants, list):
            raise ValueError("Les joueurs participants doivent être une liste.")
        if not isinstance(matchs, list):
            raise ValueError("Les matchs doivent être une liste.")
        joueurs_participants = [Joueur.from_dict(joueur_dict) for joueur_dict in joueurs_participants]
        matchs = [Match.from_dict(match_dict) for match_dict in matchs]
        return cls(nom, date, joueurs_participants, matchs)
    
    @classmethod
    def from_dict(cls, tournoi_dict):
        # Vérifier si le dictionnaire du tournoi est vide
        if not tournoi_dict:
            raise ValueError("Le dictionnaire du tournoi ne peut pas être None.")

        # Extraire les données du dictionnaire
        nom = tournoi_dict.get('nom')
        date = tournoi_dict.get('date')
        joueurs_participants = tournoi_dict.get('joueurs_participants', [])
        matchs = tournoi_dict.get('matchs', [])

        # Vérifier si le nom et la date sont présents
        if not nom:
            raise ValueError("Le nom du tournoi ne peut pas être vide.")
        if not date:
            raise ValueError("La date du tournoi ne peut pas être vide.")

        # Vérifier le type des listes de joueurs et de matchs
        if not isinstance(joueurs_participants, list):
            raise ValueError("Les joueurs participants doivent être une liste.")
        if not isinstance(matchs, list):
            raise ValueError("Les matchs doivent être une liste.")

        # Convertir les dictionnaires des joueurs et des matchs en objets correspondants
        joueurs_participants = [Joueur.from_dict(joueur_dict) for joueur_dict in joueurs_participants]
        matchs = [Match.from_dict(match_dict) for match_dict in matchs]

        # Retourner une instance du tournoi avec les données extraites
        return cls(nom, date, joueurs_participants, matchs)

    def choisir_match_par_numero(self, numero):
        # Vérifier si le numéro du match est vide
        if not numero:
            raise ValueError("Le numéro du match ne peut pas être None.")

        # Rechercher les matchs correspondant au numéro spécifié
        matching_matches = [match for match in self.matchs if match.numero == numero]

        # Vérifier s'il y a des matchs correspondants
        if matching_matches:
            # Retourner le premier match correspondant
            return matching_matches[0]
        else:
            # Afficher un message si aucun match n'est trouvé
            print("Aucun match trouvé avec le numéro spécifié.")
            return None


    def to_dict(self):
        # Convertit l'objet Tournoi en un dictionnaire, y compris la liste des matchs
        return {
            'nom': self.nom,
            'date': self.date,
            'joueurs_participants': [joueur.to_dict() for joueur in self.joueurs_participants],
            'matchs': [match.to_dict() for match in self.matchs],
            'dernier_numero_match': self.dernier_numero_match,
        }
        
    def afficher_matchs(self, matchs):
        # Affiche la liste des matchs
        print("===== LISTE DES MATCHS =====")
        for match in matchs:
            print(f"{match.numero}. {match.joueur1.nom} vs {match.joueur2.nom}")   
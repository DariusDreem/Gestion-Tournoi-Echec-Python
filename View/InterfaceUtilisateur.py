from Gestions.GestionTournoi import GestionTournois
from Gestions.GestionJoueurs import GestionJoueurs
from Gestions.GestionMatch import GestionMatchs
from Classes.Tournoi import Tournoi
from Classes.Joueur import Joueur
from Classes.Match import Match
from datetime import datetime
import json

gestion_joueurs = GestionJoueurs("Model/joueurs.json")

def menu_principal():
    print("===== MENU PRINCIPAL =====")
    print("1. Gestion des joueurs")
    print("2. Gestion des tournois")
    print("3. Bonus et autres")
    print("4. Quitter")

def menu_gestion_joueurs(gestion_joueurs):
    print("===== GESTION DES JOUEURS =====")
    print("1. Ajouter un joueur")
    print("2. Modifier un joueur")
    print("3. Supprimer un joueur")
    print("4. Retour au menu principal")

def menu_gestion_tournois(gestion_tournois):
    print("===== GESTION DES TOURNOIS =====")
    print("1. Créer un tournoi")
    print("2. Modifier un tournoi")
    print("3. Supprimer un tournoi")
    print("4. Inscrire un joueur à un tournoi")
    print("5. Planifier un match dans un tournoi")
    print("6. Enregistrer le résultat d'un match")
    print("7. Afficher le classement d'un tournoi")
    print("8. Exporter les résultats d'un tournoi au format CSV")
    print("9. Retour au menu principal")

def menu_bonus_et_autre():
    print("\nBonus et autre :")
    print("1. Jumelage automatique de matchs dans un tournoi")
    print("2. Afficher les statistiques d'un joueur")
    print("3. Afficher la liste des joueurs d'un tournoi")
    print("4. Afficher la liste des matchs d'un tournoi")
    print("5. Retour au menu principal")
    

def afficher_joueurs(joueurs):
    print("===== LISTE DES JOUEURS =====")
    for joueur in joueurs:
        print(f"{joueur.identifiant}. {joueur.nom} {joueur.prenom} - Elo: {joueur.elo}")

def afficher_tournois(tournois):
    print("===== LISTE DES TOURNOIS =====")
    for tournoi in tournois:
        print(f"{tournoi.nom} - Date: {tournoi.date}")

def choisir_joueur(joueurs):
    for i, joueur in enumerate(joueurs, start=1):
        print(f"{i}. {joueur.nom} {joueur.prenom}")

    while True:
        try:
            choix = int(input("Choisissez le numéro du joueur (appuyez sur Entrée pour ignorer) : "))
            if 1 <= choix <= len(joueurs):
                return joueurs[choix - 1]
            print("Erreur: Aucun joueur trouvé avec le numéro spécifié.")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier.")
            return None

def choisir_tournoi():
    with open('Model/tournois.json', 'r') as f:
        data = json.load(f)
    if not data:
        print("Erreur: Aucun tournoi disponible.")
        return None
    tournois = [Tournoi.from_dict(tournoi) for tournoi in data]
    afficher_tournois(tournois)
    choix = input("Choisissez le nom du tournoi (appuyez sur Entrée pour ignorer) : ")
    if not choix:
        print("Erreur: Le nom du tournoi ne peut pas être vide.")
        return None
    tournoi_choisi = [tournoi for tournoi in tournois if tournoi.nom == choix]
    if not tournoi_choisi:
        print("Erreur: Tournoi non trouvé.")
        return None
    return tournoi_choisi[0]

def main():
    gestion_joueurs = GestionJoueurs("Model/joueurs.json")
    gestion_tournois = GestionTournois("Model/tournois.json")
    gestion_matchs = GestionMatchs("Model/matchs.json")

    while True:
        menu_principal()
        choix_principal = input("Choisissez une option : ")
        
        match choix_principal:
            case "1":
                while True:
                    menu_gestion_joueurs(gestion_joueurs)
                    choix_joueurs = input("Choisissez une option : ")

                    match choix_joueurs:
                        case "1":
                            nom = input("Nom du joueur : ")
                            while not nom:
                                print("Erreur: Le nom du joueur ne peut pas être vide.")
                                nom = input("Nom du joueur : ")

                            prenom = input("Prénom du joueur : ")
                            while not prenom:
                                print("Erreur: Le prénom du joueur ne peut pas être vide.")
                                prenom = input("Prénom du joueur : ")

                            

                            date_naissance = input("Date de naissance du joueur (YYYY-MM-DD) : ")
                            while True:
                                try:
                                    datetime.strptime(date_naissance, '%Y-%m-%d')  # Essaie de convertir la date en un objet datetime
                                    break  # Si la conversion réussit, sort de la boucle
                                except ValueError:
                                    print("Erreur: La date de naissance doit être une date valide au format YYYY-MM-DD.")
                                    date_naissance = input("Date de naissance du joueur (YYYY-MM-DD) : ")
                            
                            elo = input("Classement ELO du joueur : ")
                            while not elo or not elo.isdigit():
                                print("Erreur : Le classement ELO du joueur ne peut pas être vide et doit être un nombre entier.")
                                elo = input("Classement ELO du joueur : ")

                            elo = int(elo)

                            gestion_joueurs.creer_joueur(nom, prenom, date_naissance, elo)
                            afficher_joueurs(gestion_joueurs.joueurs)

                        case "2":
                            afficher_joueurs(gestion_joueurs.joueurs)
                            identifiant = input("Choisissez le numéro du joueur à modifier : ")
                            while not identifiant.isdigit():
                                print("Erreur: L'identifiant doit être un nombre.")
                                identifiant = input("Choisissez le numéro du joueur à modifier : ")
                            identifiant = int(identifiant)
                            
                            joueurs_filtrés = [joueur for joueur in gestion_joueurs.joueurs if joueur.identifiant == identifiant]
                            while not joueurs_filtrés:
                                print("Erreur: Aucun joueur trouvé avec cet identifiant.")
                                identifiant = input("Choisissez le numéro du joueur à modifier : ")
                                while not identifiant.isdigit():
                                    print("Erreur: L'identifiant doit être un nombre.")
                                    identifiant = input("Choisissez le numéro du joueur à modifier : ")
                                identifiant = int(identifiant)
                                joueurs_filtrés = [joueur for joueur in gestion_joueurs.joueurs if joueur.identifiant == identifiant]
                            joueur = joueurs_filtrés[0]
                            
                            nom = input(f"Nouveau nom ({joueur.nom}) : ") or joueur.nom
                            while not nom:
                                print("Erreur: Le nom ne peut pas être vide.")
                                nom = input(f"Nouveau nom ({joueur.nom}) : ") or joueur.nom

                            prenom = input(f"Nouveau prénom ({joueur.prenom}) : ") or joueur.prenom
                            while not prenom:
                                print("Erreur: Le prénom ne peut pas être vide.")
                                prenom = input(f"Nouveau prénom ({joueur.prenom}) : ") or joueur.prenom

                            date_naissance = input(f"Nouvelle date de naissance ({joueur.date_naissance}) : ") or joueur.date_naissance
                            while True:
                                try:
                                    datetime.strptime(date_naissance, '%Y-%m-%d')  # Essaie de convertir la date en un objet datetime
                                    break  # Si la conversion réussit, sort de la boucle
                                except ValueError:
                                    print("Erreur: La date de naissance doit être une date valide au format YYYY-MM-DD.")
                                    date_naissance = input(f"Nouvelle date de naissance ({joueur.date_naissance}) : ") or joueur.date_naissance
                            
                            elo = input(f"Nouveau classement ELO ({joueur.elo}) : ") or str(joueur.elo)
                            while not elo.isdigit():
                                print("Erreur: Le classement ELO doit être un nombre.")
                                elo = input(f"Nouveau classement ELO ({joueur.elo}) : ") or str(joueur.elo)
                            elo = int(elo)

                            gestion_joueurs.modifier_joueur(identifiant, nom, prenom, date_naissance, elo)
                            afficher_joueurs(gestion_joueurs.joueurs)
                        case "3":
                            afficher_joueurs(gestion_joueurs.joueurs)
                            identifiant = input("Choisissez le numéro du joueur à supprimer (appuyez sur Entrée pour ignorer) : ")
                            if identifiant:  # Si l'utilisateur a entré quelque chose
                                while not identifiant.isdigit():
                                    print("Erreur: L'identifiant doit être un nombre.")
                                    identifiant = input("Choisissez le numéro du joueur à supprimer (appuyez sur Entrée pour ignorer) : ")
                                    if not identifiant:  # Si l'utilisateur n'a rien entré
                                        break
                                if identifiant:  # Si l'utilisateur a entré quelque chose
                                    identifiant = int(identifiant)
                                    gestion_joueurs.supprimer_joueur(identifiant)
                                    afficher_joueurs(gestion_joueurs.joueurs)

                        case "4":
                            break

            case "2":
                while True:
                    menu_gestion_tournois(gestion_tournois)
                    choix_tournois = input("Choisissez une option : ")

                    match choix_tournois:
                        case "1":
                            nom = input("Nom du tournoi : ")
                            date = input("Date du tournoi (YYYY-MM-DD) : ")
                            gestion_tournois.creer_tournoi(nom, date)
                            afficher_tournois(gestion_tournois.tournois)

                        case "2":
                            afficher_tournois(gestion_tournois.tournois)
                            nom = input("Choisissez le nom du tournoi à modifier : ")
                            date = input("Nouvelle date du tournoi : ")
                            gestion_tournois.modifier_tournoi(nom, date)
                            afficher_tournois(gestion_tournois.tournois)

                        case "3":
                            afficher_tournois(gestion_tournois.tournois)
                            nom = input("Choisissez le nom du tournoi à supprimer : ")
                            gestion_tournois.supprimer_tournoi(nom)
                            afficher_tournois(gestion_tournois.tournois)

                        case "4":
                            joueur = choisir_joueur(gestion_joueurs.joueurs)
                            tournoi = choisir_tournoi()
                            if joueur and tournoi:
                                if joueur not in tournoi.joueurs_participants:
                                    tournoi.joueurs_participants.append(joueur)
                                    tournoi.sauvegarder(gestion_tournois)  # Sauvegarde le tournoi après l'ajout du joueur
                                    print(f"{joueur.nom} {joueur.prenom} inscrit avec succès au tournoi {tournoi.nom}")
                                else:
                                    print("Erreur: Un joueur ne peut pas être inscrit deux fois dans le même tournoi.")
                            else:
                                print("Erreur: Impossible d'inscrire le joueur au tournoi.")

                        case "5":
                            tournoi = choisir_tournoi()
                            if not tournoi:
                                print("Erreur: Aucun tournoi choisi.")
                                break

                            if not tournoi.joueurs_participants or len(tournoi.joueurs_participants) < 2:
                                print(f"Erreur: Pas assez de joueurs participants a ce matchs: {len(tournoi.joueurs_participants)}")
                                break

                            joueur1 = choisir_joueur(tournoi.joueurs_participants)
                            if not joueur1:
                                print("Erreur: Aucun premier joueur choisi.")
                                break

                            joueur2 = choisir_joueur(tournoi.joueurs_participants)
                            if not joueur2:
                                print("Erreur: Aucun deuxième joueur choisi.")
                                break
                            
                            if joueur1 == joueur2:
                                print("Erreur: Un joueur ne peut pas jouer contre lui-même dans un match.")
                                break

                            tournoi.planifier_match(joueur1, joueur2, gestion_tournois)  # Ajoute le tournoi comme argument
                            gestion_tournois.sauvegarder_tournois()
                            print("Match planifié avec succès.")

                        case "6":
                            tournoi = choisir_tournoi()
                            if not tournoi:
                                print("Erreur: Aucun tournoi choisi.")
                                break

                            # Afficher la liste des matchs du tournoi avant de choisir
                            if not tournoi.matchs:
                                print("Erreur: Aucun match dans ce tournoi.")
                                break
                            afficher_matchs(tournoi.matchs)

                            match = gestion_matchs.choisir_match(tournoi)  # Passer l'objet tournoi
                            if not match:
                                print("Erreur: Aucun match choisi.")
                                break

                            resultat = input("Résultat du match (1-0, 0.5-0.5, 0-1) : ")
                            if resultat not in ["1-0", "0.5-0.5", "0-1"]:
                                print("Erreur: Résultat du match invalide.")
                                break
                                
                            gestion_matchs.enregistrer_resultat(match.numero, tournoi , resultat)

                        case "7":
                            tournoi = choisir_tournoi()
                            if not tournoi:
                                print("Erreur: Aucun tournoi choisi.")
                                break
                            tournoi.afficher_classement()

                        case "8":
                            tournoi = choisir_tournoi()
                            if not tournoi:
                                print("Erreur: Aucun tournoi choisi.")
                                break
                            tournoi.exporter_resultats_csv()
                            break

                        case "9":
                            break

            case "3":
                while True:
                    menu_bonus_et_autre()
                    choix_matchs = input("Choisissez une option : ")

                    match choix_matchs:
                        case "1":
                            gestion_matchs = GestionMatchs("Model/matchs.json")
                            tournoi = choisir_tournoi()
                            print(tournoi.date)
                            if not tournoi:
                                print("Erreur: Aucun tournoi choisi.")
                                break
                            tournoi.jumeler_matchs_par_elo(gestion_tournois)

                        case "2":
                            print("===== STATISTIQUES D'UN JOUEUR =====")
                            joueur = choisir_joueur(gestion_joueurs.joueurs)
                            if joueur:
                                print(f"Identifiant: {joueur.identifiant}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, Date de naissance: {joueur.date_naissance}, Elo: {joueur.elo}")
                                stats = joueur.calculer_statistiques(gestion_tournois.tournois)
                                print(f"Total des matchs: {stats['total_matchs']}, Total des victoires: {stats['total_victoires']}, Pourcentage de victoire: {stats['pourcentage_victoire']}%")
                            else:
                                print("Aucun joueur n'a été choisi.")
                                
                        case "3":
                            tournoi = choisir_tournoi()
                            if tournoi:
                                print("Liste des joueurs pour le tournoi choisi :")
                                for joueur in tournoi.joueurs_participants:
                                    print(f"Identifiant: {joueur.identifiant}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, Date de naissance: {joueur.date_naissance}, Elo: {joueur.elo}")
                            else:
                                print("Aucun tournoi n'a été choisi.")
                        
                        case "4":
                            tournoi = choisir_tournoi()
                            tournoi.afficher_matchs(tournoi.matchs)
                        
                        case "5":
                            break

            case "4":
                print("Au revoir!")
                break

# Ajoute cette fonction à ton code
def afficher_matchs(matchs):
    print("===== LISTE DES MATCHS =====")
    for match in matchs:
        print(f"{match.numero}. {match.joueur1.nom} vs {match.joueur2.nom}")

if __name__ == "__main__":
    main()

import json

class Joueur:
    def __init__(self, identifiant, nom, prenom, date_naissance, elo):
        # Vérifie que les paramètres ne sont pas vides
        if not identifiant:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")
        if not nom:
            raise ValueError("Le nom du joueur ne peut pas être vide.")
        if not prenom:
            raise ValueError("Le prénom du joueur ne peut pas être vide.")
        if not date_naissance:
            raise ValueError("La date de naissance du joueur ne peut pas être vide.")
        if not elo:
            raise ValueError("Le classement ELO du joueur ne peut pas être vide.")
        
        # Initialise les attributs de l'instance
        self.identifiant = identifiant
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.elo = elo

    def __eq__(self, other):
        # Définit l'égalité entre deux instances de Joueur comme l'égalité de leurs identifiants
        if isinstance(other, Joueur):
            return self.identifiant == other.identifiant
        return False

    def to_dict(self):
        # Convertit l'instance de Joueur en un dictionnaire
        return {
            "identifiant": self.identifiant,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "elo": self.elo
        }

    @classmethod
    def from_dict(cls, joueur_data):
        # Crée une instance de Joueur à partir d'un dictionnaire
        if not joueur_data:
            raise ValueError("Les données du joueur ne peuvent pas être None.")
        return cls(
            joueur_data['identifiant'],
            joueur_data['nom'],
            joueur_data['prenom'],
            joueur_data['date_naissance'],
            joueur_data['elo']
        )
        
    def calculer_statistiques(self, tournois):
        # Calcule les statistiques du joueur à partir de la liste des tournois
        # Trouve tous les matchs joués par le joueur
        matchs_joues = [match for tournoi in tournois for match in tournoi.matchs if match.joueur1.identifiant == self.identifiant or match.joueur2.identifiant == self.identifiant]
        total_matchs = len(matchs_joues)
        # Calcule le nombre total de victoires du joueur
        total_victoires = sum(tournoi.compter_victoires().get(self.identifiant, 0) for tournoi in tournois)
        # Calcule le pourcentage de victoire du joueur
        pourcentage_victoire = round((total_victoires / total_matchs) * 100, 2) if total_matchs > 0 else 0

        return {
            'total_matchs': total_matchs,
            'total_victoires': total_victoires,
            'pourcentage_victoire': pourcentage_victoire,
        }
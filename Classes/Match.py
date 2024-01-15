import json

from Classes.Joueur import Joueur

class Match:
    def __init__(self, joueur1, joueur2, numero, resultat=None):
        # Initialise les attributs de l'instance
        self.joueur1 = joueur1  # Premier joueur du match
        self.joueur2 = joueur2  # Deuxième joueur du match
        self.numero = numero  # Numéro du match
        self.resultat = resultat  # Résultat du match

    def to_dict(self):
        # Convertit l'instance de Match en un dictionnaire
        return {
            "numero": self.numero,  # Numéro du match
            "joueur1": self.joueur1.to_dict(),  # Premier joueur du match
            "joueur2": self.joueur2.to_dict(),  # Deuxième joueur du match
            'resultat': self.resultat  # Résultat du match
        }

    @classmethod
    def from_dict(cls, match_dict):
        # Crée une instance de Match à partir d'un dictionnaire
        joueur1 = Joueur.from_dict(match_dict['joueur1'])  # Premier joueur du match
        joueur2 = Joueur.from_dict(match_dict['joueur2'])  # Deuxième joueur du match
        return cls(joueur1, joueur2, match_dict['numero'], match_dict['resultat'])  # Crée une nouvelle instance de Match

    def planifier_match(self, joueur1, joueur2):
        # Planifie un nouveau match
        used_match_numbers = [match.numero for match in self.matchs]  # Liste des numéros de match déjà utilisés

        # Cherche le premier numéro non utilisé
        nouveau_numero_match = max(used_match_numbers + [self.dernier_numero_match]) + 1  # Nouveau numéro de match

        nouveau_match = Match(joueur1, joueur2, nouveau_numero_match)  # Crée un nouveau match
        self.matchs.append(nouveau_match)  # Ajoute le nouveau match à la liste des matchs
        self.dernier_numero_match = nouveau_numero_match  # Met à jour le dernier numéro de match généré
        self.sauvegarder_matchs()  # Sauvegarde les matchs
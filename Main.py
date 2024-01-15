from View.InterfaceUtilisateur import main
from Gestions.GestionTournoi import GestionTournois

gestion_tournois = GestionTournois("Model/tournois.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramme interrompu.")
        

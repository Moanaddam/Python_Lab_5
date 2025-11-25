import logging
import sys
from csv_reader import (
    charger_csv, 
    CsvException, 
    FichierIntrouvableException, 
    LigneInvalideException, 
    PrixNegatifException
)

logging.basicConfig(
    filename='erreurs.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generer_fichier_exemple():
    with open("data.csv", "w", encoding="utf-8") as f:
        f.write("1;Pomme;1.50\n")
        f.write("2;Banane;0.90\n")
        f.write("\n")
        f.write("3;Orange;2.10\n")

def main():
    generer_fichier_exemple()
    fichier_cible = "data.csv" 
    
    print(f"--- Tentative d'importation de {fichier_cible} ---")

    try:
        articles = charger_csv(fichier_cible)
        
        print(f"Succès ! {len(articles)} articles importés :")
        for art in articles:
            print(f"- {art.nom} : {art.prix:.2f}€")

    except FichierIntrouvableException as e:
        print(f"ERREUR UTILISATEUR : Fichier introuvable.")
        logging.error(f"Fichier manquant : {e}")

    except LigneInvalideException as e:
        print(f"ERREUR DE FORMAT : Le fichier contient une ligne corrompue.")
        logging.error(f"Format invalide : {e}")

    except PrixNegatifException as e:
        print(f"ERREUR MÉTIER : Un article possède un prix invalide.")
        logging.error(f"Règle métier violée : {e}")

    except CsvException as e:
        print(f"ERREUR D'IMPORTATION : Une erreur inconnue est survenue.")
        logging.error(f"Erreur CSV générique : {e}")

    except Exception as e:
        print(f"ERREUR SYSTÈME CRITIQUE.")
        logging.critical(f"Crash inattendu : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
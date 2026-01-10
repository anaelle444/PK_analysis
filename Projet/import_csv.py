import csv
import os
from pymol import cmd

def load_from_csv(filename):
    """
    Charge des structures PDB dans PyMOL à partir d'un fichier CSV.
    Usage dans PyMOL: load_from_csv mon_fichier.csv
    """
    # Vérifier si le fichier existe
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        return

    try:
        with open(filename, newline='', encoding='utf-8') as f:
            lines = f.readlines()
            
            # On saute la 1ère ligne et on utilise la 2ème comme header
            reader = csv.DictReader(lines[1:])
            
            count = 0
            for row in reader:
                entry_id = row.get("Entry ID")
                if entry_id:
                    print(f"Récupération de : {entry_id}...")
                    cmd.fetch(entry_id)
                    count += 1
            
            print(f"Terminé ! {count} structures ont été ajoutées. ✨")
            
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Cette ligne permet d'enregistrer la fonction comme une commande PyMOL
cmd.extend("load_from_csv", load_from_csv)
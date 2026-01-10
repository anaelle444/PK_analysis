import csv
from pymol import cmd

csv_file = "rcsb_pdb_custom_report_20260109152453.csv"

#telecharger toutes les structures pymol du csv dans pymol automatiquement
with open(csv_file, newline='') as f:
    # Lire toutes les lignes
    lines = f.readlines()
    
    # Utiliser la deuxième ligne comme en-tête (index 1)
    reader = csv.DictReader(lines[1:])
    
    for row in reader:
        entry_id = row["Entry ID"]
        if entry_id:  # Vérifier que l'Entry ID n'est pas vide
            print("PDB trouvé :", entry_id)
            # Charger la structure dans PyMOL
            cmd.fetch(entry_id)

    print("téléchargement des srtuctures terminé! ✨")


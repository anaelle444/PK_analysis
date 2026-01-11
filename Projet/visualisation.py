"""
Fonctions pour la procédure : 
- highlight lobe C pour montrer l'alignement des lobes C
"""
#librairies 
from pymol import cmd
import csv
import os

# Configuration
results_csv = "superposition_results.csv"

#fonctions
def highlight_lobes(selection="all"):
    """
    Colore le Lobe C en rose et la Hinge en orange pour montrer l'alignement 
    des strcutures a la references sur ces domaines
    """
    
    # 1. identifier la région charniere (Hinge)
    cmd.select("hinge_region", f"({selection}) and resi 1197-1201")
    cmd.color("brightorange", "hinge_region")
    
    # 2. identifier et colorer uniquement le Lobe C
    cmd.select("lobe_C_region", f"({selection}) and resi 1202-1383")
    cmd.color("salmon", "lobe_C_region")
    
    # deselectionner sinon on a les petits points qui gachent la vue dans l'interface pymol
    cmd.deselect()
    
    print("Highlighting terminé ✨")
    print("  Orange = Hinge (1197-1201)")
    print("  Saumon = Lobe C (1202-1383)")
    
cmd.extend("highlight_lobes", highlight_lobes)
# highlight_lobes()

def color_bad_rmsd(csv_path):
    if not os.path.exists(csv_path):
        print(f"Erreur : Le fichier {csv_path} est introuvable.")
        return
    
    with open(csv_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdb_id = row['PDB_ID']
            assembly_id = "1" 
            # reconstruction du nom de l'objet comme il apparaît dans PyMOL
            obj_name = f"{pdb_id}_assembly{assembly_id}"

            status = row['Status']
            try:
                rmsd_val = float(row['RMSD']) if row['RMSD'] != 'N/A' else None
            except ValueError:
                rmsd_val = None

            # coloration des mauvais alignements (rmsd>4 ou erreur)
            if status == "ERROR" or rmsd_val is None:
                # les structures non alignées ou en erreur -> GRIS
                cmd.color("gray", obj_name)
                print(f"Structure {obj_name} colorée en GRIS (Erreur/Non alignée)")
            
            elif rmsd_val > 4.0:
                # RMSD > 4 -> MARRON
                cmd.color("brown", obj_name)
                print(f"Structure {obj_name} colorée en NOIR (RMSD: {rmsd_val})")

    print("✨ Coloration terminée ✨")

# Exécuter la fonction
color_bad_rmsd(results_csv)

from pymol import cmd
import csv
import os

def isoler_mauvais_alignements(csv_path="superposition_results.csv"):
    """
    Masque toutes les structures et n'affiche que celles avec 
    un RMSD > 4 ou en erreur.
    """
    if not os.path.exists(csv_path):
        print(f"Erreur : {csv_path} introuvable.")
        return

    # 1. Cacher tous les objets chargés pour repartir de zéro
    cmd.hide("everything", "all")
    
    mauvais_structures = []
    
    with open(csv_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdb_id = row['PDB_ID']
            status = row['Status']
            try:
                rmsd_val = float(row['RMSD']) if row['RMSD'] != 'N/A' else None
            except ValueError:
                rmsd_val = None

            # 2. Identifier les objets correspondants dans PyMOL
            # On cherche les objets qui commencent par le PDB_ID (ex: 4WB8_assembly1)
            obj_names = [n for n in cmd.get_names() if n.startswith(pdb_id)]
            
            for obj in obj_names:
                # Condition : RMSD élevé (> 4) ou Erreur d'alignement
                if status == "ERROR" or (rmsd_val is not None and rmsd_val > 4.0):
                    cmd.show("cartoon", obj)
                    mauvais_structures.append(obj)
    
    if mauvais_structures:
        # Zoomer sur les structures problématiques
        cmd.zoom(" + ".join(mauvais_structures))
        print(f"Affichage de {len(mauvais_structures)} structures (RMSD > 4 ou ERROR).")
    else:
        print("Aucune structure avec RMSD > 4 ou ERROR n'a été trouvée.")

# Ajouter la commande à PyMOL
cmd.extend("isoler_mauvais", isoler_mauvais_alignements)


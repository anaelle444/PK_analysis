import csv
import os

# Configuration
results_csv = "superposition_results.csv"

def color_by_rmsd(csv_path):
    if not os.path.exists(csv_path):
        print(f"Erreur : Le fichier {csv_path} est introuvable.")
        return

    print("Début de la coloration par RMSD...")
    
    with open(csv_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdb_id = row['PDB_ID']
            assembly_id = "1" # Par défaut, ou adapter selon votre nomenclature d'objets
            
            # Reconstruction du nom de l'objet tel qu'il apparaît dans PyMOL
            # Note : Assurez-vous que ce nom correspond à celui utilisé dans votre script d'alignement
            obj_name = f"{pdb_id}_assembly{assembly_id}"
            
            # # Vérifier si l'objet existe dans la session PyMOL actuelle
            # if obj_name not in cmd.get_names():
            #     # On essaie une variante si l'ID d'assemblage diffère
            #     potential_names = [n for n in cmd.get_names() if n.startswith(pdb_id)]
            #     if potential_names:
            #         obj_name = potential_names[0]
            #     else:
            #         continue

            status = row['Status']
            try:
                rmsd_val = float(row['RMSD']) if row['RMSD'] != 'N/A' else None
            except ValueError:
                rmsd_val = None

            # Logique de coloration
            if status == "ERROR" or rmsd_val is None:
                # Structures non alignées ou en erreur -> GRIS
                cmd.color("gray", obj_name)
                print(f"Structure {obj_name} colorée en GRIS (Erreur/Non alignée)")
            
            elif rmsd_val > 4.0:
                # RMSD > 4 -> NOIR
                cmd.color("brown", obj_name)
                print(f"Structure {obj_name} colorée en NOIR (RMSD: {rmsd_val})")
            
            else:
                # Optionnel : colorer les bonnes structures en une autre couleur (ex: bleu)
                # cmd.color("cyan", obj_name)
                pass

    print("Coloration terminée.")

# Exécuter la fonction
color_by_rmsd(results_csv)
from pymol import cmd

def highlight_lobes(selection="all"):
    """
    Colore UNIQUEMENT le Lobe C et la Hinge pour ne pas interférer 
    avec la coloration RMSD (Noir/Gris) du script précédent.
    """
    
    # 1. Identifier la Hinge (Charnière)
    # On utilise 'set_color' ou des noms de couleurs précis pour le contraste
    cmd.select("hinge_region", f"({selection}) and resi 1197-1201")
    cmd.color("brightorange", "hinge_region")
    
    # 2. Identifier et colorer uniquement le Lobe C
    # On ne touche pas au Lobe N ni au reste de la protéine (coloration RMSD conservée)
    cmd.select("lobe_C_region", f"({selection}) and resi 1202-1383")
    cmd.color("salmon", "lobe_C_region")
    
    # Nettoyage des sélections dans l'interface PyMOL
    cmd.deselect()
    
    print("Mise en évidence spécifique terminée :")
    print("  Orange = Hinge (1197-1201)")
    print("  Saumon = Lobe C (1202-1383)")
    print("  Note: Le Lobe N et les autres domaines conservent leur couleur RMSD.")

cmd.extend("highlight_lobes", highlight_lobes)
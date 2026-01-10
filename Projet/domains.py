from pymol import cmd

def highlight_lobes(selection="all"):
    """
    Colore les régions clés de la kinase ALK (Q9UM73)
    """
    # 1. Définir le domaine Kinase global (selon UniProt Q9UM73)
    cmd.color("gray80", selection)
    cmd.select("kinase_domain", f"({selection}) and resi 1116-1383")
    cmd.show_as("cartoon", "kinase_domain")
    
    # 2. Identifier la Hinge (Charnière)
    # Pour ALK, la charnière est classiquement située autour des résidus 1197-1201
    # Le résidu "Gatekeeper" est Leu 1196
    cmd.select("hinge", f"({selection}) and resi 1197-1201")
    cmd.color("brightorange", "hinge")
    
    # 3. Identifier le Lobe N et le Lobe C
    cmd.select("lobe_N", f"({selection}) and resi 1116-1196")
    cmd.select("lobe_C", f"({selection}) and resi 1202-1383")
    
    cmd.color("skyblue", "lobe_N")
    cmd.color("salmon", "lobe_C")
    
    print("Coloration ALK terminée :")
    print("Orange = Hinge (1197-1201)")
    print("Bleu = Lobe N | Saumon = Lobe C")

cmd.extend("highlight_lobes", highlight_lobes)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour vérifier les positions du lobe C dans 4WB8
"""
from pymol import cmd
import os

reference_pdb = "4WB8"
reference_chain = "A"

print("=" * 60)
print("VÉRIFICATION DES POSITIONS DU LOBE C DANS 4WB8")
print("=" * 60)

# Charger la structure
ref_file = f"{reference_pdb}-assembly1.cif"
if os.path.exists(ref_file):
    cmd.load(ref_file, f"{reference_pdb}_ref")
else:
    cmd.do(f"fetch_mmcif {reference_pdb}, {reference_pdb}_ref, 1")

# Afficher des informations sur la structure
print(f"\nInformations sur {reference_pdb}:")
print(f"  Chaînes disponibles: {cmd.get_chains(f'{reference_pdb}_ref')}")

# Compter les résidus totaux
n_total = cmd.count_atoms(f"{reference_pdb}_ref and chain {reference_chain} and name CA")
print(f"  Nombre total de résidus (C-alpha) dans chaîne {reference_chain}: {n_total}")

# Obtenir les numéros de résidus min et max
cmd.select("temp_sel", f"{reference_pdb}_ref and chain {reference_chain} and name CA")
stored.residues = []
cmd.iterate("temp_sel", "stored.residues.append(resi)")
cmd.delete("temp_sel")

resi_nums = [int(r) for r in stored.residues if r.isdigit()]
if resi_nums:
    print(f"  Premier résidu: {min(resi_nums)}")
    print(f"  Dernier résidu: {max(resi_nums)}")

# Tester différentes régions pour le lobe C
print("\n" + "=" * 60)
print("TEST DE DIFFÉRENTES RÉGIONS POUR LE LOBE C")
print("=" * 60)

test_ranges = [
    (127, 300, "Standard kinase (littérature)"),
    (40, 300, "Du milieu à la fin"),
    (50, max(resi_nums) if resi_nums else 300, "De ~50 à la fin"),
    (int(n_total * 0.3), max(resi_nums) if resi_nums else 300, "30% à fin (approximatif)"),
]

for start, end, description in test_ranges:
    n_atoms = cmd.count_atoms(f"{reference_pdb}_ref and chain {reference_chain} and resi {start}-{end} and name CA")
    print(f"\nRésidus {start}-{end} ({description}):")
    print(f"  Nombre de C-alpha: {n_atoms}")
    
print("\n" + "=" * 60)
print("RECOMMANDATION")
print("=" * 60)
print("\nPour les protéines kinases, le lobe C commence généralement:")
print("  - Après la 'hinge region' (~résidu 120-130)")
print("  - Et s'étend jusqu'à la fin du domaine catalytique")
print("\nPour 4WB8 (PKACA humaine):")
print("  - La structure contient une délétion de l'exon 1")
print("  - La numérotation peut être différente de la séquence complète")
print("\nVérifiez visuellement dans PyMOL:")
print("  1. Affichez la structure secondaire (cartoon)")
print("  2. Le lobe N contient principalement des feuillets β")
print("  3. Le lobe C contient principalement des hélices α")
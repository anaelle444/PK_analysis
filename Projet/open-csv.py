#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script complet pour charger et superposer toutes les structures ALK sur PKACA
Utilise fetch_mmcif pour les assemblages biologiques
Alignement sur le LOBE C uniquement
"""

import csv
import os
from pymol import cmd

# Fichier CSV contenant les structures PDB
csv_file = "rcsb_pdb_custom_report_20260110111300_new.csv"

# Structure de référence PKACA HUMAINE (P17612)
# 4WB8 : PKACA humaine (Homo sapiens), résolution 1.55 Å
# UniProt: P17612 - cAMP-dependent protein kinase catalytic subunit alpha
# Référence: Cheung et al. (2015) PNAS 112: 1374-1379
# Structure: résidus 14-350 (délétion exon 1)
reference_pdb = "4WB8"
reference_chain = "A"
reference_uniprot = "P17612"

# Positions du LOBE C pour 4WB8
# Le lobe C commence après la hinge region (~127) et s'étend jusqu'à ~350
PKACA_LOBE_C_START = 127
PKACA_LOBE_C_END = 350  # Correction: fin du domaine catalytique

print("=" * 60)
print("CHARGEMENT DE LA STRUCTURE DE RÉFÉRENCE PKACA")
print("=" * 60)
print(f"Protéine: PKACA humaine (Homo sapiens)")
print(f"  UniProt: {reference_uniprot}")
print(f"  Structure PDB: {reference_pdb} chaîne {reference_chain}")
print(f"  Résolution: 1.55 Å")
print(f"  Référence: Cheung et al. (2015) PNAS 112: 1374-1379")
print(f"  Résidus présents: 14-350 (délétion exon 1)")
print(f"Alignement sur le LOBE C uniquement:")
print(f"  Lobe C: résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END}")
print("=" * 60)

# Charger la structure de référence (assemblage biologique 1)
print(f"\nChargement de la structure de référence {reference_pdb}...")
try:
    # Supprimer l'objet s'il existe déjà
    if f"{reference_pdb}_ref" in cmd.get_names():
        cmd.delete(f"{reference_pdb}_ref")
        print(f"✓ Objet existant {reference_pdb}_ref supprimé")
    
    # Vérifier si le fichier existe localement
    ref_file = f"{reference_pdb}-assembly1.cif"
    if os.path.exists(ref_file):
        print(f"✓ Fichier local trouvé: {ref_file}")
        cmd.load(ref_file, f"{reference_pdb}_ref")
    else:
        cmd.do(f"fetch_mmcif {reference_pdb}, {reference_pdb}_ref, 1")
    
    cmd.remove(f"{reference_pdb}_ref and solvent")
    print(f"✓ {reference_pdb} chargé")

    # Afficher des informations sur la structure
    n_chains = len(cmd.get_chains(f"{reference_pdb}_ref"))
    n_residues = cmd.count_atoms(f"{reference_pdb}_ref and chain {reference_chain} and name CA")
    print(f"  Chaînes: {n_chains}, Résidus totaux dans chaîne {reference_chain}: {n_residues}")

except Exception as e:
    print(f"✗ Erreur: {e}")
    exit(1)

# Définir le LOBE C de la référence PKACA avec les positions connues
lobe_c_ref = f"{reference_pdb}_ref and chain {reference_chain} and resi {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END} and name CA"
n_atoms_lobe_c = cmd.count_atoms(lobe_c_ref)

if n_atoms_lobe_c == 0:
    print(f"⚠ ERREUR: Aucun atome trouvé dans le lobe C (résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END})")
    print("  Vérifiez la chaîne et les numéros de résidus!")
    exit(1)

print(f"✓ Lobe C de la référence: {n_atoms_lobe_c} C-alpha (résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END})")
print(f"  Tous les alignements seront faits sur cette région uniquement.")

# Configuration visuelle pour vérification
cmd.hide("everything", f"{reference_pdb}_ref")
cmd.show("cartoon", f"{reference_pdb}_ref")
cmd.color("green", f"{reference_pdb}_ref")
cmd.show("sticks", f"{reference_pdb}_ref and organic")
cmd.show("nb_spheres", f"{reference_pdb}_ref and inorganic")

print("\n" + "=" * 60)
print("TRAITEMENT DES STRUCTURES ALK")
print("=" * 60)

# Créer un fichier de résultats
results = []
count = 0

# Parcourir le CSV en sautant la première ligne (en-têtes de section)
with open(csv_file, newline='') as f:
    # Lire toutes les lignes
    lines = f.readlines()
    
    # Sauter la première ligne (en-têtes de section)
    # La deuxième ligne contient les vrais en-têtes
    reader = csv.DictReader(lines[1:])

    for row in reader:
        entry_id = row["PDB ID"]
        assembly_id = row["Assembly ID"]
        chain_id = row["Auth Asym ID"]

        if not entry_id or not assembly_id or not chain_id:
            continue

        count += 1
        print(f"\n[{count}] {entry_id} (Assembly {assembly_id}, Chaîne {chain_id})")
        print("-" * 60)

        try:
            obj_name = f"{entry_id}_assembly{assembly_id}"

            # Supprimer l'objet s'il existe déjà
            if obj_name in cmd.get_names():
                cmd.delete(obj_name)

            # Vérifier si le fichier existe avant de télécharger
            structure_file = f"{entry_id}-assembly{assembly_id}.cif"
            if os.path.exists(structure_file):
                print(f"✓ Structure déjà présente: {structure_file}, chargement depuis le fichier local")
                cmd.load(structure_file, obj_name)
            else:
                print(f"Téléchargement de la structure {entry_id}...")
                cmd.do(f"fetch_mmcif {entry_id}, {obj_name}, {assembly_id}")
            
            cmd.remove(f"{obj_name} and solvent")
            print(f"✓ Structure chargée")

            # Configuration visuelle
            cmd.hide("everything", obj_name)
            cmd.show("cartoon", obj_name)
            cmd.color("cyan", obj_name)
            cmd.show("sticks", f"{obj_name} and organic")
            cmd.show("nb_spheres", f"{obj_name} and inorganic")

            # Vérifier la sélection du lobe C
            lobe_c_target = f"{obj_name} and chain {chain_id} and resi {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END} and name CA"
            n_atoms_target = cmd.count_atoms(lobe_c_target)

            if n_atoms_target < 20:
                print(f"⚠ Peu d'atomes trouvés dans le lobe C ({n_atoms_target}). Utilisation de tous les C-alpha.")
                lobe_c_target = f"{obj_name} and chain {chain_id} and name CA"
                n_atoms_target = cmd.count_atoms(lobe_c_target)

            if n_atoms_target == 0:
                print(f"⚠ Aucun atome trouvé dans {entry_id}. Structure peut être incomplète.")
                results.append({
                    'PDB_ID': entry_id,
                    'Chain': 'ERROR',
                    'N_CA_aligned': 0,
                    'RMSD': 'N/A',
                    'Status': 'ERROR'
                })
                continue

            # Superposition finale
            print(f"Superposition de {n_atoms_target} C-alpha...")
            alignment = cmd.align(
                lobe_c_target,
                lobe_c_ref,
                cycles=10,
                cutoff=2.0,
                transform=1,
                quiet=0
            )

            rmsd = alignment[0]
            n_aligned = alignment[1]

            print(f"✓ Résultats finaux:")
            print(f"  RMSD: {rmsd:.2f} Å")
            print(f"  C-alpha alignés: {n_aligned}")

            # Évaluation détaillée
            if rmsd > 4.0:
                print(f"  ⚠ RMSD élevé - Vérifier manuellement!")
                status = "HIGH_RMSD"
            elif rmsd > 2.5:
                print(f"  ⚠ RMSD modéré - Acceptable mais vérifier")
                status = "MODERATE"
            elif rmsd < 2.0:
                print(f"  ✓ Excellente superposition!")
                status = "EXCELLENT"
            else:
                print(f"  ✓ Bonne superposition")
                status = "GOOD"

            if n_aligned < 50:
                print(f"  ⚠ Peu d'atomes alignés - Structures très différentes?")
            elif n_aligned > 100:
                print(f"  ✓ Bon nombre d'atomes alignés")

            # Sauvegarder les résultats
            results.append({
                'PDB_ID': entry_id,
                'Chain': chain_id,
                'N_CA_aligned': n_aligned,
                'RMSD': f"{rmsd:.2f}",
                'Status': status
            })

            # Sauvegarder la structure superposée au format mmcif
            cmd.save(f"{entry_id}_aligned.cif", obj_name)
            print(f"  💾 Sauvegardé: {entry_id}_aligned.cif")

        except Exception as e:
            print(f"✗ Erreur: {e}")
            results.append({
                'PDB_ID': entry_id,
                'Chain': 'ERROR',
                'N_CA_aligned': 0,
                'RMSD': 'N/A',
                'Status': 'ERROR'
            })

print("\n" + "=" * 60)
print("RÉSUMÉ DES SUPERPOSITIONS")
print("=" * 60)
print(f"\n{'PDB ID':<10} {'Chaîne':<10} {'N C-alpha':<15} {'RMSD (Å)':<10} {'Status':<12}")
print("-" * 60)
for result in results:
    print(f"{result['PDB_ID']:<10} {result['Chain']:<10} {result['N_CA_aligned']:<15} {result['RMSD']:<10} {result['Status']:<12}")

# Sauvegarder les résultats dans un fichier CSV
output_csv = "superposition_results.csv"
with open(output_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['PDB_ID', 'Chain', 'N_CA_aligned', 'RMSD', 'Status'])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✓ Résultats sauvegardés dans {output_csv}")

# Statistiques
n_total = len(results)
n_excellent = sum(1 for r in results if r.get('Status') == 'EXCELLENT')
n_good = sum(1 for r in results if r.get('Status') == 'GOOD')
n_moderate = sum(1 for r in results if r.get('Status') == 'MODERATE')
n_high_rmsd = sum(1 for r in results if r.get('Status') == 'HIGH_RMSD')
n_errors = sum(1 for r in results if r.get('Status') == 'ERROR')

print("\n" + "=" * 60)
print("STATISTIQUES")
print("=" * 60)
print(f"Total de structures: {n_total}")
print(f"  Excellent (RMSD < 2.0 Å): {n_excellent}")
print(f"  Bon (RMSD 2.0-2.5 Å): {n_good}")
print(f"  Modéré (RMSD 2.5-4.0 Å): {n_moderate}")
print(f"  RMSD élevé (> 4.0 Å): {n_high_rmsd}")
print(f"  Erreurs: {n_errors}")

print("\n" + "=" * 60)
print("TRAITEMENT TERMINÉ ✨")
print("=" * 60)


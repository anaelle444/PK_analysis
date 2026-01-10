#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour la superposition de quelques structures ALK sur PKACA
À utiliser pour vérifier que tout fonctionne avant de traiter toutes les structures
"""

import csv
from pymol import cmd

# Limiter le nombre de structures à tester
MAX_STRUCTURES = 3

# Fichier CSV
csv_file = "smaller5.csv"  # ou "rcsb_pdb_custom_report_20260109152453.csv"

# Structure de référence PKACA (P17612)
reference_pdb = "1ATP"
reference_chain = "E"

# Positions connues du LOBE C pour PKACA (1ATP chaîne E)
# Basées sur la structure des kinases: le lobe C commence après le hinge (~120-130)
# et s'étend jusqu'à la fin du domaine catalytique (~300)
PKACA_LOBE_C_START = 127
PKACA_LOBE_C_END = 300

print("="*60)
print("TEST DE SUPERPOSITION - MODE LIMITÉ")
print("="*60)
print(f"Alignement sur le LOBE C uniquement:")
print(f"  Référence PKACA ({reference_pdb} chaîne {reference_chain})")
print(f"  Lobe C: résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END}")
print("="*60)

# Charger la structure de référence
print(f"\nChargement de la structure de référence {reference_pdb}...")
try:
    # Utiliser fetch_mmcif comme commande PyMOL (pas cmd.fetch_mmcif)
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

# Traiter quelques structures
print("\n" + "="*60)
print("TRAITEMENT DES STRUCTURES ALK")
print("="*60)

count = 0
results = []

with open(csv_file, newline='') as f:
    lines = f.readlines()
    reader = csv.DictReader(lines[1:])
    
    for row in reader:
        if count >= MAX_STRUCTURES:
            break
            
        entry_id = row["Entry ID"]
        if not entry_id:
            continue
        
        count += 1
        print(f"\n[{count}/{MAX_STRUCTURES}] {entry_id}")
        print("-"*60)
        
        try:
            obj_name = f"{entry_id}_assembly1"
            
            # Charger l'assemblage biologique avec fetch_mmcif
            cmd.do(f"fetch_mmcif {entry_id}, {obj_name}, 1")
            cmd.remove(f"{obj_name} and solvent")
            
            # Identifier la chaîne principale
            chains = cmd.get_chains(obj_name)
            print(f"Chaînes disponibles: {', '.join(chains)}")
            
            target_chain = None
            max_residues = 0
            
            for chain in chains:
                n_res = cmd.count_atoms(f"{obj_name} and chain {chain} and polymer.protein and name CA")
                print(f"  Chaîne {chain}: {n_res} résidus")
                if n_res > max_residues and n_res > 200:
                    max_residues = n_res
                    target_chain = chain
            
            if not target_chain:
                target_chain = chains[0]
                max_residues = cmd.count_atoms(f"{obj_name} and chain {target_chain} and polymer.protein and name CA")
            
            print(f"➜ Chaîne sélectionnée: {target_chain} ({max_residues} résidus)")
            
            # Stratégie de superposition optimisée sur le LOBE C uniquement
            print("\nÉtape 1: Alignement initial sur toute la protéine...")
            global_sel = f"{obj_name} and chain {target_chain} and name CA"
            ref_global = f"{reference_pdb}_ref and chain {reference_chain} and name CA"
            
            pre_align = cmd.align(
                global_sel,
                ref_global,
                cycles=0,
                transform=1,
                quiet=1
            )
            print(f"  Pré-alignement global: RMSD={pre_align[0]:.2f} Å, {pre_align[1]} atomes")
            
            # Étape 2: Identifier la région du lobe C dans la structure cible
            print(f"\nÉtape 2: Identification de la région correspondant au lobe C...")
            print(f"  Référence PKACA lobe C: résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END}")
            
            # Tester plusieurs régions possibles pour le lobe C dans la cible
            lobe_ranges = [
                (PKACA_LOBE_C_START, PKACA_LOBE_C_END),           # Même numérotation
                (PKACA_LOBE_C_START - 30, PKACA_LOBE_C_END - 30), # Décalage -30
                (PKACA_LOBE_C_START + 30, PKACA_LOBE_C_END + 30), # Décalage +30
                (120, 280),  # Région générique du lobe C pour kinases
                (140, 300),  # Région alternative
                (100, 250),  # Région plus courte
            ]
            
            best_rmsd = 999
            best_alignment = None
            best_range = None
            best_n_atoms = 0
            
            for start, end in lobe_ranges:
                lobe_c_target = f"{obj_name} and chain {target_chain} and resi {start}-{end} and name CA"
                
                n_target = cmd.count_atoms(lobe_c_target)
                
                # Nécessite au moins 40 résidus pour un lobe C
                if n_target > 40:
                    try:
                        test_align = cmd.align(
                            lobe_c_target,
                            lobe_c_ref,  # TOUJOURS aligner sur le lobe C de la référence
                            cycles=5,
                            transform=0,  # Ne pas transformer pour ce test
                            quiet=1
                        )
                        
                        # Garder le meilleur alignement (RMSD faible ET bon nombre d'atomes)
                        if test_align[1] > 40:  # Au moins 40 atomes alignés
                            quality_score = test_align[0] - (test_align[1] / 100.0)  # Favorise plus d'atomes
                            best_score = best_rmsd - (best_n_atoms / 100.0)
                            
                            if quality_score < best_score:
                                best_rmsd = test_align[0]
                                best_alignment = test_align
                                best_range = (start, end)
                                best_n_atoms = test_align[1]
                                print(f"  ✓ Essai resi {start:3d}-{end:3d}: RMSD={test_align[0]:.2f} Å, {test_align[1]:3d} atomes alignés")
                    except Exception as e:
                        pass
            
            # Si aucune région spécifique ne fonctionne
            if best_range is None:
                print(f"  ⚠ Aucune région optimale trouvée, utilisation de résidus génériques...")
                best_range = (120, 300)
                lobe_c_target = f"{obj_name} and chain {target_chain} and resi {best_range[0]}-{best_range[1]} and name CA"
            else:
                print(f"\n  ✓✓ Meilleure région identifiée: {best_range[0]}-{best_range[1]}")
                lobe_c_target = f"{obj_name} and chain {target_chain} and resi {best_range[0]}-{best_range[1]} and name CA"
            
            # Étape 3: Superposition FINALE optimisée sur le LOBE C UNIQUEMENT
            print(f"\nÉtape 3: Superposition finale sur le LOBE C...")
            print(f"  Cible: chaîne {target_chain} résidus {best_range[0]}-{best_range[1]}")
            print(f"  Référence: chaîne {reference_chain} résidus {PKACA_LOBE_C_START}-{PKACA_LOBE_C_END}")
            
            alignment = cmd.align(
                lobe_c_target,
                lobe_c_ref,  # LOBE C de la référence UNIQUEMENT
                cycles=10,     # Plus de cycles pour optimiser
                cutoff=2.0,    # Exclure les outliers
                transform=1,   # Transformer la structure
                quiet=0        # Afficher les détails
            )
            
            rmsd = alignment[0]
            n_aligned = alignment[1]
            
            print(f"\n✓ Résultats finaux:")
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
            
            results.append({
                'PDB_ID': entry_id,
                'Chain': target_chain,
                'N_CA_aligned': n_aligned,
                'RMSD': f"{rmsd:.2f}",
                'Status': status
            })
            
            # Sauvegarder
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

# Résumé
print("\n" + "="*60)
print("RÉSUMÉ")
print("="*60)
print(f"\n{'PDB ID':<10} {'Chaîne':<10} {'N C-alpha':<15} {'RMSD (Å)':<10} {'Status':<12}")
print("-"*60)
for r in results:
    print(f"{r['PDB_ID']:<10} {r['Chain']:<10} {r['N_CA_aligned']:<15} {r['RMSD']:<10} {r['Status']:<12}")

# Configuration visuelle
print("\n" + "="*60)
print("Configuration de l'affichage...")
print("="*60)
cmd.hide("everything")
cmd.show("cartoon", "polymer.protein")
cmd.show("sticks", "organic and not polymer")
cmd.show("nb_spheres", "inorganic")
cmd.color("green", f"{reference_pdb}_ref")
cmd.color("cyan", "*assembly1")
cmd.bg_color("white")

print("\n✓ TERMINÉ!")
print("\nConseils:")
print("  - Vérifiez visuellement les superpositions")
print("  - Les structures sont colorées: référence=vert, ALK=cyan")
print("  - Si les résultats sont bons, utilisez open-csv.py pour toutes les structures")

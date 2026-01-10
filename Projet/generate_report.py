#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un rapport automatique des résultats de superposition
À exécuter HORS de PyMOL (Python normal)
"""

import csv
import os
from datetime import datetime

def generate_report():
    """Génère un rapport Markdown à partir des résultats de superposition"""
    
    results_file = "superposition_results.csv"
    output_file = "rapport_resultats.md"
    
    if not os.path.exists(results_file):
        print(f"❌ Fichier {results_file} non trouvé!")
        print("   Lancez d'abord le script open-csv.py dans PyMOL")
        return
    
    # Lire les résultats
    results = []
    with open(results_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    # Statistiques
    total = len(results)
    errors = sum(1 for r in results if r['Chain'] == 'ERROR')
    success = total - errors
    
    good = sum(1 for r in results if r['Chain'] != 'ERROR' and float(r['RMSD']) < 2.0)
    acceptable = sum(1 for r in results if r['Chain'] != 'ERROR' and 2.0 <= float(r['RMSD']) < 4.0)
    poor = sum(1 for r in results if r['Chain'] != 'ERROR' and float(r['RMSD']) >= 4.0)
    
    avg_rmsd = sum(float(r['RMSD']) for r in results if r['Chain'] != 'ERROR') / max(success, 1)
    avg_aligned = sum(int(r['N_CA_aligned']) for r in results if r['Chain'] != 'ERROR') / max(success, 1)
    
    # Générer le rapport
    report = []
    report.append("# Rapport de Superposition des Structures ALK sur PKACA")
    report.append("")
    report.append(f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Résumé
    report.append("## Résumé")
    report.append("")
    report.append(f"- **Nombre total de structures:** {total}")
    report.append(f"- **Succès:** {success} ({success*100/total:.1f}%)")
    report.append(f"- **Échecs:** {errors} ({errors*100/total:.1f}%)")
    report.append("")
    report.append("### Qualité des superpositions")
    report.append("")
    report.append(f"- **Excellentes** (RMSD < 2 Å): {good} ({good*100/max(success,1):.1f}%)")
    report.append(f"- **Acceptables** (2 ≤ RMSD < 4 Å): {acceptable} ({acceptable*100/max(success,1):.1f}%)")
    report.append(f"- **Problématiques** (RMSD ≥ 4 Å): {poor} ({poor*100/max(success,1):.1f}%)")
    report.append("")
    report.append(f"- **RMSD moyen:** {avg_rmsd:.2f} Å")
    report.append(f"- **Nombre moyen de C-alpha alignés:** {avg_aligned:.0f}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Tableau complet
    report.append("## Tableau des Résultats")
    report.append("")
    report.append("| PDB ID | Chaîne utilisée | Nb. C-alpha superposés | RMSD (Å) | Qualité |")
    report.append("|--------|-----------------|------------------------|----------|---------|")
    
    for r in results:
        if r['Chain'] == 'ERROR':
            quality = "❌ Échec"
        else:
            rmsd = float(r['RMSD'])
            if rmsd < 2.0:
                quality = "✅ Excellente"
            elif rmsd < 4.0:
                quality = "⚠️ Acceptable"
            else:
                quality = "❌ Problématique"
        
        report.append(f"| {r['PDB_ID']} | {r['Chain']} | {r['N_CA_aligned']} | {r['RMSD']} | {quality} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Cas problématiques
    report.append("## Cas Problématiques")
    report.append("")
    
    problematic = [r for r in results if r['Chain'] == 'ERROR' or 
                   (r['Chain'] != 'ERROR' and float(r['RMSD']) >= 4.0)]
    
    if problematic:
        report.append("Les structures suivantes présentent des problèmes de superposition:")
        report.append("")
        
        for r in problematic:
            report.append(f"### {r['PDB_ID']}")
            if r['Chain'] == 'ERROR':
                report.append("- **Problème:** Échec du chargement ou de la superposition")
                report.append("- **Cause possible:** Structure non disponible, format incorrect, ou absence de domaine kinase")
            else:
                report.append(f"- **RMSD:** {r['RMSD']} Å (élevé)")
                report.append(f"- **C-alpha alignés:** {r['N_CA_aligned']}")
                report.append("- **Causes possibles:**")
                report.append("  - Structure incomplète (domaine C-terminal manquant)")
                report.append("  - Conformation très différente (forme inactive/active)")
                report.append("  - Mauvaise identification de la chaîne de la kinase")
                report.append("  - Présence de domaines supplémentaires non homologues")
            report.append("")
    else:
        report.append("✅ Aucun cas problématique détecté. Toutes les superpositions sont de bonne qualité.")
        report.append("")
    
    report.append("---")
    report.append("")
    
    # Recommandations
    report.append("## Recommandations")
    report.append("")
    report.append("### Pour le rapport final")
    report.append("")
    report.append("1. **Vérification visuelle obligatoire** dans PyMOL:")
    report.append("   ```python")
    report.append("   # Charger quelques structures")
    report.append("   load 1ATP_ref.cif")
    report.append("   load 2KUP_aligned.cif")
    report.append("   ")
    report.append("   # Visualiser")
    report.append("   hide everything")
    report.append("   show cartoon, polymer")
    report.append("   color green, 1ATP_ref")
    report.append("   color cyan, 2KUP_aligned")
    report.append("   ```")
    report.append("")
    report.append("2. **Figure à inclure dans le rapport:**")
    report.append("   - Vue d'ensemble de toutes les structures superposées (ribbon)")
    report.append("   - Zoom sur le lobe C pour montrer la qualité de l'alignement")
    report.append("   - Légende claire identifiant la référence et quelques structures ALK")
    report.append("")
    report.append("3. **Discussion des cas problématiques:**")
    
    if problematic:
        report.append(f"   - {len(problematic)} structures nécessitent une attention particulière")
        report.append("   - Expliquer pourquoi certaines structures ont un RMSD élevé")
        report.append("   - Proposer des hypothèses (structure partielle, domaines additionnels, etc.)")
    else:
        report.append("   - Toutes les structures se superposent correctement")
        report.append("   - Discuter de l'homologie structurale entre ALK et PKACA")
    
    report.append("")
    report.append("4. **Points forts à mentionner:**")
    report.append(f"   - {good} structures avec excellente superposition (RMSD < 2 Å)")
    report.append(f"   - RMSD moyen de {avg_rmsd:.2f} Å indique une bonne conservation structurale")
    report.append(f"   - {avg_aligned:.0f} C-alpha alignés en moyenne confirme l'homologie")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("## Fichiers Générés")
    report.append("")
    report.append("### Dossier Projet/")
    report.append("- Scripts Python pour PyMOL")
    report.append("- Fichier CSV source")
    report.append("- Fichier de résultats CSV")
    report.append("")
    report.append("### Dossier Super/")
    report.append(f"- 1 structure de référence PKACA (1ATP_ref.cif)")
    report.append(f"- {success} structures ALK superposées (*_aligned.cif)")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Rapport généré automatiquement par generate_report.py*")
    
    # Écrire le rapport
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("="*60)
    print("RAPPORT GÉNÉRÉ AVEC SUCCÈS")
    print("="*60)
    print(f"\n📄 Fichier créé: {output_file}")
    print(f"\n📊 Statistiques:")
    print(f"   - Structures traitées: {total}")
    print(f"   - Succès: {success} ({success*100/total:.1f}%)")
    print(f"   - RMSD moyen: {avg_rmsd:.2f} Å")
    print(f"   - C-alpha alignés (moyenne): {avg_aligned:.0f}")
    print(f"\n✅ Excellentes superpositions: {good}")
    print(f"⚠️  Acceptables: {acceptable}")
    print(f"❌ Problématiques: {poor}")
    
    if errors > 0:
        print(f"\n⚠️  {errors} structures n'ont pas pu être traitées")
    
    print(f"\n💡 Consultez {output_file} pour le rapport détaillé")
    print("="*60)

if __name__ == "__main__":
    generate_report()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour organiser les fichiers pour le rendu final
Crée le dossier Super/ et y copie toutes les structures alignées
"""

import os
import shutil
import glob

# Créer le dossier Super s'il n'existe pas
super_dir = "../Super"
if not os.path.exists(super_dir):
    os.makedirs(super_dir)
    print(f"✓ Dossier {super_dir} créé")
else:
    print(f"✓ Dossier {super_dir} existe déjà")

# Copier la structure de référence
reference_files = ["1ATP_ref.cif", "1ATP-assembly1.cif"]
for ref_file in reference_files:
    if os.path.exists(ref_file):
        dest = os.path.join(super_dir, ref_file)
        shutil.copy(ref_file, dest)
        print(f"✓ Copié: {ref_file} → Super/")
        break
else:
    print("⚠ Structure de référence non trouvée (1ATP_ref.cif)")

# Copier toutes les structures alignées
aligned_files = glob.glob("*_aligned.cif")
count = 0
for aligned_file in aligned_files:
    dest = os.path.join(super_dir, aligned_file)
    shutil.copy(aligned_file, dest)
    count += 1

print(f"✓ {count} structures alignées copiées dans Super/")

# Vérifier le contenu
files_in_super = os.listdir(super_dir)
print(f"\n✓ Contenu de Super/: {len(files_in_super)} fichiers")
print(f"  Fichiers: {', '.join(sorted(files_in_super)[:5])}...")

print("\n" + "="*60)
print("Organisation terminée!")
print("="*60)
print(f"Le dossier Super/ contient toutes les structures superposées")
print(f"Vous pouvez maintenant créer votre ZIP pour le rendu")

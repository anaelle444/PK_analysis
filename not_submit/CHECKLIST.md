# CHECKLIST AVANT DE LANCER LE PROJET

## ✅ Vérifications préalables

### 1. Extension fetch_mmcif installée
```bash
# Dans PyMOL, taper:
help fetch_mmcif
```
➜ Si l'aide s'affiche, c'est OK ✓

### 2. Fichier CSV présent
- [ ] `rcsb_pdb_custom_report_20260109152453.csv` existe dans le dossier Projet/

### 3. Se placer dans le bon dossier
```bash
# Dans PyMOL:
cd /home/najat/Master_bioinformatique/M2/Structure_medicament/projet_stefano/PK_analysis/Projet
pwd  # Vérifier le chemin
```

## 📝 Étapes à suivre

### Étape 1: Test avec quelques structures (OBLIGATOIRE)
```bash
# Dans PyMOL:
run test_superposition.py
```

**Vérifications:**
- [ ] 3 structures se chargent correctement
- [ ] Les RMSD sont < 4 Å
- [ ] Le nombre de C-alpha alignés est > 50
- [ ] Les structures sont visibles et bien superposées (référence=vert, ALK=cyan)

**En cas de problème:**
- Si RMSD > 4 Å : normal pour certaines structures, à documenter dans le rapport
- Si erreur de chargement : vérifier que fetch_mmcif fonctionne
- Si pas d'alignement : ajuster les résidus du lobe C

### Étape 2: Ajuster les paramètres si nécessaire

#### Structure de référence PKACA
Par défaut: `1ATP`, chaîne `E`

Pour vérifier/changer, éditer dans les scripts:
```python
reference_pdb = "1ATP"      # Modifier si nécessaire
reference_chain = "E"       # Modifier si nécessaire
```

**Autres structures PKACA possibles:**
- 1ATP : Complexe avec ATP (recommandé)
- 1CDK : Complexe avec inhibiteur
- 1JBP : Forme active
- 4WB5 : Haute résolution

#### Région du lobe C
Par défaut: résidus 160-300

Si besoin d'ajuster:
```python
lobe_c_ref = f"{reference_pdb}_ref and chain {reference_chain} and resi 160-300 and name CA"
```

**Pour trouver les bons résidus:**
1. Charger la structure de référence dans PyMOL
2. Identifier visuellement le lobe C (partie C-terminale, contient hélices alpha)
3. Utiliser `iterate (sele and name CA), print(resi)` pour voir les numéros

### Étape 3: Traitement complet
Une fois satisfait des tests:
```bash
# Dans PyMOL:
run open-csv.py
```

**⏱ Temps estimé:** 
- Quelques minutes à quelques dizaines de minutes selon le nombre de structures
- Surveillez la console pour les messages d'erreur

**Sorties attendues:**
- [ ] Fichiers `*_aligned.cif` créés (un par structure)
- [ ] Fichier `superposition_results.csv` créé
- [ ] Messages de succès dans la console

### Étape 4: Vérification des résultats
```bash
# Vérifier le fichier de résultats
cat superposition_results.csv
```

**Points à vérifier:**
- [ ] Toutes les structures du CSV sont traitées
- [ ] Pas trop d'erreurs (quelques-unes sont acceptables)
- [ ] RMSD majoritairement < 4 Å
- [ ] N_CA_aligned majoritairement > 50

### Étape 5: Vérification visuelle
Dans PyMOL après l'exécution:
- [ ] Structures superposées visibles
- [ ] Lobes C bien alignés
- [ ] Pas de superpositions aberrantes

**Commandes utiles:**
```python
# Afficher seulement la référence et une structure
disable all
enable 1ATP_ref
enable 2KUP_assembly1

# Zoomer sur le lobe C
zoom chain E and resi 160-300

# Mesurer RMSD entre deux structures
rms_cur 2KUP_assembly1 and chain A, 1ATP_ref and chain E
```

### Étape 6: Organisation des fichiers pour le rendu

#### Option A: Avec Python (hors PyMOL)
```bash
cd /home/najat/Master_bioinformatique/M2/Structure_medicament/projet_stefano/PK_analysis/Projet
python3 organize_for_submission.py
```

#### Option B: Manuellement
```bash
# Créer le dossier Super
mkdir -p ../Super

# Copier la référence
cp 1ATP_ref.cif ../Super/ 
# ou
cp 1ATP-assembly1.cif ../Super/

# Copier toutes les structures alignées
cp *_aligned.cif ../Super/
```

**Vérification:**
```bash
ls -lh ../Super/
# Doit contenir: 1ATP_ref.cif + toutes les *_aligned.cif
```

### Étape 7: Préparation du rapport

#### Tableau des résultats
À créer à partir de `superposition_results.csv`:

```
PDB ID | Chaîne utilisée | Nb. C-alpha superposés | RMSD (Å)
-------|-----------------|------------------------|----------
2KUP   | A               | 142                    | 2.34
2KUQ   | A               | 138                    | 2.56
...
```

#### Figure des superpositions
Dans PyMOL:
```python
# Configurer la vue
hide everything
show cartoon, polymer
color green, 1ATP_ref
spectrum count, rainbow, *assembly1
bg_color white

# Orienter la vue
orient
zoom chain E and resi 160-300

# Capturer l'image
png superposition_figure.png, dpi=300, ray=1
```

#### Points à documenter
- [ ] Structures qui n'ont pas pu être superposées (RMSD > 4 ou erreurs)
- [ ] Raisons possibles (structure incomplète, domaines manquants, etc.)
- [ ] Difficultés rencontrées
- [ ] Solutions apportées

### Étape 8: Créer le ZIP final
```bash
cd /home/najat/Master_bioinformatique/M2/Structure_medicament/projet_stefano/PK_analysis

# Vérifier le contenu
ls Projet/
ls Super/

# Créer l'archive
zip -r rendu_groupe5.zip Projet/ Super/ rapport.pdf

# Vérifier l'archive
unzip -l rendu_groupe5.zip
```

## 🚨 Problèmes fréquents et solutions

### Erreur: "fetch_mmcif not found"
**Solution:** 
```bash
# Vérifier l'installation
ls ${HOME}/PROGRAMS/PYMOL_SCRIPTS/fetch_mmcif.py

# Vérifier .pymolrc
cat ~/.pymolrc | grep fetch_mmcif

# Relancer PyMOL
```

### Erreur: "KeyError: 'Entry ID'"
**Solution:** Déjà gérée dans le script (lecture ligne 2 du CSV)

### RMSD très élevés partout
**Causes possibles:**
- Mauvaise structure de référence
- Mauvaise région du lobe C
- Mauvaise chaîne sélectionnée

**Solution:** Vérifier visuellement une superposition dans PyMOL

### Script très lent
**Normal** si beaucoup de structures. Pour accélérer:
- Tester d'abord avec `test_superposition.py`
- Traiter par lots si nécessaire

### Pas assez d'espace disque
Chaque structure fait ~1-10 Mo. Prévoir au moins 500 Mo libres.

## 📊 Résultats attendus

### Bonnes superpositions (attendu pour la majorité)
- RMSD: 1-3 Å
- N_CA_aligned: 100-150
- Visuellement: lobes C bien alignés

### Superpositions acceptables
- RMSD: 3-4 Å
- N_CA_aligned: 50-100
- À commenter dans le rapport

### Échecs (normaux pour quelques structures)
- RMSD: > 4 Å
- N_CA_aligned: < 50
- À documenter et expliquer dans le rapport

## ✅ Checklist finale avant rendu

- [ ] Tous les scripts Python sont dans Projet/
- [ ] Le fichier CSV est dans Projet/
- [ ] Toutes les structures superposées sont dans Super/
- [ ] La structure de référence PKACA est dans Super/
- [ ] Le rapport PDF est complété avec:
  - [ ] Description de la stratégie
  - [ ] Tableau des résultats
  - [ ] Figure des superpositions
  - [ ] Discussion des échecs/difficultés
- [ ] Le ZIP contient: Projet/ + Super/ + rapport.pdf
- [ ] Le ZIP est testé (extraction et vérification du contenu)

## 💡 Conseils finaux

1. **Commencez tôt** - Certaines structures peuvent poser problème
2. **Testez d'abord** - Utilisez `test_superposition.py`
3. **Documentez tout** - Notez les problèmes rencontrés
4. **Vérifiez visuellement** - Ne vous fiez pas qu'aux chiffres
5. **Demandez de l'aide** - Si quelque chose ne fonctionne pas

Bonne chance ! 🚀

# Projet de Superposition de Structures ALK sur PKACA

## Description
Ce projet permet de charger automatiquement les assemblages biologiques de structures PDB contenant la protéine kinase ALK (Q9UM73) et de les superposer sur une structure de référence PKACA (P17612).

## Fichiers du projet

### Scripts Python pour PyMOL
- **`test_superposition.py`** : Script de test qui traite seulement 3 structures (recommandé pour débuter)
- **`open-csv.py`** : Script principal qui traite toutes les structures du CSV
- **`import_csv.py`** : (À vérifier/adapter selon vos besoins)

### Fichiers de données
- **`rcsb_pdb_custom_report_20260109152453.csv`** : Liste complète des structures PDB
- **`smaller5.csv`** : Liste réduite pour les tests (si disponible)

## Prérequis

### Installation de l'extension fetch_mmcif
L'extension `fetch_mmcif` doit être installée dans PyMOL. Si ce n'est pas déjà fait :

```bash
mkdir -p ${HOME}/PROGRAMS/PYMOL_SCRIPTS
# Télécharger fetch_mmcif.py dans ce dossier
```

Ajouter dans `~/.pymolrc` :
```python
cmd.run("${HOME}/PROGRAMS/PYMOL_SCRIPTS/fetch_mmcif.py")
```

### Vérification
Dans PyMOL, taper :
```
help fetch_mmcif
```
Si l'aide s'affiche, l'extension est correctement installée.

## Utilisation

### 1. Test initial (RECOMMANDÉ)
Commencez par tester avec quelques structures :

```bash
# Dans PyMOL
cd /home/najat/Master_bioinformatique/M2/Structure_medicament/projet_stefano/PK_analysis/Projet
run test_superposition.py
```

Ce script :
- Charge 3 structures seulement
- Affiche des informations détaillées
- Permet de vérifier que tout fonctionne correctement

### 2. Traitement complet
Une fois le test validé, lancez le traitement complet :

```bash
# Dans PyMOL
run open-csv.py
```

Ce script :
- Parcourt tout le fichier CSV
- Charge chaque assemblage biologique (assembly 1)
- Identifie automatiquement la chaîne de la kinase
- Superpose sur le lobe C de PKACA
- Sauvegarde les structures alignées au format mmcif
- Génère un fichier de résultats CSV

## Sorties générées

### Fichiers de structures superposées
- `<PDB_ID>_aligned.cif` : Structures superposées au format mmcif
- À copier dans le dossier `Super/` pour le rendu final

### Fichier de résultats
- `superposition_results.csv` : Tableau récapitulatif avec :
  - PDB ID
  - Chaîne utilisée
  - Nombre de C-alpha superposés
  - RMSD (Å)

## Paramètres ajustables

### Structure de référence PKACA
Par défaut : `1ATP`, chaîne `E`

Pour changer, modifier dans le script :
```python
reference_pdb = "1ATP"  # Autre structure PDB de PKACA
reference_chain = "E"   # Chaîne contenant PKACA
```

### Région du lobe C
Par défaut : résidus 160-300

Pour ajuster :
```python
lobe_c_ref = f"{reference_pdb}_ref and chain {reference_chain} and resi 160-300 and name CA"
```

### Critères d'évaluation
- **RMSD > 4 Å** : Avertissement affiché (superposition problématique)
- **N_aligned < 50** : Avertissement affiché (structure incomplète)

## Vérification des résultats

### Visuelle
Dans PyMOL après l'exécution :
- Structure de référence : **vert**
- Structures ALK : **arc-en-ciel** (spectrum)
- Représentation : cartoon pour les protéines, sticks pour les ligands

### Quantitative
Vérifier dans le tableau de résultats :
1. **RMSD** : doit être < 4 Å (idéalement < 2 Å)
2. **N C-alpha alignés** : doit être > 50 (idéalement > 100)

## Problèmes courants

### Erreur "KeyError: 'Entry ID'"
- Le CSV a des en-têtes multiples
- Solution déjà implémentée dans le script (lecture à partir de la ligne 2)

### Erreur "fetch_mmcif not found"
- L'extension n'est pas installée ou pas chargée
- Vérifier le fichier `~/.pymolrc`
- Relancer PyMOL

### RMSD très élevé (> 4 Å)
- Structure non-similaire à PKACA
- Lobe C mal défini pour cette structure
- Vérifier visuellement la superposition

### Peu d'atomes superposés
- Structure incomplète
- Région du lobe C mal définie
- Le script bascule automatiquement sur tous les C-alpha

## Organisation pour le rendu

```
Projet/
├── open-csv.py
├── test_superposition.py
├── rcsb_pdb_custom_report_20260109152453.csv
└── superposition_results.csv

Super/
├── 1ATP_ref.cif  (structure de référence PKACA)
├── 2KUP_aligned.cif
├── 2KUQ_aligned.cif
├── 2YS5_aligned.cif
└── ... (toutes les structures superposées)
```

## Stratégie du projet

1. **Recherche PDB** : Structures contenant ALK (Q9UM73), assemblages biologiques uniquement
2. **Référence** : PKACA (P17612) - structure 1ATP
3. **Superposition** : 
   - Région ciblée : Lobe C (résidus ~160-300)
   - Méthode : `cmd.align()` avec C-alpha uniquement
   - Cycles d'optimisation : 5
4. **Validation** :
   - Visuelle : vérification dans PyMOL
   - Quantitative : RMSD et nombre d'atomes alignés

## Auteurs
- Projet M2 Bioinformatique
- Groupe 5 - ALK (Q9UM73)

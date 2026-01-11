```markdown
# Projet de Superposition de Structures ALK sur PKACA

## Description
Ce projet permet de charger automatiquement les assemblages biologiques de structures PDB contenant la protéine kinase ALK (Q9UM73) et de les superposer sur une structure de référence PKACA (P17612, structure 4WB8).

## Fichiers du projet

### Scripts Python pour PyMOL
- **`open_pdb_csv.py`** : Script principal qui charge et superpose toutes les structures ALK sur PKACA
- **`visualisation.py`** : Script de visualisation pour mettre en évidence les régions d'alignement et identifier les structures problématiques

### Fichiers de données
- **`rcsb_pdb_custom_report_20260110111300_new.csv`** : Liste complète des structures PDB contenant ALK
- **`superposition_results.csv`** : Résultats générés par le script principal (RMSD, nombre de C-alpha alignés, statut)

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

### 1. Superposition des structures

```bash
# Lancer PyMOL
pymol

# Dans PyMOL, exécuter le script principal
run open_pdb_csv.py
```

Ce script :
- Charge la structure de référence 4WB8 (PKACA humaine)
- Parcourt le fichier CSV contenant toutes les structures ALK
- Pour chaque structure :
  - Télécharge l'assemblage biologique 1 (ou charge depuis le cache local)
  - Supprime les molécules d'eau et solvants
  - Superpose le lobe C (résidus 127-350) sur celui de PKACA
  - Calcule le RMSD et le nombre de C-alpha alignés
  - Sauvegarde la structure superposée au format mmCIF
- Génère un fichier CSV avec tous les résultats
- Affiche des statistiques détaillées

**Note :** Pour limiter le nombre de structures traitées (utile pour les tests), décommenter et ajuster dans le script :
```python
MAX_STRUCTURES = 10  # Traiter seulement 10 structures
```

### 2. Visualisation des résultats

Après avoir exécuté le script principal, chargez le script de visualisation :

```bash
# Dans PyMOL
run visualisation.py
```

Ce script fournit trois fonctions :

#### a) Mise en évidence du lobe C et de la région charnière
```python
highlight_lobes
```
- Colore le lobe C en **saumon** (résidus 1202-1383)
- Colore la région charnière en **orange** (résidus 1197-1201)
- Permet de visualiser clairement la région utilisée pour l'alignement

#### b) Coloration des structures problématiques
```python
color_bad_rmsd("superposition_results.csv")
```
- Colore en **marron** les structures avec RMSD > 4 Å
- Colore en **gris** les structures en erreur
- S'exécute automatiquement au chargement du script

#### c) Isolation des structures problématiques
```python
isoler_mauvais
```
- Masque toutes les structures bien alignées
- Affiche uniquement les structures avec RMSD > 4 Å ou en erreur
- Zoome sur ces structures pour inspection visuelle

## Sorties générées

### Structure de référence
- `4WB8-assembly1.cif` : Structure de référence PKACA (si téléchargée)

### Fichiers de structures superposées
- `<PDB_ID>_aligned.cif` : Chaque structure ALK superposée au format mmCIF
- Exemple : `2XB7_aligned.cif`, `2XBA_aligned.cif`, etc.

### Fichier de résultats
- `superposition_results.csv` : Tableau récapitulatif contenant :
  - **PDB_ID** : Identifiant de la structure
  - **Chain** : Chaîne utilisée pour la superposition
  - **N_CA_aligned** : Nombre de C-alpha superposés
  - **RMSD** : Écart quadratique moyen en Ångströms
  - **Status** : EXCELLENT, GOOD, MODERATE, HIGH_RMSD, ou ERROR

## Paramètres de la superposition

### Structure de référence PKACA
- **PDB ID** : 4WB8
- **Chaîne** : A
- **UniProt** : P17612
- **Résolution** : 1.55 Å
- **Référence** : Cheung et al. (2015) PNAS 112: 1374-1379

### Région du lobe C
- **Résidus** : 127-350 (228 C-alpha)
- **Stratégie de fallback** : Si moins de 20 C-alpha sont trouvés dans cette région, le script utilise automatiquement tous les C-alpha disponibles dans la chaîne

### Paramètres d'alignement
- **Algorithme** : `cmd.align()` de PyMOL
- **Atomes** : C-alpha uniquement (backbone)
- **Cycles d'optimisation** : 10
- **Cutoff** : 2.0 Å

### Critères d'évaluation
- **RMSD < 2.0 Å** → Status : EXCELLENT
- **RMSD 2.0-2.5 Å** → Status : GOOD
- **RMSD 2.5-4.0 Å** → Status : MODERATE
- **RMSD > 4.0 Å** → Status : HIGH_RMSD (vérification manuelle recommandée)
- **Erreur de chargement/alignement** → Status : ERROR

## Configuration visuelle

Le script principal configure automatiquement l'affichage :
- **Structure de référence (4WB8)** : vert
- **Structures ALK** : cyan
- **Ligands** : sticks
- **Ions** : nb_spheres (sphères non liées)
- **Solvant** : masqué

Après visualisation, vous pouvez personnaliser :
```python
# Dans PyMOL
hide everything
show ribbon, all
show sticks, organic
show nb_spheres, inorganic
zoom reference and chain A and resi 127-350
```

## Vérification des résultats

### Vérification visuelle
1. Charger le script de visualisation
2. Utiliser `highlight_lobes` pour voir la région d'alignement
3. Utiliser `isoler_mauvais` pour inspecter les structures problématiques
4. Comparer visuellement les structures avec RMSD élevé avec la référence

### Vérification quantitative
Consulter `superposition_results.csv` et vérifier :
1. **RMSD** : idéalement < 2 Å, acceptable jusqu'à 4 Å
2. **N_CA_aligned** : devrait être > 50 (idéalement 70-80)
3. **Status** : priorité aux structures EXCELLENT et GOOD

### Statistiques affichées
Le script affiche automatiquement :
- Nombre total de structures traitées
- Nombre de structures avec statut EXCELLENT/GOOD/MODERATE/HIGH_RMSD/ERROR
- Distribution par catégorie de qualité

## Problèmes courants et solutions

### RMSD très élevé (> 4 Å)
**Causes possibles :**
- Structure dans une conformation inactive (DFG-out vs DFG-in)
- Présence de domaines supplémentaires perturbant l'alignement
- Numérotation des résidus très différente
- Structure incomplète ou fragmentaire

**Solution :** Vérification visuelle avec `isoler_mauvais` et inspection manuelle dans PyMOL

### Peu d'atomes superposés (< 20)
**Causes possibles :**
- Structure incomplète (fragment du domaine kinase)
- Lobe C partiellement absent
- Numérotation non standard des résidus

**Solution :** Le script bascule automatiquement sur tous les C-alpha disponibles

### Erreur de chargement (Status: ERROR)
**Causes possibles :**
- Fichier mmCIF non disponible sur la PDB
- Assemblage biologique non défini pour cette structure
- Chaîne spécifiée incorrecte ou absente

**Solution :** Vérifier manuellement sur https://www.rcsb.org/structure/<PDB_ID>

### Fichiers déjà présents
Le script vérifie automatiquement si les fichiers mmCIF existent localement avant de les télécharger, ce qui accélère considérablement les exécutions suivantes.

## Organisation des fichiers

```
Projet/
├── open_pdb_csv.py                                # Script principal
├── visualisation.py                               # Script de visualisation
├── rcsb_pdb_custom_report_20260110111300_new.csv  # Liste des structures
└── superposition_results.csv                      # Résultats

Super/
├── 4WB8-assembly1.cif                       # Référence PKACA
├── 2XB7_aligned.cif                         # Structures superposées
├── 2XBA_aligned.cif
└── ... (toutes les structures *_aligned.cif)
```

## Stratégie du projet

1. **Recherche PDB** : Structures contenant ALK (Q9UM73), assemblages biologiques uniquement
2. **Référence** : PKACA (P17612) - structure 4WB8 (haute résolution : 1.55 Å)
3. **Superposition** : 
   - Région ciblée : Lobe C (résidus 127-350)
   - Méthode : `cmd.align()` avec C-alpha uniquement
   - Cycles d'optimisation : 10
   - Fallback automatique si numérotation non standard
4. **Validation** :
   - Visuelle : fonctions de coloration et isolation
   - Quantitative : RMSD et nombre d'atomes alignés
   - Statistiques détaillées par catégorie


## Auteurs
- Projet M2 Bioinformatique
- Najat et Anaelle
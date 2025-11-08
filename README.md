# Algorithme de Reconciliation

### Introduction 

La réconciliation phylogénétique consiste à faire correspondre l’arbre des espèces et celui des gènes.
Certains gènes suivent une évolution différente du reste du génome, à cause d’événements comme la duplication, la perte ou la spéciation, ce qui peut compliquer la construction de l’arbre des espèces [1].

Cette méthode modélise ces événements pour mieux comprendre l’histoire du génome.
Notre algorithme réalise cette réconciliation avec la librairie ETE3 [2], qui exploite le format Newick, un standard bioinformatique pour représenter la structure, les distances et les nœuds d’un arbre phylogénétique.

<br>

### 1. Explication du Code 
#### a. Fonctions 

#### a.1 Parse Arguments

Il s’agit de la première fonction de notre algorithme de réconciliation. Elle permet de spécifier en argument, lors du lancement du script, les fichiers contenant les arbres d’espèces et d’ancêtres des gènes, ou de les saisir directement dans la ligne de commande.

Cette fonction utilise les librairies os (`import os`), sys (`import sys`) et argparse (`import argparse`).
Elle gère également les options `--loss`, `--verif` et `-h`.
Le module argparse facilite la création automatique de l’aide (`-help`) et le traitement des arguments fournis au script.

##### a.2 Load Trees



##### a.3 Initialize Mapping

q
q
q
q
q 

##### a.4 Compute Lca
a
a
a
a
a

##### a.5 Compute Mappings and Classify
a
a
a
a
a
##### a.6 Display Tree ASCII
a
a
a
a
a
##### a.7 Reconciliation
a
a
a
a
aa
##### a.8 Option Verif and Loss
a
a
a
a
a
##### a.9 MAIN 

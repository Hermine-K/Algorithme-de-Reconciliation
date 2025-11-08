# Algorithme de Reconciliation

### Introduction 

La réconciliation phylogénétique consiste à faire correspondre l’arbre des espèces et celui des gènes.
Certains gènes suivent une évolution différente du reste du génome, à cause d’événements comme la duplication, la perte ou la spéciation, ce qui peut compliquer la construction de l’arbre des espèces [1].

Cette méthode modélise ces événements pour mieux comprendre l’histoire du génome.
Notre algorithme réalise cette réconciliation avec la librairie ETE3 [2], qui exploite le format Newick, un standard bioinformatique pour représenter la structure, les distances et les nœuds d’un arbre phylogénétique.

<br>

### 1. Explication du Code 
#### a. Fonctions 

#### a.1 Parse Arguments et Load  Tree

La première étape de notre algorithme de réconciliation consiste à analyser les arguments passés au script.
Cette fonction permet d’indiquer, au moment de l’exécution, les fichiers contenant les arbres d’espèces et les arbres de gènes, ou bien de les fournir directement via la ligne de commande.

Elle s’appuie sur les librairies os (`import os`), sys (`import sys`), argparse (`import argparse`).

La fonction gère plusieurs options :

* `--loss` : active la prise en compte des pertes de gènes

* `--verif` : lance une vérification des arbres fournis

* `-h` : affiche l’aide automatique générée par argparse

En complément, la fonction **load Tree** permet de charger les arbres de gènes et d’espèces à partir d’un fichier ou d’une chaîne au format Newick, format standard pour représenter la structure hiérarchique d’un arbre phylogénétique.
   

##### a.3 Initialize Mapping



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

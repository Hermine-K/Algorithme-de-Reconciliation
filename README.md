# Algorithme de Reconciliation

### Introduction 

La réconciliation phylogénétique consiste à faire correspondre l’arbre des espèces et celui des gènes.
Certains gènes suivent une évolution différente du reste du génome, à cause d’événements comme la duplication, la perte ou la spéciation, ce qui peut compliquer la construction de l’arbre des espèces [1].

Cette méthode modélise ces événements pour mieux comprendre l’histoire du génome.
Notre algorithme réalise cette réconciliation avec la librairie ETE3 [2], qui exploite le format Newick, un standard bioinformatique pour représenter la structure, les distances et les nœuds d’un arbre phylogénétique.

<br>

### 1. Explication du Code 

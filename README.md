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

La fonction initialize_mapping() constitue la première étape du processus de réconciliation. Elle permet d’établir une correspondance initiale entre les feuilles de l’arbre des gènes et celles de l’arbre des espèces. Cette fonction ajoute une étiquette `M(g)` à chaque feuille de l'arbre de gène. 

##### a.4 Compute Lca

La fonction `compute_lca` permet de trouver le dernier ancêtre commun (LCA) de deux nœuds dans l’arbre des espèces.
Elle fonctionne en plusieurs étapes :

* Pour chaque nœud, elle construit la liste de tous ses ancêtres jusqu’à la racine.

* Elle inverse ces listes pour aller de la racine vers les nœuds.

* Elle compare les listes élément par élément pour identifier le dernier nœud partagé, qui correspond au LCA.

Cette fonction est utilisée dans notre algorithme pour déterminer le point d’origine commun de deux gènes dans l’arbre des espèce.



##### a.5 Compute Mappings and Classify

La fonction `compute_mappings_and_classify()` correspond à la deuxième étape de l’algorithme de réconciliation, appelée phase montante. Elle sert à déterminer la correspondance M(g) pour les nœuds internes de l’arbre de gènes et à classer chaque nœud comme un événement de duplication ou de spéciation.

L’arbre de gènes est parcouru en post-ordre (des feuilles vers la racine). Pour chaque nœud interne, la fonction récupère les correspondances de ses enfants dans l’arbre des espèces, calcule leur dernier ancêtre commun (LCA) et assigne ce LCA au nœud courant. Si le LCA correspond à l’un des enfants, l’événement est une duplication ; sinon, une spéciation.


##### a.6 Display Tree ASCII et Reconciliation

La fonction `display_tree_ascii()` affiche dans le terminal l’arbre de gènes réconcilié sous forme ASCII, accompagné des annotations associées à chaque nœud.
Pour chaque nœud, elle affiche soit :

* le nom du gène et sa correspondance d’espèce pour les feuilles,

* soit le type d’événement (duplication ou spéciation) et la correspondance M(g) pour les nœuds internes.

Elle produit également un résumé final du nombre de duplications et de spéciations identifiées.


La fonction principale `reconciliation()` appelle l’ensemble des fonctions citées plus haut. 


##### a.7 Option Verif and Loss

La fonction `option_verif_et_loss()` gère les options facultatives --verif et --loss du programme.
Elle utilise la méthode `reconcile()` de la librairie ETE3 pour effectuer une réconciliation automatique entre l’arbre de gènes et l’arbre d’espèces, puis affiche les événements de spéciation et de duplication identifiés.
Selon les options activées, elle peut aussi afficher graphiquement l’arbre de gènes original (`--verif`) ou l’arbre réconcilié avec pertes (`--loss`).

La fonction `main()` constitue le point d’entrée du programme. Elle analyse les arguments, vérifie les options, puis lance soit `option_verif_et_loss()` pour les cas spécifiques, soit la réconciliation standard via `reconciliation()`.

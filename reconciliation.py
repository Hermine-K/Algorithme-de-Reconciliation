"""
-------------------------------------------------------------------------------
Outil de Réconciliation Phylogénétique : Hermine KIOSSOU
-------------------------------------------------------------------------------
Ce programme réalise la réconciliation entre un arbre de gènes et un arbre
d'espèces à l'aide de la librairie ete3, en mettant en évidence l'évolution
des gènes à travers les espèces.

La réconciliation consiste à relier chaque nœud de l'arbre de gènes à
l'espèce correspondante dans laquelle le gène (ou son ancêtre) est présent.
Elle permet de détecter les événements évolutifs clés :
    - Spéciation : divergence d'un gène suite à la divergence des espèces,
    - Duplication : copie d'un gène au sein d'une même espèce,
    - Perte de gènes (optionnelle selon l'arbre analysé).
"""

from ete3 import *
import os
import sys
import argparse

def load_trees(gene_input, species_input):
    """
    Charge les arbres de gènes et d'espèces depuis un fichier ou une chaîne Newick.

    Args:
        gene_input: Chemin vers fichier ou chaîne Newick de l'arbre de gènes
        species_input: Chemin vers fichier ou chaîne Newick de l'arbre d'espèces

    Returns:
        Tuple (arbre_genes, arbre_especes)
    """
    # Charger l'arbre de gènes
    if os.path.isfile(gene_input):
        print(f"Chargement de l'arbre de gènes depuis le fichier: {gene_input}")
        G = Tree(gene_input, format=1)
    else:
        print("Chargement de l'arbre de gènes depuis la chaîne Newick")
        G = Tree(gene_input, format=1)

    # Charger l'arbre d'espèces
    if os.path.isfile(species_input):
        print(f"Chargement de l'arbre d'espèces depuis le fichier: {species_input}")
        S = Tree(species_input, format=1)
    else:
        print("Chargement de l'arbre d'espèces depuis la chaîne Newick")
        S = Tree(species_input, format=1)

    print("\nArbre de gènes:")
    print(G)
    print("\nArbre d'espèces:")
    print(S)

    return G, S

def initialize_mapping(gene_tree, species_tree):
    """
    Étape 1: Initialisation - Associe chaque feuille de l'arbre de gènes
    à sa feuille correspondante dans l'arbre d'espèces.

    Args:
        gene_tree: Arbre de gènes
        species_tree: Arbre d'espèces
    """
    print("\n" + "=" * 60)
    print("ÉTAPE 1 : INITIALISATION")
    print("=" * 60)

    for leaf in gene_tree.iter_leaves():
        # Extraire le nom de l'espèce (premier caractère)
        gene_name = leaf.name
        species_name = gene_name[0:3]
        print(species_name)

        # Trouver la feuille correspondante dans l'arbre d'espèces
        species_leaf = species_tree.search_nodes(name=species_name)[0]

        # Associer M(g) à cette feuille
        leaf.add_feature("M", species_leaf)

        print(f"Feuille {gene_name} (espèce {species_name}) → M({gene_name}) = {species_leaf.name}")


def compute_lca(node1, node2):
    """
    Calcule le dernier ancêtre commun (LCA) de deux nœuds dans un arbre.

    Args:
        node1: Premier nœud
        node2: Deuxième nœud

    Returns:
        Le nœud représentant le LCA
    """
    if node1 == node2:
        return node1

    # Construire le chemin depuis node1 jusqu'à la racine
    path1 = []
    current = node1
    while current is not None:
        path1.append(current)
        current = current.up
    path1.reverse()

    # Construire le chemin depuis node2 jusqu'à la racine
    path2 = []
    current = node2
    while current is not None:
        path2.append(current)
        current = current.up
    path2.reverse()

    # Trouver le dernier ancêtre commun
    lca = None
    for i in range(min(len(path1), len(path2))): #comparaison des feuilles vers la racine
        if path1[i] == path2[i]:
            lca = path1[i]
        else:
            break

    return lca



def compute_mappings_and_classify(gene_tree):
    """
    Étape 2: Phase montante - Calcule M(g) pour tous les nœuds internes
    et classifie les événements (duplication/spéciation) en un seul parcours.

    Args:
        gene_tree: Arbre de gènes avec les feuilles déjà initialisées
    """
    print("\n" + "=" * 60)
    print("ÉTAPE 2 : PHASE MONTANTE ET CLASSIFICATION")
    print("=" * 60)

    for node in gene_tree.traverse("postorder"):
        if not node.is_leaf():
            children = node.get_children()
            g1, g2 = children[0], children[1]

            M_g1 = g1.M
            M_g2 = g2.M

            # Calculer le LCA dans l'arbre d'espèces
            lca_node = compute_lca(M_g1, M_g2)
            node.add_feature("M", lca_node)

            # Classification immédiate
            if lca_node == M_g1 or lca_node == M_g2:
                node.add_feature("event_type", "DUPLICATION")
            else:
                node.add_feature("event_type", "SPÉCIATION")

            print(f"\nNœud interne '{node.name}':")
            print(f"  Enfant 1: {g1.name} → M = {M_g1.name}")
            print(f"  Enfant 2: {g2.name} → M = {M_g2.name}")
            print(f"  M({node.name}) = LCA({M_g1.name}, {M_g2.name}) = {lca_node.name}")
            print(f"  → Type: {node.event_type}")


def display_tree_ascii(gene_tree):
    """Affiche l'arbre dans le terminal avec les annotations."""
    print("\n" + "=" * 80)
    print("ARBRE DE GÈNES RÉCONCILIÉ")
    print("=" * 80)

    # Fonction pour formater les nœuds avec leurs annotations
    def get_node_name(node):
        if node.is_leaf():
            return f"{node.name} [M={node.M.name}]"
        else:
            return f"{node.name} [{node.event_type}] M={node.M.name}"

    # Modifier temporairement les noms pour l'affichage
    original_names = {}
    for node in gene_tree.traverse():
        original_names[node] = node.name
        node.name = get_node_name(node)

    # Afficher l'arbre en ASCII
    print(gene_tree.get_ascii(show_internal=True))

    print("=" * 80)

    print("\n" + "-" * 60)
    print("Résumé des événements:")
    print("-" * 60)

    duplications = []
    speciations = []

    # Restaurer les noms originaux et affichage de la classification
    for node in gene_tree.traverse():
        node.name = original_names[node]
        if not node.is_leaf() and hasattr(node, 'event_type'):
            if node.event_type == "DUPLICATION":
                duplications.append(node.name)
            else:
                speciations.append(node.name)

    print(f"Duplications ({len(duplications)}): {', '.join(duplications) if duplications else 'aucune'}")
    print(f"Spéciations ({len(speciations)}): {', '.join(speciations) if speciations else 'aucune'}")


def reconciliation(gene_input, species_input):
    """
    Fonction principale de réconciliation.

    Args:
        gene_input: Fichier ou chaîne Newick de l'arbre de gènes
        species_input: Fichier ou chaîne Newick de l'arbre d'espèces

    Returns:
        Tuple (arbre_genes_reconcilie, arbre_especes)
    """
    # Chargement des arbres
    G, S = load_trees(gene_input, species_input)

    # Étape 1: Initialisation
    initialize_mapping(G, S)

    # Étape 2: Calcul des mappings internes et classification
    compute_mappings_and_classify(G)

    # Affichage de l'arbre réconcilié
    display_tree_ascii(G)

    return G, S


def option_verif_et_loss(gene_input, species_input, show_verif=False, show_loss=False):
    """
    Fonction pour les options verif et loss utilisant la méthode reconcile d'ete3.

    Args:
        gene_input: Fichier ou chaîne Newick de l'arbre de gènes
        species_input: Fichier ou chaîne Newick de l'arbre d'espèces
        show_verif: Si True, affiche genetree
        show_loss: Si True, affiche recon_tree
    """
    # Charger les arbres
    genetree = PhyloTree(gene_input)
    sptree = PhyloTree(species_input)

    print("\n" + "=" * 60)
    options_actives = []
    if show_verif:
        options_actives.append("VERIF")
    if show_loss:
        options_actives.append("LOSS")
    print(f"OPTIONS: {' + '.join(options_actives)}")
    print("=" * 60)

    # Réconciliation avec la méthode d'ete3
    recon_tree, events = genetree.reconcile(sptree)

    # Affichage des événements
    print("\nÉvénements de spéciation et duplication:")
    print("-" * 60)
    for ev in events:
        if ev.etype == "S":
            print('Spéciation:', ','.join(ev.inparalogs), "<====>", ','.join(ev.orthologs))
        elif ev.etype == "D":
            print('Duplication:', ','.join(ev.inparalogs), "<====>", ','.join(ev.outparalogs))

    # Affichage graphique selon les options
    if show_verif:
        print("\nAffichage de l'arbre de gènes original...")
        genetree.show()

    if show_loss:
        print("\nAffichage de l'arbre réconcilié...")
        recon_tree.show()


def parse_arguments():
    """
    Parse les arguments de la ligne de commande.

    Returns:
        Namespace contenant les arguments parsés
    """
    parser = argparse.ArgumentParser(
        description="Outil de réconciliation phylogénétique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Avec des chaînes Newick directement
  python3 reconciliation.py "(((AAA1,BBB1)1,CCC1)2,((CCC2,DDD1)3,DDD2)4)5;" "(((AAA,BBB)6,CCC)7,DDD)8;"

  # Avec des fichiers
  python3 reconciliation.py gene_tree.nwk species_tree.nwk

  # Avec l'option verif
  python3 reconciliation.py gene_tree.nwk species_tree.nwk --verif

  # Avec l'option loss
  python3 reconciliation.py gene_tree.nwk species_tree.nwk --loss

  # Avec les deux options en même temps
  python3 reconciliation.py gene_tree.nwk species_tree.nwk --verif --loss
        """
    )

    parser.add_argument(
        'arbre_gene',
        type=str,
        help="Arbre de gènes (chemin vers fichier .nwk ou chaîne Newick)"
    )

    parser.add_argument(
        'arbre_espece',
        type=str,
        help="Arbre d'espèces (chemin vers fichier .nwk ou chaîne Newick)"
    )

    parser.add_argument(
        '--verif',
        action='store_true',
        help="Affiche l'arbre de gènes original avec la méthode reconcile d'ete3"
    )

    parser.add_argument(
        '--loss',
        action='store_true',
        help="Affiche l'arbre réconcilié avec détection des pertes (méthode reconcile d'ete3)"
    )

    return parser.parse_args()


def main():
    """
    Point d'entrée principal du programme.
    """
    # Parser les arguments
    args = parse_arguments()

    print("=" * 60)
    print("RÉCONCILIATION D'ARBRES PHYLOGÉNÉTIQUES")
    print("=" * 60)

    try:
        # Vérifier si une option spéciale est demandée
        if args.verif or args.loss:
            option_verif_et_loss(args.arbre_gene, args.arbre_espece,
                                 show_verif=args.verif, show_loss=args.loss)
        else:
            # Réconciliation standard
            G, S = reconciliation(args.arbre_gene, args.arbre_espece)

        print("\n" + "=" * 60)
        print("RÉCONCILIATION TERMINÉE")
        print("=" * 60)

    except Exception as e:
        print(f"\nErreur: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
from parser import rechercheASK
import numpy as np
import re


# Fonction qui traduit les mots français en chiffre en fonction de leurs relations
def traductionFrancaisToChiffre(mot):
    mot = mot.lower().strip()
    try:
        int(mot)
        return mot
    except:
        dictionnaire = {
            '0': ["associe", "associé", "associer"],
            '6': ["est", "sont", "etre", "être"],
            '7': [
                "est le contraire de", "contraire", "être contraire",
                "etre contraire", "opposé"
            ],
            '9': ["a", "à", "ont", "partie de"],
            '13': [
                "r_agent", "agent", "sujet", "avoir pour sujet",
                "a pour sujet", "a sujet", "avoir sujet"
            ],
            '15': [
                "est à", "être à", "r_lieu", "lieu", "être à", "est à",
                "est a", "être a"
            ],
            '24': ["r_agent-1", "peut", "peuvent", "pouvoir"],
            '28': ["a comme lieu", "r_lieu-1"],
            '41': [
                "conséquence", "consequence", "être consequence",
                "etre consequence"
            ],
            '42': ["cause", "causer", "a pour cause"],
            '53': ["produit", "produire"],
            '57': ["impliqie", "implication"],
            '60': [
                "avoir féminin", "féminin", "feminin", "avoir feminin",
                "être le féminin", "être féminin"
            ],
            '67': ["est similaire à", "similaire"],
            '106': ["a pour couleur", "avoir couleur"],
            '121': ["possède", "possede", "tient", "tenir", "posseder"],
            '156': ["est utilisé par", "utilise", "utilisé"],
            '163': ["concerne"],
            '170': [
                "a pour forme générique", "singulier", "a pour singulier",
                "au singulier"
            ]
        }
        for (id, relations) in dictionnaire.items():
            for relation in relations:
                if relation == mot:
                    return id

        relation = input("Veuillez donner une bonne relation :")
        return traductionFrancaisToChiffre(relation)


# Fonction qui traduit les relations écrites en chiffres vers leurs traductions pour ReseauASK
def traductionChiffreToRelation(mot):
    mot = mot.lower().strip()

    dictionnaire = {
        "r_associated": ['0'],
        "r_isa": ['6'],
        "r_has_part": ['9'],
        "r_agent": ['13'],
        "r_agent-1": ['24'],
        "r_has_conseq": ['41'],  # r_has_conseq
        "r_lieu": ['15'],
        "r_anto": ['7'],
        "r_lieu-1": ['28'],
        "r_has_causatif": ['42'],
        "r_make": ['53'],
        "r_implication": ['57'],
        "r_fem": ['60'],
        "r_similar": ['67'],
        "r_has_color": ['106'],
        "r_own": ['121'],
        "r_is_used_by": ['156'],
        "r_concerning": ['163'],
        "r_sing_form": ['170']
    }
    for (id, relations) in dictionnaire.items():
        for relation in relations:
            if relation == mot:
                return id

    relation = input(f"{relation} Veuillez donner une bonne relation (CtoR) :")
    return traductionChiffreToRelation(relation)


# Fonction qui traduit les relatiosn écrites en chiffre vers leur traduction française
def traductionChiffreToFrancais(mot):
    mot = mot.lower().strip()

    dictionnaire = {
        "est associé à": ['0'],
        "est un(e)/du": ['6'],
        "a un(e)/de/du": ['9'],
        "est possible par": ['13'],
        "peut": ['24'],
        "a pour conséquence": ['41'],  # r_has_conseq
        "est à": ['15'],
        "est le contraire de": ['7'],
        "produit du": ['53'],
        "comporte comme lieu la/le": ['28'],
        "implique que": ['57'],
        "a pour féminin": ['60'],
        "est similaire à": ['67'],
        "a pour couleur": ['106'],
        "a pour cause": ['42'],
        "possède du": ['121'],
        "est utilisé par": ['156'],
        "conserne": ['163'],
        "a pour singulier": ['170']
    }
    for (id, relations) in dictionnaire.items():
        for relation in relations:
            if relation == mot:
                return id

    relation = input(
        f"{mot} Veuillez donner une bonne relation (chiffre to francais) :")
    return traductionChiffreToRelation(relation)


# Focntion qui traduit les relations écrites en chiffre vers le français à la négation
def traductionChiffreToFrancaisNeg(mot):
    mot = mot.lower().strip()

    dictionnaire = {
        "n'est pas associé à": ['0'],
        "n'est pas un(e)/du": ['6'],
        "n'a pas un(e)/de": ['9'],
        "n'est pas possible par": ['13'],
        "ne peut pas": ['24'],
        "n'a pas pour conséquence": ['41'],  # r_has_conseq
        "n'a pas pour lieu": ['15'],
        "n'est pas le contraire de/du": ['7'],
        "n'a pas pour féminin": ['60'],
        "ne comporte pas comme lieu le/la": ['28'],
        "n'est pas causé par": ['42'],
        "ne produit pas du": ['53'],
        "n'implique pas": ['57'],
        "n'est pas similair à": ['67'],
        "n'a pas pour couleur": ['106'],
        "ne possède pas de": ['121'],
        "n'est pas utilisé par": ["156"],
        "ne conserne pas": ['163'],
        "n'a pas pour singulier": ['170']
    }
    for (id, relations) in dictionnaire.items():
        for relation in relations:
            if relation == mot:
                return id

    relation = input(f"{relation} Veuillez donner une bonne relation (CtoFN):")
    return traductionChiffreToRelation(relation)


# Intersection entre deux ensembles
def calculIntersection(ens1, ens2):
    intersection = []
    for e1 in ens1:
        for e2 in ens2:
            if (e1[1] == e2[1]):
                intersection.append(e1)

    return intersection


# Tri des relations pour la récupération des données
def tri_relations(tab):
    return (-tab[4], -tab[5])


# Fonction qui trie les explications 
def triageExplication(mot1, mot2, relationString, tab_iprim, tab_note,
                      tab_pourcentage, tab_triplet2):
    # Trier les explications
    relations_triees = [
    ]  # [mot1, iprim, relation, mot2, noteClassement, poidFrequence]
    for iprim, noteExplication, tab2, pourcentage in zip(
            tab_iprim, tab_note, tab_triplet2, tab_pourcentage):
        relations_triees.append(
            [mot1, iprim, relationString, mot2, noteExplication, pourcentage])

    # Tri du tableau en fonction des notes des explications, puis en fonction des poids d'annotation si égalité
    relations_triees.sort(key=tri_relations)

    return relations_triees

# Traduire les mots avec des numéros en leur nom formaté donc on passe du mot name vers le mot formatedName
def traductionNomIprim(intersection, tab_iprim):

    tab_iprim_nom = tab_iprim.copy()
    for entite in intersection: # entite = [e,eid,'name',type,w, formatedname]
        if len(entite) == 6:
            tab_iprim_nom[intersection.index(entite)] = entite[5][1:-1]

    return tab_iprim_nom


# Recherche des annotations sur le site reseauASK
def rechercheAnnotations(intersection, mot1, mot2, relationString):

    tab_triplet1 = []
    tab_triplet2 = []
    tab_iprim = []

    # Pour chaque élément de l'intersection 'lion' 
    for i in intersection: # i = [e,eid,'name',type, w, formatedname]
        iprim = i[2].strip("'")
        r1, w1, anot1 = rechercheASK(mot1, "r_isa", iprim)
        r2, w2, anot2 = rechercheASK(iprim, relationString, mot2)
        tab_triplet1.append([r1, w1, anot1])
        tab_triplet2.append([r2, w2, anot2])
        tab_iprim.append(iprim)

    return tab_triplet1, tab_triplet2, tab_iprim


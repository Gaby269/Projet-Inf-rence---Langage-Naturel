from parser import rechercheDUMP, formaterDico, parserDico, rechercheFilterDUMP, getId
from utilities import calculIntersection


# heuristique des réponses en fonction de se que reseauAsk nous donne
def heuristiqueAnnotationAsk(tab_ask, tab_note):

    # Parcours du tableau des notes
    for i in range(len(tab_ask)):
        # Si l'affirmation est "peu pertinent", "non-pertinent"
        if "peu pertinent" in tab_ask[i][2] or "non pertinent" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] / 4
        # Sinon au contraire est ce que l'affirmation est "pertinent"
        elif "pertinent" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] * 4

        # Si l'affirmation est "rare"
        if "rare" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] / 3
        # Si l'affirmation est "toujours vrai"
        if "toujours vrai" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] * 3

        # Si l'affirmation est possible
        if "possible" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] / 2
        # Si l'affirmation est fréquente
        if "fréquent" in tab_ask[i][2]:
            tab_note[i] = tab_note[i] * 2

        # Si pas d'indication pertinente on ne change rien
        if tab_ask[i][2] == "VIDE" or "non spécifique" in tab_ask[i][2]:
            tab_note[i] = tab_note[i]
        # A changer pcq faut le prendre en compte correctement
        if "constrastif" in tab_ask[i][2]:
            tab_note[i] = tab_note[i]

    return tab_note


# heuristique des mots qui sont égaux, on les laisse mais on réduit leurs pertinence (par ex : un chat est un chat, et un chat peut manger)
def heuristiqueEgalite(mot1, tab_iprim, tab_note):
    # Parcours du tableau des notes
    for i in range(len(tab_note)):
        if tab_iprim[i] == mot1:
            tab_note[i] = tab_note[
                i] / 4  # comme si c'était peu pertinent de le dire
    return tab_note


# heuristique par rapport aux pourcentages de Aprécis par rapport au Agénéral (par ex : pourcentage d'oiseau pouvant voler parmis tous les oiseaux)
def heuristiquePourcentageDump(mot1, relation, mot2, tab_iprim):

    pourcentage = []

    # Parcours du tableau des iprim
    for i in range(len(tab_iprim)):

        print("\n\n")
        #print(tab_iprim[i])

        # Recuperation du nombre total de A
        # en récupérant les relations sortantes de A (par ex : animaux)
        rechercheFilterDUMP(tab_iprim[i], id_relation=6, with_sortante=False)
        dicoFilterIprim = formaterDico([tab_iprim[i]],
                                       filter=True,
                                       id_relation=6,
                                       with_sortante=False)[tab_iprim[i]]
        entiteFilterIprim = dicoFilterIprim[
            "2;e;eid;'name';type;w;'formated name'"]

        # Recuperation des iprim qui sont en relation avec B (par ex : lion qui peut rugir)
        # en récuperant les relation entrantent de B (par ex : de rugir)
        rechercheFilterDUMP(mot2, id_relation=relation, with_sortante=False)
        dicoFilterMot2 = formaterDico([mot2],
                                      filter=True,
                                      id_relation=relation,
                                      with_sortante=False)[mot2]
        entiteFilterMot2 = dicoFilterMot2[
            "2;e;eid;'name';type;w;'formated name'"]

        # Tableau d'intersection entre l'ensemble de tous les A sortant et de tous les B entrants (par ex : tous les animaux possible et ceux qui peuvent rugir)
        intersection = calculIntersection(entiteFilterIprim, entiteFilterMot2)

        # Calcul du nombres de chaque ensembles
        nb_entiteTotal_iprim = len(
            entiteFilterIprim)  # nombre total de A (par ex : d'animaux)
        nb_entite_iprimMot2 = len(
            intersection)  # nombre de B (par ex : peuvent rugir)
        pourcentage.append(nb_entite_iprimMot2 * 100 / nb_entiteTotal_iprim)  # calcul du pourcentage final

        #print(f"nbTotal de {tab_iprim[i]}  : ", nb_entiteTotal_iprim)
        #print("nbTrier : ",nb_entite_iprimMot2)
        #print("Pourcentage : ", (nb_entite_iprimMot2 / nb_entiteTotal_iprim)*100)

    return pourcentage


# Application de toutes les heuristiques et renvoie le tableaud des notes plus le pourcentage
def calculNoteRelation(
    mot1, relation, mot2, tab_iprim, tab_ask, tab_note, use_egalite, use_ask, use_pourcentage
):  # utiliser ca pour le faire use_ask=True, use_egalite=True, use_pourcentage=True
    if use_egalite :
        tab_note = heuristiqueEgalite(mot1, tab_iprim, tab_note)
    if use_ask :
        tab_note = heuristiqueAnnotationAsk(tab_ask, tab_note)
    if use_pourcentage :
        tab_pourcentage = heuristiquePourcentageDump(mot1, relation, mot2,
                                                tab_iprim)
    else :
        tab_pourcentage = [0]*len(tab_note)

    return tab_note, tab_pourcentage


# Test pour les fonctions
if __name__ == "__main__":
    heuristiquePourcentageDump("lion", '24', "rugir", [
        'animal', 'animal sauvage', 'félin', 'félin>17559', 'fauve', 'félidé',
        'féliforme', 'féloïdé', 'homme', 'individu'
    ], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    #['animal', 'animal sauvage', 'félin', 'félin>17559', 'fauve', 'félidé', 'féliforme', 'féloïdé', 'homme', 'individu']

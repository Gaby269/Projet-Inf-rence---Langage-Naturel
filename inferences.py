import os
import re
from parser import rechercheDUMP, formaterDico, parserDico
from utilities import *
from heuristiques import *


def debutInference(mot1, relation, mot2) :
    
    # Récuperer les informations de ReseauDUMP des mot1 et des mots 2
    rechercheDUMP([mot1, mot2])
    print("** Recherche dans ReseauDUMP fini\n")

    # Dico récuperer du fichier
    dico_courant = formaterDico([mot1, mot2])
    # Puis je recupere le dico de chacun
    dico1 = dico_courant[mot1]
    dico2 = dico_courant[mot2]

    return dico1, dico2

def suiteInference(dico1_form, dico2_form) :
    # Recup les elements c de dico1
    entite_dico1 = dico1_form["2;e;eid;'name';type;w;'formated name'"]
    entite_dico2 = dico2_form["2;e;eid;'name';type;w;'formated name'"]
    #print("ENTITE 1 :",entite_dico1) print("\n\n") print("ENTITE 2 : ",entite_dico2)
    print("\n** Recuperer les entites fini ** ")

    # Intersection des entités entre dico1 et dico2 pour obtenir les C valables
    print("\n")
    intersection = calculIntersection(entite_dico1, entite_dico2)
    #print("INTERSECTION : ", intersection)
    print("** Intersection fini **")

    return intersection

def explicationInference(mot1, relation, mot2, intersection, dico1, dico2, use_egalite, use_ask, use_pourcentage) :
    
    print("\n\n** Calcul en cours.. () **")
    if len(intersection) != 0 :

        # Traduction de la relation en r_...
        relationString = traductionChiffreToRelation(relation)
        # Tableau des annotation de reseauASK
        tab_triplet1, tab_triplet2, tab_iprim = rechercheAnnotations(intersection, mot1, mot2, relationString)
        # Traduction des iprim pour l'affichage des réponses
        tab_iprim_nom = traductionNomIprim(intersection, tab_iprim)
        # Tableau des notes et des pourcentages
        tab_note, tab_pourcentage = calculNoteRelation(mot1, relation, mot2, tab_iprim, tab_triplet2, [1]*len(tab_triplet2), use_egalite, use_ask, use_pourcentage)
        # Tableau des relations triees
        relations_triees = triageExplication(mot1, mot2, relationString, tab_iprim_nom, tab_note, tab_pourcentage, tab_triplet2)
        #print("IPRIM : ", tab_iprim)

        return dico1, dico2, True, relations_triees

    return dico1, dico2, False, []
    

def deduction(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage):  # A relation B

    print("\n****************************\n** Déduction est en cours **\n****************************\n")
    
    # Début générique des inferences
    dico1, dico2 = debutInference(mot1, relation, mot2)
    
    # Récuperer les relations sortantes r_isa du dico1 (mot1)
    dico1_form = parserDico(dico1, "relation", '6', is_entrante=False)
    #print("DICO1 FORMATER : ",dico1_form) print("\n\n")
    print("  Dico1 formaté")

    # Récuperer les relations entrantes de type relation (paramètre) de dico2 (mot2)
    dico2_form = parserDico(dico2, "relation", relation, is_sortante=False)
    #print("DICO2 FORMATER : ",dico2_form) print("\n\n")
    print("  Dico2 formaté")

    # Calcul des explication possible
    intersection = suiteInference(dico1_form, dico2_form)

    # Explications finals
    return explicationInference(mot1, relation, mot2, intersection, dico1_form, dico2_form, use_egalite, use_ask, use_pourcentage)


def induction(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage):  # A relation B

    print("\n****************************\n** Induction est en cours **\n****************************\n")

    # Début générique des inferences
    dico1, dico2 = debutInference(mot1, relation, mot2)

    # Recuperer les relations entrantes de r_isa vers mot1
    dico1_form = parserDico(dico1, "relation", '6', is_sortante=False)
    #print("DICO1 FORMATER : ",dico1_form) 
    #print("\n\n")
    print("  Dico1 formaté")

    # Recuperer les relations entrantes de relation vers mot2
    dico2_form = parserDico(dico2, "relation", relation, is_sortante=False)
    #print("DICO2 FORMATER ENTRANTES : ",dico2_form) 
    #print("\n\n")
    print("  Dico2 formaté")

    # Calcul des explication possible
    intersection = suiteInference(dico1_form, dico2_form)

    # Explications finals
    return explicationInference(mot1, relation, mot2, intersection, dico1_form, dico2_form, use_egalite, use_ask, use_pourcentage)


    
def transitivité(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage):

    print("\n*******************************\n** Transitivité est en cours **\n*******************************\n")
    
    # si A vers B et B vers C alors A vers C
    # Début générique des inferences
    dico1, dico2 = debutInference(mot1, relation, mot2)
    # Récuperer les relations sortantes relation du dico1 (mot1)
    dico1_form = parserDico(dico1, "relation", relation, is_entrante=False)
    #print("DICO1 FORMATER : ",dico1_form) print("\n\n")
    print("  Dico1 formaté")

    # Récuperer les relations entrantes de type relation (paramètre) de dico2 (mot2)
    dico2_form = parserDico(dico2, "relation", relation, is_sortante=False)
    #print("DICO2 FORMATER : ",dico2_form) print("\n\n")
    print("  Dico2 formaté")

    # Calcul des explication possible
    intersection = suiteInference(dico1_form, dico2_form)

    # Explications finals
    return explicationInference(mot1, relation, mot2, intersection, dico1_form, dico2_form, use_egalite, use_ask, use_pourcentage)

    
    

def inferencesTotal(mot1, relation, mot2, is_egalite, use_egalite, use_ask, use_pourcentage) :

    dicoDeduction1, dicoDeduction2, is_oui1, relations_triees1 = deduction(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage)
    dicoInduction1, dicoInduction2, is_oui2, relations_triees2 = induction(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage)
    dicoTransitivite1, dicoTransitivite2, is_oui3, relations_triees3 = transitivité(mot1, relation, mot2, use_egalite, use_ask, use_pourcentage)

    relationString = traductionChiffreToFrancais(relation)
    relationStringNeg = traductionChiffreToFrancaisNeg(relation)

    # La relation serait alors vrai
    if is_oui1 or is_oui2 or is_oui3 :
        
        explications = relations_triees1 + relations_triees2 + relations_triees3
        #print(explications)
        # Suppression des doublons dans explications
        explications = list(set(tuple(exp) for exp in explications))
        # Tri du tableau en fonction des notes des explications, puis en fonction des poids d'annotation si égalité
        explications.sort(key=tri_relations)

        # Affichage final 
        #print("EXPLICATION TRIEES : ", explications)
        print(f"\n\nOuiii un(e) {mot1} {relationString} {mot2} parce que : \n")

        cpt = 1 # Affichage de 5 explications 
        for exp in explications : # exp = [mot1, iprim, relationString, mot2, noteExplication, pourcentage]
            # Soit on veut les égalité, soit si on a bien pas d'egalité
            if is_egalite or (exp[0] != exp[1] and exp[1] != exp[3]) :
                # Si c'est une deduction
                if [x for x in exp] in relations_triees1 :
                    print(f"   * {cpt} * un(e)/du {exp[0]} est un(e) {exp[1]}, et un(e)/du {exp[1]} {relationString} {exp[3]} !!!")
                # Si c'est une induction
                elif [x for x in exp] in relations_triees2 :
                    print(f"   * {cpt} * un(e)/du {exp[1]} est un(e) {exp[0]}, et un(e)/du {exp[1]} {relationString} {exp[3]} !!!")
                # Si c'est une transitivité
                else :
                    print(f"   * {cpt} * un(e)/du {exp[0]} {relationString} {exp[1]}, et un(e)/du {exp[1]} {relationString} {exp[3]} !!!")
            # Si ya égalité on continue parcequ'on en veut pas
            else :
                continue

            cpt+=1
            if cpt > 5 :
                break
        print("\n\n")
        
    # La relation serait alors fausse
    else : 
        tab_entite1 = dicoDeduction1["2;e;eid;'name';type;w;'formated name'"] + dicoInduction1["2;e;eid;'name';type;w;'formated name'"] # Tableau d'entite des relation sortante de deduction et induction
        tab_entite2 = dicoDeduction2["2;e;eid;'name';type;w;'formated name'"] + dicoInduction2["2;e;eid;'name';type;w;'formated name'"] # Tableau d'entite des relation entrante de deduction et induction
        entiteTransitivite1 = dicoTransitivite1["2;e;eid;'name';type;w;'formated name'"] # tableau entite de transitivite en relation sortante
        entiteTransitivite2 = dicoTransitivite2["2;e;eid;'name';type;w;'formated name'"] # tableau entite de transitivite en relation entrante
        
        explications1 = []
        explications2 = []
        explicationsT1 = []
        explicationsT2 = []

        # Pour chaque éléments trouvés on en veut 5 au maximum
        cpt = 1
        for e1, e2, eT1, eT2 in zip(tab_entite1, tab_entite2, entiteTransitivite1, entiteTransitivite2) :

            cpt += 1
            # Remplissage des explications negatives
            # Si c'est un mot formaté
            if len(e1) == 6 :
                # si l'explication n'est pas présente dans explications1 ou explications2
                if ([mot1, relation, mot2, e1[5][1:-1]] not in explications1 or [mot1, relation, mot2, e1[5][1:-1]] not in explications2) :
                    explications1.append([mot1, relation, mot2, e1[5][1:-1]]) # ajout dans explications1
            # Pareil si c'est un nom de base
            else :
                if ([mot1, relation, mot2, e1[2][1:-1]] not in explications1 or [mot1, relation, mot2, e1[2][1:-1]] not in explications2) :
                    explications1.append([mot1, relation, mot2, e1[2][1:-1]])
            cpt += 1
            if len(e2) == 6 :
                if ([mot1, relation, mot2, e1[5][1:-1]] not in explications2) or [mot1, relation, mot2, e1[5][1:-1]] not in explications1 :
                    explications2.append([mot1, relation, mot2, e2[5][1:-1]])
            else :
                if ([mot1, relation, mot2, e1[2][1:-1]] not in explications2) or [mot1, relation, mot2, e1[2][1:-1]] not in explications1 :
                    explications2.append([mot1, relation, mot2, e2[2][1:-1]])
            cpt += 1
            if len(eT1) == 6 :
                if ([mot1, relation, mot2, e1[5][1:-1]] not in explicationsT1) or [mot1, relation, mot2, e1[5][1:-1]] not in explicationsT2:
                    explicationsT1.append([mot1, relation, mot2, eT1[5][1:-1]])
            else :
                if ([mot1, relation, mot2, e1[2][1:-1]] not in explicationsT1) or [mot1, relation, mot2, e1[2][1:-1]] not in explicationsT2 :
                    explicationsT1.append([mot1, relation, mot2, eT1[2][1:-1]])
            cpt += 1
            if len(eT2) == 6 :
                if ([mot1, relation, mot2, e1[5][1:-1]] not in explicationsT2) or [mot1, relation, mot2, e1[5][1:-1]] not in explicationsT1 :
                    explicationsT2.append([mot1, relation, mot2, eT2[5][1:-1]])
            else :
                if ([mot1, relation, mot2, e1[2][1:-1]] not in explicationsT2) or [mot1, relation, mot2, e1[2][1:-1]] not in explicationsT1 :
                    explicationsT2.append([mot1, relation, mot2, eT2[2][1:-1]])
            cpt += 1

            # Compteur augmenter pour qu'il n'y est que 10 réponse
            if cpt > 5 :
                break
        
        if len(explications1) == 0 and len(explications2) == 0 and len(explicationsT1) == 0 and len(explicationsT2) == 0 :
            print(f"\n\nReseauDUMP ne sait pas si un(e) {mot1} {relationString} {mot2} !!!\n")
        else : 
            print(f"\n\nNon un(e) {mot1} {relationStringNeg} {mot2}\n")
            # on cherche les relations avec mots 1 et on dit qu'il ne le sont pas avec mot2
            # et on peut chercher aussi les entrées de mot2 et dire quiol ne le sont pas
            cpt = 1
            for e1, e2, et1, et2 in zip(explications1, explications2, explicationsT1, explicationsT2) :
            
                # Soit on veut les égalité, Soit on a bien pas d'egalité
                if is_egalite or ( e1[0] != e1[3] and e1[2] != e1[3] and e2[0] != e2[3] and e2[2] != e2[3] and et1[0] != et1[3] and et1[2] != et1[3] and et2[0] != et2[3] and et2[2] != et2[3]) :
                    
                    # Si c'est une deduction de relation sortante
                    print(f"   * un(e)/du {e1[0]} est un(e)/du {e1[3]}, mais un(e)/du {e1[3]} {relationStringNeg} {e1[2]} !!!")
                    # Si c'est une deduction de relation entrante
                    print(f"   * un(e)/du {e2[3]} {relationString} {e2[2]}, mais un(e)/du {e2[0]} n'est pas un(e)/du {e2[3]} !!!")
                    # Si c'est une induction de relation sortante
                    print(f"   * un(e)/du {e1[3]} est un(e)/du {e1[0]}, mais un(e)/du {e1[3]} {relationStringNeg} {e1[2]} !!!")
                    # Si c'est une induction de relation entrante
                    print(f"   * un(e)/du {e2[3]} {relationString} {e2[2]}, mais un(e)/du {e2[3]} n'est pas un(e)/du {e2[0]} !!!")
                    # Si c'est une transitivité de relation sortante
                    print(f"   * un(e)/du {et1[0]} {relationString} {et1[3]}, mais un(e)/du {et1[3]} {relationStringNeg} {et1[2]} !!!")
                    # Si c'est une transitivité de relation entrante
                    print(f"   * un(e)/du {et2[3]} {relationString} {et2[2]}, mais un(e)/du {et2[0]} {relationStringNeg} {et2[3]} !!!")
                # Si ya égalité on continue parcequ'on en veut pas
                else :
                    continue
    
                cpt += 1
                if cpt > 5 :
                    break


if __name__ == "__main__":
    # 9 = r_has_part
    #deduction("enfant", '24', "rigoler")
    #induction("lion", '9', "poils")
    inferencesTotal("chocolat", '9', "lait", True)
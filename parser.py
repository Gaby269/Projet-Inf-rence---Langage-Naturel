import requests
import json
import os
import re


#from inferences import deduction
def tri_cle(cle):
    if 'formated name' in cle:  #entite
        return 0
    elif 'ntname' in cle:  #typede entite
        return 1
    elif 'node1' in cle:  #relation
        return 2
    elif 'rthelp' in cle:  #type relation
        return 3



# Formatage du mot pour les fichiers
def motFormater(mot) :
    mot = mot.replace(" ","-")
    mot = mot.replace(">","-")
    mot = mot.replace("/","-")

    return mot


# Fonction qui cherche dans reseauDUMP en fonctions des infos données
#depart sert à savoir si c'est la premiere fois quon le demande comme dans le main ou on veut les relations
def rechercheDUMP(mots,
                  overwrite=False,
                  id_relation=-1):

    for mot in mots:
        # Si le mot a pas deja été trouvé
        chemin = os.path.join("dump_files", f"selected_{motFormater(mot)}.txt")
        if (not os.path.exists(chemin) or (overwrite == True)):
            id = ""
            if (id_relation != -1):
                id = str(id_relation)
    
            # Faire la requête HTTP
            if len(mot.split()) > 1 :
                for m in mot.split()[1:-1] :
                    mot = mot+"+"+m
                    if m == mot.split()[-1] :
                        mot+=m
            url1 = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot + "&rel=" + id + "&relin=norelin"
            url2 = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot + "&rel=" + id + "&relout=norelout"
            
            print(url1)
            print(url2)

            selected1 = "MUTED_PLEASE_RESEND"
            selected2 = "MUTED_PLEASE_RESEND"
            while ("MUTED_PLEASE_RESEND" in selected1 or "MUTED_PLEASE_RESEND" in selected2):
                
                response1 = requests.get(url1)
                response2 = requests.get(url2)
        
                # Recuperation des données de reseauDump dans body
                body1 = response1.text
                body2 = response2.text
        
                # Recherche de la position de la première occurrence de la balise <CODE> pour récuperer les choses à l'interieur
                start_index1 = body1.find("<CODE>")
                start_index2 = body2.find("<CODE>")
        
                # Recuperation du texte du code source
                selected1 = ""
                selected2 = ""
        
                # Si le mot existe dans la base
                if start_index1 != -1:
                    end_index1 = body1.find("</CODE>", start_index1)
                    end_index2 = body2.find("</CODE>", start_index2)
        
                    if end_index1 != -1:
                        # Extraction du contenu entre les balises <CODE> et </CODE>
                        selected1 = body1[start_index1+6:end_index1] # On rajoute la longueur de la balise <CODE>
                        selected2 = body2[start_index2+6:end_index2]
        
                # Sinon on regarde s'il y a un message d'erreur qui dit que le mot n'existe pas
                else:
                    start_index_warning = body1.find(u"""<div class="jdm-warning">""")
                    if start_index_warning != -1:
                        print(f"\nLe mot {mot} n'existe pas veuillez changer la phrase")
                    else:
                        print("\nErreur lors de la requête")
                    exit(1)
    
            body1 = selected1[:-7]
            
            # Ecriture des relations sortantes
            with open(os.path.join("dump_files", f"selected_{motFormater(mot)}.txt"), "w", encoding="utf-8", errors="surrogateescape") as f:
                f.write(body1)
    
            body2 = selected2[selected2.find("// les relations entrantes"):]
    
            # Ecriture des relations entrantes
            with open(os.path.join("dump_files", f"selected_{motFormater(mot)}.txt"), "a", encoding="utf-8", errors="surrogateescape") as file:
                file.write(body2)
                    
            print(f"\n   Les données du mot {mot} ont été récupérées.\n")
        else :
            print(f"   Le fichier dump_files/selected_{motFormater(mot)}.txt existe déjà\n")



def rechercheFilterDUMP(mot, overwrite=False, id_relation=-1, with_sortante=True, with_entrante=True) :

    # Si le mot a pas deja été trouvé
    chemin = os.path.join("filter_files", f"filter_{motFormater(mot)}_{id_relation}_{with_sortante}_{with_entrante}.txt")
    if (not os.path.exists(chemin) or (overwrite == True)):
        id = ""
        if (id_relation != -1):
            id = str(id_relation)

        url = ""
        if with_sortante == False : 
            # Faire la requête HTTP
            url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot + "&rel=" + id + "&relout=norelout"
            print(url)
            
        if with_entrante == False :
            # Faire la requête HTTP
            url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot + "&rel=" + id + "&relin=norelin"
            print(url)
        

        selected = "MUTED_PLEASE_RESEND"
        while ("MUTED_PLEASE_RESEND" in selected):
            # print(url)
            response = requests.get(url)
    
            # Recuperation des données de reseauDump dans body
            body = response.text
    
            # Recherche de la position de la première occurrence de la balise <CODE> pour récuperer les choses à l'interieur
            start_index = body.find("<CODE>")
    
            # Recuperation du texte du code source
            selected = ""
    
            # Si le mot existe dans la base
            if start_index != -1:
                end_index = body.find("</CODE>", start_index)
    
                if end_index != -1:
                    # Extraction du contenu entre les balises <CODE> et </CODE>
                    selected = body[start_index+6:end_index] # On rajoute la longueur de la balise <CODE>
    
            # Sinon on regarde s'il y a un message d'erreur qui dit que le mot n'existe pas
            else:
                start_index_warning = body.find(u"""<div class="jdm-warning">""")
                if start_index_warning != -1:
                    print(f"\nLe mot {mot} n'existe pas veuillez changer la phrase")
                else:
                    print("\nErreur lors de la requête")
                exit(1)

        body = selected[:-7]
        
        # Ecriture des relations sortantes
        with open(os.path.join("filter_files", f"filter_{motFormater(mot)}_{id_relation}_{with_sortante}_{with_entrante}.txt"), "w", encoding="utf-8", errors="surrogateescape") as f:
            f.write(body)
                
        print(f"\n\n   Les données du mot {mot} ont été récupérées.\n\n")
    else :
        print(f"\n   Le fichier filter_files/filter_{motFormater(mot)}_{id_relation}_{with_sortante}_{with_entrante}.txt existe déjà")


# Fonction qui nous sert à donner une réponse
def rechercheDUMPreponse(mot1, id_relation, mot2) :
    # Si le mot a pas deja été trouvé
    chemin = os.path.join("response_files", f"reponse_{motFormater(mot1)}_{id_relation}_{motFormater(mot2)}.txt")
    if (not os.path.exists(chemin)):
        id = ""
        if (id_relation != -1):
            id = str(id_relation)

        # Faire la requête HTTP
        url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot1 + "&rel=" + id + "&relin=norelin"
        print(url)

        selected = "MUTED_PLEASE_RESEND"
        while ("MUTED_PLEASE_RESEND" in selected):
            response = requests.get(url)
    
            # Recuperation des données de reseauDump dans body
            body = response.text
    
            # Recherche de la position de la première occurrence de la balise <CODE> pour récuperer les choses à l'interieur
            start_index = body.find("<CODE>")
    
            # Recuperation du texte du code source
            selected = ""
    
            # Si le mot existe dans la base
            if start_index != -1:
                end_index = body.find("</CODE>", start_index)
    
                if end_index != -1:
                    # Extraction du contenu entre les balises <CODE> et </CODE>
                    selected = body[start_index+6:end_index] # On rajoute la longueur de la balise <CODE>
    
            # Sinon on regarde s'il y a un message d'erreur qui dit que le mot n'existe pas
            else:
                start_index_warning = body.find(u"""<div class="jdm-warning">""")
                if start_index_warning != -1:
                    print(f"\nLe mot {mot1} n'existe pas veuillez changer la phrase")
                else:
                    print("\nErreur lors de la requête")
                exit(1)

        body = selected[:-7]
        
        poid = -1
        idMot2 = -1
        idMot1 = -1
        
        # Recherche de l'id de lentite du mot2
        entite = body.find(f"'{mot2}'")
        if entite != -1:
            end_entite = body.rfind("e", 0, entite) #je veux les élément avant entite et apres la premiere occurence de e avant
            if end_entite != -1:
                selected = body[end_entite+2:entite-1]
            idMot2 = selected
        
            # Recherche de l'id du mot1
            idMot1 = body.find("eid=") # trouver l'id du mot1
            if idMot1 != -1:
                end_id = body.find(")", idMot1)
                if end_id != -1:
                    selected = body[idMot1+4:end_id]
            idMot1 = selected
        
            # Recherche de la relation associé
            relation = body.find(f"{idMot1};{idMot2};6")
            if relation != -1:
                end_relation = body.find("r", relation)
                if end_relation != -1:
                    selected = body[relation+len(idMot1)+len(idMot2)+4:end_relation-1]
            poid = selected
        

            # Ecriture de la réponse
            chemin = os.path.join("reponse_files", f"reponse_{motFormater(mot1)}_{id_relation}_{motFormater(mot2)}.txt")
            with open(chemin, "w", encoding="utf-8") as f:
                if int(poid) >= 0: # On considere que si la relation est à 0 elle est vrai
                    f.write("True")
                else:
                    f.write("False")
        else :
            # Ecriture de la reponse étant fausse
            chemin = os.path.join("reponse_files", f"reponse_{motFormater(mot1)}_{id_relation}_{motFormater(mot2)}.txt")
            with open(chemin, "w", encoding="utf-8") as f:
                f.write("Pas")
                            
        print(f"\n\n   La réponse de si {mot1} {id_relation} {mot2} a été récupérées.\n\n")
    else :
        print(f"\n   Le fichier reponse_files/reponse_{motFormater(mot1)}_{id_relation}_{motFormater(mot2)}.txt existe déjà")

#Fonction qui forme le texte en dico
def formaterDico(phr, filter=False, id_relation=-1, with_sortante=True, with_entrante=True):

    # Dictionnaire pour tous les mots de la phrase
    dico_entier = {}

    for p in phr:

        # Remplir le dico
        dico_entier[p] = {}

        # Bossage avec le fichier mtn
        donnees_par_categorie = {}

        # Choix du fichier a utiliser
        fichier = ""
        if filter :
            path = "filter_files"
            name = f"filter_{motFormater(p)}_{str(id_relation)}_{str(with_sortante)}_{str(with_entrante)}.txt"
        else : 
            path = "dump_files"
            name = f"selected_{motFormater(p)}.txt"
            
        with open(os.path.join(path, name), 'r', encoding="utf-8", errors="surrogateescape") as file:

            categorie_actuelle = "None"  # dans quelle categorie on est
            num_categorie = 0  # id de la categorie
            a_l_interieur_de_la_balise = False  # si tes dans <def></def>
            lignes = file.readlines()

            for ligne in lignes:
                if ligne.startswith('\n'):
                    continue
                # On igonre les lignes <def></def> si on est dedans on cherche
                elif a_l_interieur_de_la_balise:
                    if ligne.strip() == "</def>":
                        a_l_interieur_de_la_balise = False
                    continue
                # On ignore si c'est la ligne
                elif ligne.strip() == "<def>":
                    a_l_interieur_de_la_balise = True
                    continue
                # Si c'est une ligne de commentaire
                if ligne.startswith('//') and not ":" in ligne:
                    continue
                if ligne.startswith('//') and ":" in ligne:
                    # on peut regardant tant quon a pas start par r
                    if ((len(donnees_par_categorie.get(categorie_actuelle, [])) == 0)
                        and len(donnees_par_categorie) !=
                        0):  # si la categorie est vide alors on saute le commentaire
                        continue
                    # Sinon on a trouvé une nouvelle catégorie
                    
                    elif ("les relations sortantes" not in ligne) and (num_categorie == 3):  # on verifie que si jamais ya pas de relations sortantes on incremente
                        # cela veut dire quon est en relations entrantes et que il n'y a pas de relations sortantes
                        num_categorie += 1
                        categorie_actuelle = str(num_categorie) + ";" + (ligne.split(
                         ":")[1]).strip()  # on peut prendre les meme chose que la ligne suivante
                        donnees_par_categorie[categorie_actuelle] = []
                        # on passe a la categorie suivante normalement
                        num_categorie += 1
                        categorie_actuelle = str(num_categorie) + ";" + (ligne.split(
                         ":")[1]).strip()  # on peut prendre les meme chose que la ligne suivante
                        donnees_par_categorie[categorie_actuelle] = []
                        
                    elif ("les relations entrantes" not in ligne) and (num_categorie == 4):  # on regarde si ya des relations entrantes
                        # cela veut dire quon est en relations entrantes mais que yen a pas
                        num_categorie += 1
                        categorie_actuelle = str(num_categorie) + ";" + (ligne.split(
                         ":")[1]).strip()  # on peut prendre les meme chose que la ligne suivante
                        donnees_par_categorie[categorie_actuelle] = []
                        
                    else:  # sinon on est dans les sortantes et ya pas de problème
                        num_categorie += 1
                        categorie_actuelle = str(num_categorie) + ";" + (
                         ligne.split(":")[1]).strip()
                        #print("cate", categorie_actuelle)
                        donnees_par_categorie[categorie_actuelle] = []
                # Sinon
                else:
                    # On ajoute la ligne à la catégorie courante
                    if categorie_actuelle != "None":
                        donnees_par_categorie[categorie_actuelle].append(
                         ligne.strip().split(';'))

        dico_entier[p] = donnees_par_categorie

    return dico_entier


# Dictiopnnaire a structurer pour avoir les specifications demandées avec la relation, et le fait que ce soit sortant et entrant ou non
# Type de trie c'est si je trie sur entite ou relation ou autre
# valeur_trie  c'est avec quoi je trie
def parserDico(dico,
               type_trie,
               valeur_trie,
               is_sortante=True,
               is_entrante=True):

    # On récuper le dico
    dico_formater = dico.copy()

    # Tableau des clé d'un dico
    cle = list(dico_formater.keys())

    # Tableau des relations
    tab_entrantes = []
    tab_sortantes = []
    tab_typeRelat = []
    tab_Entites = []
    tab_typeEntit = []

    if type_trie == "relation":

        cle.reverse()

        # Parcours du dictionnaire
       
        for key in cle: 
            #cpt = 0
            # Parcours des tableaux
            for tab in dico_formater[key]:
                
                # cpt += 1
                # if cpt % 1000 == 0:
                    # print(key, "-", cpt)
                    
                #  Choix du type de relation
                if tab[0] == 'rt' and tab[1] == valeur_trie and tab not in tab_typeRelat:
                    tab_typeRelat.append(tab)
                # Choix des relations
                if tab[0] == 'r' and tab[4] == valeur_trie:
                    # Si on choisis les relation sortantes + Si c'est bien la clé pour les relations sortantes (4)
                    if is_sortante and key[0] == '4' and tab not in tab_sortantes and int(tab[5]) > 0 :
                        tab_sortantes.append(tab)
                    # Si c'est une relation et que la relation est de type relation + Si c'est bien la clé pour les relations entrantes (5)
                    if is_entrante and key[0] == '5' and tab not in tab_entrantes and int(tab[5]) > 0:
                        tab_entrantes.append(tab)
                # Choix les entités
                if tab[0] == 'e':
                    if is_sortante:
                        # Parcours des relations sortantes
                        for sor in tab_sortantes:
                            # Si entite aparait dans une relation en terme 1 ou en terme 2 on le garde
                            if (tab[1] == sor[2] or tab[1] == sor[3]) and tab not in tab_Entites:
                                tab_Entites.append(tab)
                    if is_entrante:
                        # Parcours des relations entrantes
                        for ent in tab_entrantes:
                            # Si entite aparait dans une relation en terme 1 ou en terme 2 on le garde
                            if (tab[1] == ent[2] or tab[1] == ent[3]) and tab not in tab_Entites:
                                tab_Entites.append(tab)
                # Choix des types d'etnités
                if tab[0] == 'nt':
                    for e in tab_Entites:
                        # Si le type aparait dans une des entites il faut le garder
                        if e[3] == tab[1] and tab not in tab_typeEntit:
                            tab_typeEntit.append(tab)

    # Reconstruction du dictionnaire a partir des données de maintenant
    dico_formater["1;nt;ntid;'ntname'"] = tab_typeEntit
    #print(tab_Entites,tab_sortantes, tab_entrantes)
    dico_formater["2;e;eid;'name';type;w;'formated name'"] = tab_Entites
    dico_formater["3;rt;rtid;'trname';'trgpname';'rthelp'"] = tab_typeRelat
    dico_formater["4;r;rid;node1;node2;type;w"] = tab_sortantes
    dico_formater["5;r;rid;node1;node2;type;w"] = tab_entrantes

    return dico_formater


#get.id
def getId(mot):
    f = open(os.path.join("selected_filed", f"selected_{motFormater(mot)}.txt"), "r", encoding="utf-8", errors="surrogateescape")
    id_line = f[1]
    id_string = id_line.split("=")
    id = id_string[-1].strip(")")
    return id




def rechercheASK(mot1, relation, mot2) :

    path = "ask_files"
    name = f"{motFormater(mot1)}_{relation}_{motFormater(mot2)}.txt"
    if os.path.exists(os.path.join(path, name)):
        r, w, anot = [line.strip() for line in open(os.path.join(path, name), "r", encoding="utf-8", errors="surrogateescape")]
        return r, w, anot
        
	# URL pour chercher si la relation 
    url = "https://www.jeuxdemots.org/rezo-ask.php?gotermsubmit=Demander&term1="+mot1+"&rel="+relation+"&term2="+mot2
    response = requests.get(url)

	# Recuperation des données de reseauDump dans body
    body = response.text

	# Recherche de la position de la première occurrence de la balise <CODE> pour récuperer les choses à l'interieur
    start_index = body.find("<RESULT>")

	# Recuperation du texte du code source
    selected = ""

	# Si le mot existe dans la base
    if start_index != -1:
        start_index += 8  # On rajoute la longueur de la balise <result>
        end_index = body.find("</RESULT>", start_index)

        if end_index != -1:
			# Extraction du contenu entre les balises <CODE> et </CODE>
            selected = body[start_index:end_index]

	# Sinon on regarde s'il y a un message d'erreur qui dit que le mot n'existe pas
    else:
        start_index_warning = body.find("<ERROR>")
        if start_index_warning != -1:
            print("\nUn des mots n'existe pas veuillez changer les entrées")
            exit(1)
        else : 
            print("\nErreur de la requete")
            exit(1)
	# Ecriture dans un texte
	#print(selected)

	# R
    r = ""
    start_index_r = selected.find("<R>")
    # Si le mot existe dans la base
    if start_index_r != -1:
        start_index_r += 3  # On rajoute la longueur de la balise <R>
        end_index_r = selected.find("</R>", start_index_r)

        if end_index_r != -1:
			# Extraction du contenu entre les balises <CODE> et </CODE>
            r = selected[start_index_r:end_index_r]
    #print("r : ", r)
	
    # W
    w = ""
    start_index_w = selected.find("<W>")
    # Si le mot existe dans la base
    if start_index_w != -1:
        start_index_w += 3  # On rajoute la longueur de la balise <R>
        end_index_w = selected.find("</W>", start_index_w)

        if end_index_w != -1:
			# Extraction du contenu entre les balises <CODE> et </CODE>
            w = selected[start_index_w:end_index_w]
    #print("w : ", w)
	
    # ANNOT
    anot = ""
    start_index_anot = selected.find("<ANOT>")
    # Si le mot existe dans la base
    if start_index_anot != -1:
        start_index_anot += 6  # On rajoute la longueur de la balise <R>
        end_index_anot = selected.find("</ANOT>", start_index_anot)

        if end_index_anot != -1:
            # Extraction du contenu entre les balises <CODE> et </CODE>
            anot = selected[start_index_anot:end_index_anot]

    if anot.strip() == '':
        anot = "VIDE"
    
    # Ecrire dans la BDD
    # remplacement pour éviter les problèmes
    with open(os.path.join(path, name), "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(f"{r}\n{w}\n{anot}")

    return r, w, anot

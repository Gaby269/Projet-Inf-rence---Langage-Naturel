import requests
import json
import os
from inferences import inferencesTotal
from parser import rechercheDUMP, rechercheASK, formaterDico
from utilities import *


if not os.path.exists("ask_files"):
    os.makedirs("ask_files")
if not os.path.exists("dump_files"):
    os.makedirs("dump_files")
if not os.path.exists("filter_files"):
    os.makedirs("filter_files")
if not os.path.exists("reponse_files"):
    os.makedirs("reponse_files")

# Heuristique on donne une valeur juste pour quelles soient définies
is_egalite = True
use_pourcentage = True
use_egalite = True
use_ask = True

# Demander à l'utilisateur de rentrer une phrase mot à mot
print("**************************\n* Choix de l'affirmation *\n**************************\n")
mot1 = input("Entrez un premier mot : ").strip()
relation = input("Entrez une relation (verbe infinitif) : ").strip()
mot2 = input("Entrez un second mot : ").strip()
print("\nLa phrase que vous avez entrée est :", mot1, relation, mot2)

# Demande à l'utilisateur si il veut des relations avec des égalité c'est à dire un animal est un animal
print("\n\n**************\n* Précisions *\n**************")
is_egalite = input("\nVoulez vous avoir des relations avec des égalités comme \"chocolat est du chocolat\" [y/n] ?").strip()
if is_egalite == "y":
    is_egalite = True
else:
    is_egalite = False

# Demande pour les euristiques
print("\n\n*************************\n* Choix des heuristiques *\n*************************")
# Pourcentage
use_pourcentage = input("\nHeuristique sur les pourcentages (plus long) [y/n] ? ").strip()
if use_pourcentage == "y":
    use_pourcentage = True
else:
    use_pourcentage = False
# Si l'utilisateur ne veut pas les égalités pour les résultats
if is_egalite == False:
    use_egalite = False  # on ne fait pas les heuristiques sur l'égalité
    use_ask = True  # on doit garder ask pour pouvoir avoir le tableau de note
# Sinon on demande si il veut les égalités, les ask ou les deux
else:
    # Ask ou égalité ou les deux
    use_reponse = input(
        "\nHeuristique avec les annotations de ask [1], sur les égalités [2] ou les deux [3] ? "
    ).strip()
    if use_reponse == "1":
        use_ask = True
        use_egalite = False
    elif use_reponse == "2":
        use_egalite = True
        use_ask = False
    else:
        use_egalite = True
        use_ask = True

relation = traductionFrancaisToChiffre(relation)
phr = [mot1, relation, mot2]
inferencesTotal(mot1, relation, mot2, is_egalite, use_egalite, use_ask, use_pourcentage)  # à modifier pour prendre en compte

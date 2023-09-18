# Projet Inférence Langage Naturel

## Description

Ce projet consistait à réaliser une sorte de questionnaire où on pose des questions simples comme "Est ce qu'un chat a des poiles ?" ou encore "Est ce qu'un lit peut voler ?". Le but était donc de créer un code qui permette à l'aide de la base [Jeux de Mots](https://www.jeuxdemots.org/jdm-accueil.php) de répondre à la question par oui ou par non et de fournir une explication. Pour cela nous devions nous aider de [reseauDUMP](https://www.jeuxdemots.org/rezo-dump.php) et [reseauASK](https://www.jeuxdemots.org/rezo-ask.php) (toujours de Jeux de Mots) pour pouvoir réussir à fournir une réponse et fournir plusieurs explications en classant ses dernières par pertinence. Nous devions donc avoir une interface qui permette de poser une question et cela fournissait la réponse et les explications.

Pour trouver les explications, nous devions faire des inférences à partir des relations déjà présentes dans Jeux de Mots. Par exemple pour la question "Est ce que un chat a des poils ?", pour trouver oui on devait chercher dans [reseauDUMP](https://www.jeuxdemots.org/rezo-dump.php) si la relation "chat r_has_part poiles" existait, puis pour trouver les explications, on a utilisé la déduction, l'induction ou encore la transitivité pour dire qu'un chat est un animal et que des animaux peuvent avoir des poils par exemple.

## Dossiers / Fichiers

- [ask_files](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/tree/main/ask_files) : Ensemble des fichiers des sélections des différentes requêtes faite à reseauAsk. Si on demande si le terme chat est en relation r_isa avec un animal, reseauASK va nous donner si la réponse est plausible ou non. C'est ce que nous enregistrons dans le fichier *_chat_r_isa_animal.txt_*.
- [dump_files](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/tree/main/dump_files) : Ensemble des fichiers des sélections des différentes requêtes faite à reseauDUMP. Si on demande les relations associées à chat on aura le fichier *_selected_chat.txt_* qui va se créer.
- [reponse_files](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/tree/main/reponse_files) : Ensemble des fichiers qui donne une réponse à la question d'origine pour les traitements suivants (explication).
- [hauristiques.py](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/blob/main/heuristiques.py) : Fichier qui contient les différentes fonctions d'heuristique utilisées
- [inferences.py](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/blob/main/inferences.py)  Fichier qui contient les fonctions d'inférence utilisées dans le projet : déduction, induction, transitivité.
- [main.py](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/blob/main/main.py) : Fichier principale, qui demande aux utilisateur de poser la question ainsi que de choisir les heuristiques proposées qui sont plus ou moins longue à faire.
- [parser.py](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/blob/main/parser.py) : Fichier qui contient les différentes fonctions pour parser les fichiers stockées au cours de l'éxécution du code.
- [utilities.py](https://github.com/Gaby269/Projet_Inference_Langage_Naturel/blob/main/utilities.py) : Fichier qui contient toutes les autres fonctions dont nous avons besoin pour le projet comme les traductions des différentes relations en chiffre, ou en français.

## Utilisation

```bash
python main.py
```

ou

```bash
python3 main.py
```

Celon si vous utiliser python ou python3, il faut rajouter un 3. Puis, suivre les informations indiquées sur le terminal.

## Paramètres

Valeur par défaut est "non" si vous n'entrez pas de valeur.

- **_Relation d'égalité_** : exemple "chocolat est du chocolat" [y/n]
- **_Heuristique de pourcentage_ (très long)** : exemple 50% des animaux sont des animaux qui volent parmi les animaux
- **_Heuristique sur les annotations_** : [3] par défaut pour les deux

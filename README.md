# Projet langage Naturel

## Description

Ce projet consistait à réaliser une sorte de questionnaire où on pose des questions simple comme "Est ce qu'un chat a des poiles ?" ou encore "Est ce que un lit peut voler ?". Le but été donc de créer un code qui permette à l'aide de la base [Jeux de Mots](https://www.jeuxdemots.org/jdm-accueil.php) de répondre à la question par oui ou par non et de fournir une explication. Pour cela nous devions nous aider de [reseauDUMP](https://www.jeuxdemots.org/rezo-dump.php) et [reseauASK](https://www.jeuxdemots.org/rezo-ask.php) (toujours de Jeux de Mots) pour pouvoir réussir à fournir une réponse et fournir plusieurs explications en classant ses dernières par pertinance. Nous devions donc avoir une interface qui permette de poser une question et cela fournissait la réponse et les explications.

Pour trouver les explications, nous devions faire des inferences à partir des relations déjà présente dans Jeux de Mots. Par exemple pour la question "Est ce que un chat a des poils ?", pour trouver oui on devait chercher dans [reseauDUMP](https://www.jeuxdemots.org/rezo-dump.php) si la relation "chat r_has_part poiles" existait, puis pour trouver les explications, on a utilisé la déduction, l'induction ou encore la transitivité pour dire qu'un chat est un animal et que des animaux peuvent avoir des poils par exemple.

## Utilisation

```bash
python main.py
```

ou

```bash
python3 main.py
```

Celon si vous utiliser python ou python3, il faut rajouter un 3. Puis, suivre les informations indiqué sur le terminal.

## Paramètres

Valeur par défault est "non" si vous n'entrez pas de valeur.

- **_Relation d'égalité_** : exemple "chocolat est du chocolat" [y/n]
- **_Heuristique de pourcentage_ (très long)** : exemple 50% des animaux sont des animaux qui volent parmis les animaux
- **_Heuristique sur les annotations_** : [3] par défault pour les deux

# Projet langage Naturel

## Description

Ce projet consistait a réaliser une sorte de questionnaire où on pose des questions simple comme "Est ce qu'un chat a des poiles" ou encore "Est ce que un lit peut voler". Le but été donc de créer un code qui permette à l'aide de la base Jeux de Mots de répondre à la question par oui ou par non et de fournir une explication. Pour cela nous devions nous aider de reseauDUMP et reseauASK (toujours de Juex de Mots) pour pouvoir réussir à fournir une réponse et fournir plusieurs explications en classant ses dernières par pertinance. Nous devions donc avoir une interface qui permette de poser une question et cela founissait la réponse et les explications.

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
- **_Heuritique sur les annotations_** : [3] par défault pour les deux

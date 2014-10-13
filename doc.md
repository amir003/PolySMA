PolySMA : modélisation de protéines et de leurs interactions dans un environnement 3D
=====================================================================================

Introduction
------------

Ce programme a été fait pour l'igem 2014 dans le cadre du projet Elasticoli. Ce projet s'intéresse à la production synthétique de protéines élastiques par la bactérie Escherichia coli. Ces protéines élastiques, aussi appelées ELP (Elastine Like Protein), ont pour caractéristiques de s'associer entre elles et peuvent former des agréggats (ou des fils dans certaines conditions).

PolySMA a été conçu pour essayer de mieux comprendre comment ces protéines s'associer. En effet, polySMA est un programme ayant pour objectif de modéliser ces protéines et leurs interactions dans un environnement en trois dimensions.

Analyse
-------

Nous nous intéressons ici qu'à modéliser un type de protéine. Il faut modéliser plusieurs protéines dans un environnement à trois dimensions, ensuite elles vont être déplacées et possiblement s'associer.

**Modélisation des protéines**

Pour modéliser simplement une protéine, celle-ci pourrait être représentée par une forme sphérique lorsqu'elle est isolée (non-associée à d'autres protéines). Il a été observé en laboratoire qu'après association l'agrégat ainsi formé a un volume inférieur à la somme des volumes initiaux de chaque élément de l'agrégat. En effet un agrégat de 100 protéines fait environ le volume de 1,5 fois de celui de la protéine isolé. Cette forme sphérique de départ d'une protéine pourrait donc évoluer en fonction du nombre d'associations et avoir tendance à occuper donc moins de place dans ces conditions.

**Règles d'association et de déplacement**

Pour savoir si les protéines s'associent il faut prendre en compte plusieurs éléments. Tout d'abord la probabilité de rencontre, pour prendre ce paramètre en compte il faut simuler les mouvements des protéines dans un espace 3D (Cet espace étant celui de la cellule par exemple). Mais il ne s'agit pas simplement de savoir que la protéine sera à un endroit A puis un endroit B, il s'agit aussi de s'avoir où elle sera entre ces deux points car elle ne se déplace pas en ligne droite.

Pour prendre en compte cette probabilité de rencontre, il a été choisi de déplacer la protéine par petits mouvements. Chaque mouvement étant déterminé aléatoirement et n'excédant pas la taille de la protéine, nous savons quel est le chemin emprunté par chaque protéine simulé.

Si deux protéines sont suffisament proches, il faut alors déterminer si elles s'associent. Il ne faudra pas oublier de prendre en compte une probabilité d'association car la réaction qui le permet a une certaine probabilité de se produire. Si l'association ne se produit les protéines vont alors s'éloigner l'une de l'autre (principe d'attraction-répulsion).

Il a aussi été demandé de pouvoir modifier la température dans le modèle simulé. La température a pour effet d'augemnter la réaction notamment en augmentant la probabilité de rencontre par le biais de l'agitation thermique. Ceci peut donc être modélisé en augmentant la vitesse des protéines et donc la distance parcourue pour un même pas de temps simulé.

Enfin, lors du déplacement d'une protéine, il faudra choisir ce qu'il se produit lorsque celle-ci arrive au bord de l'environnement simulé.

**État de l'art des logiciels de modélisation 3D**

Maintenant que nous savons ce que nous allons simuler, il faut aussi l'afficher et interagir avec l'utilisateur. Pour cela, il faut donc choisir un programme ou des librairies permettant de modéliser en 3 dimensions et permettant à l'utilisateur d'interagir avec cette visualisation (qu'il puisse par exemple "se déplacer" dans celle-ci).

*Blender*

Blender dispose d'une interface permettant à l'utilisateur d'interagir avec l'environnement 3D créé. Ce logiciel présente aussi la possibilité d'animer les objets (prise en compte du temps).Enfin le logiciel propose une API en python facilement accessible.

*Soya3D et vPython*

Soya3D et vPython sont des modules python permettant de représenter en 3D des objets. Cependant, par défault, à l'éxecution, il présente une fenêtre trop simple perettant peu 'interactions avec l'utilisateur.

Blender a donc été choisi pour plus de simplicité. Le language utilisé pour programmer sera donc python 3.

Conception
----------

**L'environnement simulé**

L'environnement de simulation, c'est à dire l'endroit où les protéines peuvent se déplacer, sera représenté par un cube d'une dimension choisi par l'utilisateur.

L'utilisateur pourra donc choisir la taille de l'environnement et aussi le nombre de protéines simulées. En paramétrant ces deux variables, la concentration de protéines dans l'environnement est changé.

Comme dit précédemement, lors du déplacement d'une protéine, il faut choisir ce qu'il se produit lorsque celle-ci arrive au bord de l'environnement simulé.  Ici, la simulation va feindre un domaine infini en repliant l'espace bord à bord (appélé configuration torique). Par exemple, si une protéine arrive en bas du cube simulé, elle est alors placée en haut de ce dernier.

**Les protéines simulées**

Comme dit précédemment, les protéines sont simulées par des grains (ou objet sphérique). Dans cette simulation, nous avons besoin de deux types d'informations : celles liées au grain biologique (coordonées, positions des sites de liaison,...) et celles liées au grain simulé (objet blender,..).

Il serait donc logique d'utiliser une structure "grain biologique" qui stockerait pour chaque protéine :
  - les informations de coordonées
  - les positions des sites de liaison
  - les protéines auquelles elle est attachée
  - la probabilité d'association avec une autre protéine

La structure grain simulé quant à elle contiendrait :
  - le grain biologique
  - l'objet blender
  - information disant si le grain a été déplacé dans le tour de déplacement actuel

Ces informations sont résumées ci dessous :
![Diagramme_Classe](https://raw.githubusercontent.com/amir003/PolySMA/master/ressources/classes_conception.png)

*Placement initial des protéines*

Pour le placement initial des protéines, le programme va tout d'abord déterminé aléatoirement leur position.

Les sites actifs sont positionnés aux mêmes endroits pour toutes les sphères, ces endroits étant déterminés aléatoirement et répartis de façon uniforme. Ensuite, le programme applique une rotation aléatoire sur chaque sphére créée.

*Déplacement des protéines*

Comme dit précédemement, les protéines sont déplacés aléatoirement par petits mouvements (chacun n'exédant pas la taille de la protéine). Les protéines à déplacer sont choisies au hasard et sont toutes déplacées une fois durant chaque tour.

Lors de chaque déplacement, si une protéine est suffisament proche le programme teste l'association et détermine quels sont les deux sites qui vont se lier. S'il y a association, la zone du site actif va être rapprochée du centre (compression) et la probabilité d'accrochage des sites adjacents augmente.

Fonctionnement de l'interface
-----------------------------

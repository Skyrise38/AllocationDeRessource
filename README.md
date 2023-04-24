
# __I -  Librairies à installer__
Si vous utilisez l'environnement anaconda il vous suffira de réaliser les commandes suivantes : 
```
pip install gurobipy
pip install munkres
```
Si vous n'utilisez pas anaconda il faudra installer les librairies avec les commandes suivantes : 

```
pip install pandas
pip install gurobipy
pip install tkinter
pip install openpyxl
pip install munkres
pip install matplotlib
pip install more-itertools
```

Vous aurez peut être à changer pip par pip3 ou conda selon ce que vous utiliser. 

# __II -  Installer la licence universitaire de Guroby__

Guroby est un algorithme développé par GUROBI OPTIMIZATION. Nous utilisons leur algorithme pour générer les solutions de projets attribués. 

La version gratuite ne permet pas de résoudre des problèmes trop complexes il faudra donc pour utiliser notre programme importer la license universitaire gratuite. 

Pour l'installer il faudra :

- Créer un compte sur leur site avec votre adresse universitaire : https://www.gurobi.com/

- Ensuite il faudra vous connecter au VPN de l'UGA car il faut être relié à une adresse ip universitaire pour cela suivez les indications sur le site suivant : https://services-numeriques-personnels.univ-grenoble-alpes.fr/menu-principal/connexions/le-vpn-acces-au-reseau-distant-/le-vpn-acces-au-reseau-distant--217742.kjsp

- Connectez vous sur https://www.gurobi.com/ avec vos identifiants 
- Allez ensuite dans Licenses -> Request -> Named-User Academic -> Generate Now !

- Acceptez les conditions et cliquez sur CONFIRM REQUEST (Si jamais vous avez un message d'erreur "Academic Domain Error" c'est que vous n'êtes pas connecté au VPN de l'UGA)

- Après cela vous pouvez aller dans Licenses->Licenses et vous devriez voir votre license apparaître. 

- Cliquez ensuite sur INSTALL et suivez les instructions 

# __III -  Comment utiliser l'application__

- 1-  En arrivant sur l'interface graphique vous avez le choix entre 2 algorithmes pour répartir les élèves dans les projets: 
    - Munkres : cet algorithme permet d'avoir l'ensemble des solutions disponibles et vous permettra de selectionner celle qui vous convient le mieux. Cet algorithme est en revanche assez long à trouver les solutions.
    - Guroby : cet algorithme est beaucoup plus rapide que le premier en revanche il ne vous sera pas possible de changer de solution. 
- 2- Vous devrez dans un second temps choisir le fichier excel dans lequel les étudiants auront fait leurx choix. Une fois celui-ci selectionné vous devrez pouvoir visualiser le nom de celui-ci.

- 3- Cliquez ensuite sur le bouton "Generer solution" pour générer le tableau d'attribution. Attention l'excel ne sera pas encore enregistré.

- 4- Vous pouvez prévisualiser votre excel avec le bouton "Afficher"

- 5- Si la répartition des élèves vous convient vous pouvez l'enregistrer avec le bouton "Enregitrer" en ayant au préalable rentré un nom de excel. 
- 6- Le fichier sera enregistré dans le dossier ou est lancé de programme. 

 

# Auteurs

* **LOMBARD Loris** _alias_ [@Skyrise38](https://github.com/Skyrise38)
* **MOREL Raphaël** _alias_ [@Ralf622](https://github.com/Ralf622)
* **TRAN Robin** _alias_ [@RobinTran1](https://github.com/RobinTran1)
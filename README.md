![](logo/logo.svg)

# Projet de Securité des Applications Nomades

---

## Instructions de configuration du projet

Tout d'abord il faut exécuter la commande :

```source ./venv/bin/activate```

pour se placer dans le venv

Ensuite il faut installer les dépendances :

```pip install -r requirements.txt```

# Utilisation de l'outil

Pour lancer l'interface graphique il suffit d'exécuter la commande :

```python3 main.py```

Il est ensuite possible de choisir un fichier APK en haut. Après avoir sélectionné le fichier APK, un temps d'analyse de quelques dizaines de secondes est alors déclanché pour charger l'apk et alimenter les différents objets en mémoire.
Ensuite, il est possible de sélectionner une classe à analyser puis une analyse.
Une fois cela fait, un clic sur le bouton "Analyser" créera des fichiers de rapport dans le dossier out.

CAS DE TESTS :
L'APK apk/TEST_APK_1.apk contient des cas de tests pour les analyses 1 et 2 (les sources de ce fichier APK sont dans le dossier source_TEST_APK_1):
 - Pour essayer l'analyse 1, il est possible de sélectionner les classes commençant par "Check".
 - Pour essayer l'analyse 2, il faut sélectionner la classe CheckInheritance.

L'APK apk/commu2.apk contient un cas de test pour l'analyse 3.


Note : l'apk de test invalide contient un test qui fait planter le programme


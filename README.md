# GesUniversity

GesUniversity est une application desktop de gestion scolaire robuste et moderne développée en Python avec CustomTkinter. Conçue spécifiquement pour répondre aux besoins opérationnels de l'**Institut Supérieur Polytechnique Sainte Lucie d'Oyo (ISPSL)**, elle permet de centraliser et d'automatiser l'intégralité des flux administratifs : inscriptions, réinscriptions, encaissement des mensualités, génération de reçus PDF, suivi des impayés, consultation de la liste des élèves et gestion des archives scolaires.

## Logo du projet

## Sommaire

1. [Objectif du projet](#objectif-du-projet)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Technologies utilisées](#technologies-utilisées)
4. [Architecture du projet](#architecture-du-projet)
5. [Structure du dépôt](#structure-du-dépôt)
6. [Prérequis](#prérequis)
7. [Installation](#installation)
8. [Initialisation de la base de données](#initialisation-de-la-base-de-données)
9. [Lancement de l'application](#lancement-de-lapplication)
10. [Identifiants administrateur](#identifiants-administrateur)
11. [Compilation & Distribution (Nuitka)](#compilation--distribution-nuitka)
12. [Gestion de la Base de Données en Production](#gestion-de-la-base-de-données-en-production)
13. [Besoin d'aide ou de support](#besoin-daide-ou-de-support)

---



## Objectif du projet

L'objectif principal de GesUniversity est de fournir à l'administration de l'ISPSL un outil bureautique hors-ligne, fluide, sécurisé et prêt à l'emploi. Il élimine le suivi manuel sur papier ou tableur en offrant une traçabilité rigoureuse des transactions financières et un accès instantané aux dossiers administratifs des étudiants.

---



## Fonctionnalités principales

- 📝 **Inscriptions & Réinscriptions :**
  - Création complète de dossiers étudiants avec validation stricte des données.
  - Réinscription rapide pour le renouvellement annuel des élèves.
- 💳 **Gestion des Paiements Mensuels :**
  - Recherche instantanée d'étudiants par matricule, nom ou classe.
  - Encaissement des frais de scolarité, droits d'inscription et frais annexes.
  - Impression et exportation automatisées de reçus de paiement au format PDF via ReportLab.
- 📋 **Consultation des Étudiants :**
  - Affichage dynamique des élèves inscrits filtrable par classe, option et année académique.
  - Modales détaillées de profil étudiant.
- 📊 **Suivi des Paiements & Rapports :**
  - Tableau de bord des règlements mensuels.
  - État des impayés par promotion et génération de rapports imprimables.
- 📁 **Archives Étudiants :**
  - Consultation et recherche dans les bases d'archives des années scolaires précédentes.
- 🛡️ **Espace Administration :**
  - Accès restreint protégé par authentification.
  - Gestion globale des paramètres scolaires, des classes et clôture des années académiques.

---



## Technologies utilisées

- **Langage principal :** Python 3.13+
- **Interface Graphique (GUI) :** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) pour une interface moderne en mode sombre/clair natif.
- **ORM & Base de données :** [SQLAlchemy](https://www.sqlalchemy.org/) avec **SQLite** pour un stockage local, autonome et sans serveur.
- **Génération de documents :** [ReportLab](https://www.reportlab.com/) pour la création dynamique de reçus et rapports PDF.
- **Composants d'interface :** `TkCalendar` (sélecteurs de dates) et `Pillow` (gestion des images et logos).
- **Compilation C++ Native :** [Nuitka](https://nuitka.net/) pour la génération d'exécutables autonomes hyper-performants.
- **Gestionnaire d'environnement :** [uv](https://astral.sh/uv) (Astral) pour une gestion ultra-rapide des dépendances Python et de l'environnement virtuel.
- **Tests :** `pytest` pour les tests unitaires et d'intégration.

---



## Architecture du projet

Le projet applique une architecture en couches type **MVC (Model-View-Controller)** couplée au pattern **Repository / Service**, garantissant une séparation nette des responsabilités, un code maintenable et facilement testable :

- `models/` : Définition des entités SQLAlchemy (Mappage BDD) et des DTOs (*Data Transfer Objects*).
- `repositories/` : Couche d'accès aux données. Encapsule toutes les requêtes SQLite/SQLAlchemy.
- `services/` : Logique métier, règles de validation et opérations financières/administratives.
- `controllers/` : Intermédiaire entre la logique métier et l'interface graphique.
- `interfaces/` : Vues CustomTkinter, formulaires, tableaux et fenêtres modales.
- `database/` : Configuration des sessions SQLAlchemy et gestion du cycle de vie de la connexion SQLite.

---



## Structure du dépôt

```text
GesUniversity/
├── assets/             # Ressources statiques (logos, images, icônes)
├── config/             # Paramètres de configuration globaux
├── controllers/        # Contrôleurs métier de l'application
├── data/               # Dossier hôte de la base de données SQLite (school.db)
├── database/           # Session DB, engine et scripts de connexion
├── interfaces/         # Vues, formulaires et composantes CustomTkinter
├── models/             # Entités SQLAlchemy et modèles de données
├── repositories/       # Couche d'accès aux données (SQLAlchemy)
├── services/           # Logique applicative et règles métier
├── seed/               # Scripts d'initialisation et données de démonstration
├── main.py             # Point d'entrée principal de l'application
├── pyproject.toml      # Configuration du projet Python et dépendances
├── uv.lock             # Fichier de verrouillage des dépendances uv
└── README.md           # Documentation du projet
```

---



## Prérequis

Avant de lancer l’application ou de procéder à la compilation, veillez à disposer de :

1. **Python 3.13+**
2. `uv` **(Gestionnaire de paquets Astral)** : [Instructions d'installation](https://astral.sh/uv) `uv`
3. **Microsoft Visual C++ Redistributable 2015-2022** (nécessaire sur l'ordinateur de développement pour la compilation C++ via Nuitka).

---



## Installation

1. Cloner le dépôt Git du projet :
  ```bash
   git clone <url-du-depot>
   cd GesUniversity
  ```
2. Synchroniser et créer l'environnement virtuel avec `uv` :
  ```bash
   uv sync
  ```

*(Optionnel, si vous utilisez le gestionnaire* `pip` *standard)* :

```bash
pip install -e .
```

---



## Initialisation de la base de données

La base de données SQLite est initialisée et peuplée via les scripts de seed. Pour créer les tables et alimenter le système avec le jeu de données initial, exécutez :

```bash
uv run -m seed.db_test
```

Ou via Python standard :

```bash
python -m seed.db_test
```

> **Remarque :** Le fichier `school.db` sera généré automatiquement dans le dossier `data/`.

---



## Lancement de l'application

Pour exécuter l'application en mode développement :

```bash
uv run main.py
```

Ou :

```bash
python main.py
```

---



## Identifiants administrateur

L'accès au panneau d'administration s'effectue avec les identifiants par défaut suivants :

- **Nom d'utilisateur :** `admin`
- **Mot de passe :** `admin123`

---



## Compilation & Distribution (Nuitka)

Pour distribuer l'application sous forme de programme autonome sans nécessiter l'installation de Python sur l'ordinateur cible, nous utilisons **Nuitka**.

### Commande de compilation

Depuis la racine du projet, lancez :

```bash
uv run nuitka --standalone \
  --windows-console-mode=disable \
  --enable-plugin=tk-inter \
  --include-data-dir=assets=assets \
  --include-data-files=LICENSE=LICENSE \
  --windows-icon-from-ico=assets/app_icon.ico \
  main.py
```



### Signification des options :

- `--standalone` : Produit un dossier complet (`main.dist`) contenant l'exécutable et l'ensemble de ses dépendances.
- `--windows-console-mode=disable` : Supprime la fenêtre d'invite de commande noire au lancement de la GUI.
- `--enable-plugin=tk-inter` : Inclut et configure les dépendances graphiques de Tkinter/CustomTkinter.
- `--include-data-dir=assets=assets` : Copie le dossier `assets/` (images, logo) à l'intérieur du dossier compilé.
- `--include-data-files=LICENSE=LICENSE` : Copie le fichier de licence `LICENSE` directement à la racine du dossier compilé.
- `--windows-icon-from-ico=assets/app_icon.ico` : Applique l'icône de l'application à l'exécutable `.exe` sous Windows.

---



## Gestion de la Base de Données en Production

Afin d'éviter toute perte de données lors des mises à jour applicatives, **la base de données** `school.db` **est conservée en dehors de l'exécutable**.

### Procédure de préparation du livrable final :

1. À la fin de la compilation, ouvrez le dossier `main.dist/` généré à la racine.
2. Copiez votre dossier `data/` (contenant le fichier `school.db`) directement dans `main.dist/`, au même niveau que `main.exe`.
3. Vous obtenez la structure de distribution suivante :

```text
main.dist/
├── assets/          # Fichiers graphiques (gérés automatiquement par Nuitka)
├── data/            # Dossier externe contenant la base de données SQLite
│   └── school.db
├── main.exe         # Exécutable principal de l'application
└── ...              # Bibliothèques DLL et binaires C++
```

1. Compressez l'intégralité du dossier `main.dist` au format `.zip` pour diffusion aux utilisateurs finaux.

---



### Besoin d'aide ou de support ?

Pour toute question, suggestion ou rapport de bug :

- 📧 Consultez la section *Issues* du dépôt
- 📖 Vérifiez la documentation technique dans les fichiers du projet
- 💬 N'hésitez pas à contribuer via des *Pull Requests*


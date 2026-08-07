# GesUniversity

GesUniversity est une application desktop de gestion scolaire développée en Python avec Tkinter/CustomTkinter. Elle permet de gérer les inscriptions, les paiements mensuels, la consultation des élèves, le suivi des paiements et la gestion des années académiques depuis une interface simple et moderne.

## Objectif du projet

Ce projet a été conçu pour faciliter la gestion administrative d’un établissement scolaire, notamment l’ISPSL D’Oyo. Il centralise les opérations courantes liées aux étudiants et aux paiements dans un outil unique.

## Fonctionnalités principales

- Inscription de nouveaux étudiants
- Réinscription annuelle des élèves
- Gestion des paiements mensuels
- Génération de reçus et de rapports PDF
- Consultation de la liste des étudiants
- Suivi des paiements par mois et par classe
- Gestion des années académiques
- Accès administrateur protégé par authentification

## Technologies utilisées

- Python 3.14+
- CustomTkinter pour l’interface graphique
- SQLAlchemy pour l’accès aux données
- **SQLite** pour le stockage local et léger de la base de données
- ReportLab pour la génération de fichiers PDF
- TkCalendar pour les sélecteurs de dates
- Pytest pour les tests
- **[uv](https://astral.sh/uv)** : Gestionnaire de packages et d'environnements virtuels extrêmement rapide écrit en Rust, utilisé comme outil principal pour la gestion des dépendances et de l'environnement du projet.

## Architecture du projet

Le projet suit une architecture MVC (Model-View-Controller) avec séparation claire des responsabilités :

- **Models** : représentation des entités métier et DTOs
- **Repositories** : accès aux données et requêtes SQLAlchemy
- **Services** : logique métier et règles de validation
- **Controllers** : coordination entre l’interface et les services
- **Interfaces** : formulaires et vues graphiques

## Structure du dépôt

- `controllers/` : contrôleurs de chaque module fonctionnel
- `interfaces/` : vues et formulaires Tkinter/CustomTkinter
- `services/` : logique métier
- `repositories/` : accès aux données
- `models/` : modèles et objets de transfert de données
- `database/` : configuration, gestion des sessions et connexion SQLite
- `config/` : paramètres de configuration
- `seed/` : scripts d'initialisation et données de test
- `temp/` : fichiers temporaires et ressources utiles

## Prérequis

Avant de lancer l’application, assurez-vous d’avoir :

- Python installé sur votre machine
- L'outil **`uv`** installé (consultez le site officiel [uv (Astral)](https://astral.sh/uv))

## Installation

1. Cloner le projet
2. Synchroniser l'environnement et installer les dépendances avec `uv` :

```bash
uv sync
```

ou, si vous utilisez `pip` :

```bash
pip install -e .
```

## Initialisation de la base de données

La base de données du projet est gérée sous **SQLite**. Pour créer et alimenter la base de données avec le jeu de données initial, vous devez exécuter le module `db_test` situé dans le package `seed`.

Exécutez la commande suivante :

```bash
uv run -m seed.db_test
```

ou avec Python standard :

```bash
python -m seed.db_test
```

> **Note :** Les paramètres de configuration de la connexion SQLite se trouvent dans les dossiers `config/` et `database/`.

## Lancement de l’application

Pour démarrer l’application en mode développement, exécutez :

```bash
uv run main.py
```

ou :

```bash
python main.py
```

## Identifiants administrateur

L’interface d’administration utilise les identifiants suivants par défaut :

- **Nom d’utilisateur :** `admin`
- **Mot de passe :** `admin123`

## Compilation de l'application

Le projet intègre **PyInstaller** dans ses dépendances pour compiler l'application Python en un exécutable autonome (`.exe` sous Windows ou binaire sous Linux/macOS).

Pour générer l'exécutable, lancez la commande suivante depuis la racine du projet :

```bash
uv run pyinstaller --noconsole --onefile main.py
```

### Explications des options :

- `--onefile` : Regroupe l'application et l'ensemble de ses dépendances dans un fichier unique.
- `--noconsole` : Masque la fenêtre de terminal au lancement de l'interface graphique CustomTkinter.

Si votre application nécessite d'embarquer des fichiers de ressources statiques ou le dossier `temp/`, vous pouvez les inclure lors de la compilation :

```bash
uv run pyinstaller --noconsole --onefile --add-data "temp:temp" main.py
```

Une fois la compilation terminée, l'exécutable généré se trouve dans le dossier `dist/`.

## Notes importantes

- Les interfaces utilisateur sont entièrement en français, conformément au besoin métier du projet.
- Assurez-vous d'avoir exécuté la commande d'initialisation de la base de données (`uv run -m seed.db_test`) avant le premier lancement.

## À venir / améliorations possibles

- Ajout de davantage de rapports et de statistiques
- Amélioration de l’interface utilisateur
- Sécurisation accrue des accès administrateur
- Intégration de tests automatisés plus complets
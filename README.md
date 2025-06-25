# 🎬 Movie_Predict – Système de Prédiction des Admissions Cinéma

> **Projet d'équipe - MVP sur 1 mois, méthode Agile (Jira, GitHub synchronisés)**

Movie_Predict est une solution complète basée sur une architecture microservices pour **prédire les entrées en salle d’un film avant sa sortie**. Le projet combine **scraping**, **machine learning**, **automatisation Airflow**, **API FastAPI**, et une interface web en **Django + Tailwind**.

L’objectif est d’aider les gérants de salles à anticiper les performances des films et optimiser l’affectation des salles, la stratégie marketing et les ressources.

---

## 🧪 Dépendances principales

![python](https://img.shields.io/badge/python-3.11-blue.svg)
![fastapi](https://img.shields.io/badge/fastapi-0.110.2-blue.svg)
![uvicorn](https://img.shields.io/badge/uvicorn-0.29.0-blue.svg)
![sqlmodel](https://img.shields.io/badge/sqlmodel-0.0.18-blue.svg)
![passlib](https://img.shields.io/badge/passlib-1.7.4-blue.svg)
![pyjwt](https://img.shields.io/badge/pyjwt-2.8.0-blue.svg)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-blue.svg)
![pydantic](https://img.shields.io/badge/pydantic-2.7.1-blue.svg)
![alembic](https://img.shields.io/badge/alembic-1.13.1-blue.svg)
![airflow](https://img.shields.io/badge/airflow-2.9.1-blue.svg)
![requests](https://img.shields.io/badge/requests-2.32.3-blue.svg)
![xgboost](https://img.shields.io/badge/xgboost-2.0.3-blue.svg)
![pandas](https://img.shields.io/badge/pandas-2.2.2-blue.svg)
![cloudpickle](https://img.shields.io/badge/cloudpickle-3.0.0-blue.svg)
![gunicorn](https://img.shields.io/badge/gunicorn-22.0.0-blue.svg)
![python-jose](https://img.shields.io/badge/python--jose-3.3.0-blue.svg)
![django](https://img.shields.io/badge/django-5.0.6-blue.svg)
![tailwind](https://img.shields.io/badge/tailwindcss-3.4.1-blue.svg)
![scrapy](https://img.shields.io/badge/scrapy-2.12.0-blue.svg)
![django_browser_reload](https://img.shields.io/badge/django__browser__reload-1.12.1-blue.svg)

---

## 📑 Sommaire

- [📁 Structure du projet](#-structure-du-projet)
- [🎯 Objectifs métier](#-objectifs-métier)
- [🧱 Architecture](#-architecture)
- [🚀 Installation](#-installation)
- [🔧 Configuration](#-configuration)
- [🏃 Utilisation](#-utilisation)
- [📊 Fonctionnalités](#-fonctionnalités)
- [📉 Exemple de prédictions](#-exemple-de-prédictions)
- [💰 Estimation des coûts cloud](#-estimation-des-coûts-cloud)
- [🤝 Contribution](#-contribution)

---

## 📁 Structure du Projet

```bash
Movie_Predict/
├── automation_folder/     # Automatisation du scraping et des prédictions (ex: Airflow, Cron, scripts de planification)
├── cinema_prediction/     # API FastAPI pour exposer les prédictions du modèle
├── data_scraping/         # Traitement des données extraites, nettoyage, enrichissement, et feature engineering
├── moviescraper/          # Projet Scrapy initial pour le scraping d'IMDb
├── weekly_scraping/       # Scraping hebdomadaire pour les nouveaux films à prédire
│
├── .gitignore             # Fichiers/dossiers ignorés par Git
├── README.md              # Documentation du projet (ce fichier)
├── all_workflow.py        # Script de coordination scraping + prédiction (pipeline manuel ou déclenché)
├── requirements.txt       # Dépendances Python du projet
├── run_scraping.py        # Point d’entrée pour lancer le scraping (exécution directe)
├── scrapy.cfg             # Configuration du projet Scrapy

```

## 🎯 Objectifs Métier

    - Estimer les entrées des films à venir (avant leur sortie en salle)

    - Optimiser la gestion des salles, la rentabilité et la planification

    - Offrir une visualisation claire et actionnable au gérant

## 🧱 Architecture

    - 🧠 Modèle ML de régression (XGBoost / scikit-learn)

    - 🔌 API FastAPI exposant les prédictions

    - 🕸️ Scraping hebdomadaire automatisé (Airflow + Scrapy)

    - 🌐 Interface Django / Tailwind pour le dashboard

    - 💾 BDD analytique (prédiction + données cinéma)

    - 🧱 Docker pour tous les services (déploiement prod)

    - ☁️ Azure ML Studio & Azure SQL (optionnel / budgeté)

## 🚀 Installation
1. Cloner le repo

git clone https://github.com/ton-org/Movie_Predict.git
cd Movie_Predict

2. Lancer les services
docker-compose up --build -d

3. Activer Airflow
cd airflow
./deploy_airflow.sh

4. Lancer Django
cd django_app
python manage.py runserver

5. Lancer FastAPI

cd api
uvicorn main:app --reload --port 8001

## 🔧 Configuration
Créer un fichier .env à la racine de chaque composant (api, django_app, airflow), avec par exemple :

DATABASE_URL=sqlite:///./db.sqlite3
SECRET_KEY=...
JWT_ALGORITHM=HS256


## 🏃 Utilisation

    🔁 Scraping IMDB hebdomadaire via Airflow

    🧠 API FastAPI consultée par l’app Django

    📉 Dashboard avec :

        Top 10 sorties à venir + estimation

        Comparatif prédiction vs réalité

        Chiffres : CA, occupation, croissance

    🔎 Historique des prédictions & performance du modèle

## 📊 Fonctionnalités
| Module             | Description                           |
| ------------------ | ------------------------------------- |
| `Airflow`          | Pipeline scraping et prédiction       |
| `FastAPI`          | API REST pour exposer les prédictions |
| `Django`           | Interface web avec dashboard          |
| `Scrapy`           | Scraping de films IMDB                |
| `XGBoost`          | Régression (entrées cinéma)           |
| `MLFlow` (AzureML) | Suivi des expériences                 |
| `SQLite`           | Historique des prédictions            |
| `Tailwind`         | UI moderne et responsive              |

## 📉 Exemple de prédictions
| 🎬 Film                      | 🎯 Estimation entrées | 📅 Date de sortie |
| ---------------------------- | --------------------- | ----------------- |
| **Deadpool & Wolverine**     | 1 200 000             | 2025-07-24        |
| **Le Comte de Monte Cristo** | 850 000               | 2025-07-10        |
| **Vice-Versa 2**             | 2 100 000             | 2025-06-19        |

## 💰 Estimation des Coûts Cloud
| Composant             | Ressource Azure             | Coût estimé / mois |
| --------------------- | --------------------------- | ------------------ |
| Azure App Service     | API FastAPI déployée        | \~20 €             |
| Azure ML Studio       | ML Training/Tracking        | \~50 €             |
| Azure SQL Database    | BDD historique + analytique | \~15 €             |
| Azure VM pour Airflow | Automatisation (Linux B1s)  | \~25 €             |
| **Total estimé**      |                             | **\~110 € / mois** |

## 📬Contact

Pour toute question ou suggestion :

### ✉️ delvoyeadf@gmail.com  

<p align="left">
  <img src="prime_assurance/static/images/logo_entreprise.png" alt="Logo de l'Entreprise" width="300" height="auto">
</p>

<div>
<h4>Antoine Delvoye </h4>
<a href = "mailto: delvoyeadf@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="www.linkedin.com/in/antoine-delvoye1" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
</a>  
<a href="https://github.com/A-Delvoye" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
</a>
</div>

<div>
<h4>Sami Kabdani </h4>
<a href = "mailto: samikabdani.pro@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/hacene-z" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
</a>  
<a href="https://github.com/Sami-Kbdn" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
</a>
</div>

<div>
<h4>Gauthier Vannesson </h4>
<a href = "mailto: g.vannesson@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/gauthier-vannesson-6444a2179/" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
</a>  
<a href="https://github.com/gvannesson" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
</a>
</div>

<div>
<h4>David Scott </h4>
<a href = "mailto: david.scott.2875@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/david-scott-051a132b5/" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
</a>  
<a href="https://github.com/Daviddavid-sudo" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
</a>
</div>
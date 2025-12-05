# 🐧 front_pengouin — Interface Streamlit

Interface Streamlit multi-pages pour explorer les données des pingouins, faire des prédictions via l'API FastAPI, et visualiser les résultats du training.

## 🎨 Design

L'interface s'inspire du design Plotly avec une palette de couleurs moderne et intuitive. L'icône penguin 🐧 apparaît sur la page d'accueil.

## 📁 Structure

- **`01_Accueil.py`** — Page d'accueil (prédictions single/batch)
- **`pages/02_Analyse_Resultats.py`** — Page d'analyse avec 3 onglets :
  - 📊 **EDA** : 5 graphiques interactifs (histogramme, scatter 2D, scatter 3D, pairplot, distribution)
  - 🤖 **Training** : Comparaison de 3 modèles (Logistic Regression, KNN, Random Forest)
  - 📌 **Statistiques** : Résumé du dataset
- **`.streamlit/config.toml`** — Configuration Streamlit (thème, couleurs)
- **`Dockerfile`** — Image Docker multi-stage pour le déploiement GCP
- **`requirements.txt`** — Dépendances

## 🚀 Lancement Local

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Exécution

```bash
streamlit run 01_Accueil.py
```

L'app s'ouvrira à `http://localhost:8501`.

## 🌐 Déploiement sur GCP (Google Cloud Run)

### Prérequis

- Compte GCP avec Cloud Run activé
- `gcloud` CLI installé
- Docker installé localement

### Configuration

1. Définir les variables d'environnement dans `.env` :

```bash
cp .env.example .env
# Éditer .env avec vos paramètres GCP
```

Remplir :
- `PROJECT_ID` : ID de votre projet GCP
- `LOCATION` : région GCP (ex: `europe-west9`)
- `REPOSITORY` : nom du registre Artifact Registry
- `IMAGE_FRONT` : nom de l'image Docker
- `SERVICE_FRONT` : nom du service Cloud Run

2. Sourcer les variables :

```bash
source ../.env
```

### Déploiement via Makefile

```bash
# Option 1 : Build local puis push
make build_front_gcp
make deploy_front

# Option 2 : Build directement dans GCP
make cloud_build_front
```

### Commandes détaillées

```bash
# Build l'image Docker localement
docker build -t penguin-front -f front_pengouin/Dockerfile .

# Tag pour Artifact Registry
docker tag penguin-front \
  europe-west9-docker.pkg.dev/[PROJECT_ID]/docker-repo/penguin-front:latest

# Push vers Artifact Registry
docker push \
  europe-west9-docker.pkg.dev/[PROJECT_ID]/docker-repo/penguin-front:latest

# Déployer sur Cloud Run
gcloud run deploy penguin-front \
  --image europe-west9-docker.pkg.dev/[PROJECT_ID]/docker-repo/penguin-front:latest \
  --region europe-west9 \
  --platform managed \
  --port 8501 \
  --memory 1Gi \
  --allow-unauthenticated
```

## 📊 Fonctionnalités

### Page 1 — Accueil
- 🎯 Formulaire de prédiction single (appelle `/predict`)
- 📤 Upload CSV pour prédictions batch (appelle `/predict_batch`)
- 🔌 Sélection entre API locale ou distante

### Page 2 — Analyse & Résultats
- **Onglet EDA** :
  - Histogramme de flipper_length coloré par espèce
  - Scatter flipper_length vs body_mass (bubble size = bill_length)
  - Scatter 3D interactif
  - Bill length vs Bill depth
  - Pie chart des espèces
  
- **Onglet Training** :
  - Comparaison de l'accuracy (3 modèles : Logistic Regression, KNN, Random Forest)
  - Bar chart de l'accuracy
  - Matrices de confusion (heatmap)
  - Rapport de classification du meilleur modèle
  
- **Onglet Statistiques** :
  - Métriques du dataset
  - Distribution des espèces
  - Résumé descriptif

## 🎨 Design & Thème

Fichier `.streamlit/config.toml` applique :
- Couleur primaire Plotly blue (`#1f77b4`)
- Thème clair moderne
- Police sans-serif
- Mode developer activé

## 📋 Variables d'environnement (Makefile)

Pour faciliter le déploiement, définissez dans le shell ou un fichier `.env` :

```bash
export PROJECT_ID="your-project-id"
export LOCATION="europe-west9"
export REPOSITORY="docker-repo"
export IMAGE_FRONT="penguin-front"
export SERVICE_FRONT="penguin-front"
```

## 🔗 Liens

- **API locale** : `http://localhost:8000`
- **API distante** : `https://penguin-949276358023.europe-west9.run.app/`
- **Streamlit local** : `http://localhost:8501`

## 📝 Notes

- Les graphiques EDA sont cachés en cache pour optimiser les performances
- L'entraînement des modèles se fait à chaque chargement de la page (avec cache)
- Les fichiers CSV doivent contenir les colonnes : `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`, `species`

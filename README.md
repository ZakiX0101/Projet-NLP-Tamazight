# ⵣ Projet NLP Tamazight → Arabe avec TF-IDF

Ce projet réalise une traduction **Tamazight/Tifinagh → Arabe** à l’aide d’une approche basée sur **TF-IDF** et la **similarité cosinus**.

Le système fonctionne comme une mémoire de traduction : il recherche dans une base de phrases Tamazight la phrase la plus proche de l’entrée utilisateur, puis retourne sa traduction arabe.

---

## Objectif

L’objectif du projet est de proposer une solution NLP légère, rapide et explicable pour la traduction Tamazight/Tifinagh vers Arabe.

Cette approche ne nécessite pas de GPU et peut être exécutée facilement sur un PC local.

---

## Fonctionnalités

- Traduction Tamazight/Tifinagh → Arabe
- Recherche par similarité TF-IDF
- Interface web avec Streamlit
- Interface en ligne de commande
- Affichage du score de similarité
- Affichage des alternatives les plus proches
- Évaluation simple sur un jeu de test

---

## Architecture du projet

```text
Projet-NLP-Tamazight/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   └── processed/
│       ├── train_clean.csv
│       ├── valid_clean.csv
│       └── test_clean.csv
│
├── models/
│   └── tfidf_translation_memory.joblib
│
├── scripts/
│   ├── build_index.py
│   └── evaluate_tfidf.py
│
├── src/
│   ├── config.py
│   ├── preprocessing/
│   │   └── normalization.py
│   ├── retrieval/
│   │   └── tfidf_translator.py
│   └── cli/
│       └── translate.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Données

Les fichiers utilisés doivent être placés dans :

```text
data/processed/
```

Fichiers nécessaires :

```text
train_clean.csv
valid_clean.csv
test_clean.csv
```

Chaque fichier doit contenir au minimum les colonnes suivantes :

```text
tamazight, arabic
```

Le dataset a été nettoyé afin de garder une direction cohérente :

```text
Tamazight/Tifinagh → Arabe
```

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ZakiX0101/Projet-NLP-Tamazight.git
cd Projet-NLP-Tamazight
```

### 2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Sous Linux/macOS :

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Construction de l’index TF-IDF

Avant de lancer l’application, il faut construire l’index TF-IDF :

```bash
python scripts/build_index.py
```

Cette commande génère :

```text
models/tfidf_translation_memory.joblib
```

---

## Utilisation en ligne de commande

```bash
python -m src.cli.translate --text "ⵜⴳⴰ ⵜⴰⵖⴰⵔⴰⵙⵜ ⵜⴰⵔⵎⵉⴷⵉⵜ"
```

Exemple de résultat :

```text
Texte saisi     : ⵜⴳⴰ ⵜⴰⵖⴰⵔⴰⵙⵜ ⵜⴰⵔⵎⵉⴷⵉⵜ
Score           : 1.0
Fiable          : Oui
Traduction      : طريقة خاطئة
Source trouvée  : ⵜⴳⴰ ⵜⴰⵖⴰⵔⴰⵙⵜ ⵜⴰⵔⵎⵉⴷⵉⵜ
```

---

## Lancer l’application web

```bash
streamlit run app/streamlit_app.py
```

Puis ouvrir le lien affiché dans le terminal, généralement :

```text
http://localhost:8501
```

L’interface permet de :

- saisir une phrase en Tamazight/Tifinagh ;
- obtenir la traduction arabe ;
- consulter le score de similarité ;
- afficher les alternatives proposées.

---

## Évaluation

Pour évaluer le système sur `test_clean.csv` :

```bash
python scripts/evaluate_tfidf.py
```

Le script affiche :

- le nombre total d’exemples testés ;
- le taux de traductions fiables ;
- l’exact match rate ;
- le score TF-IDF moyen ;
- quelques exemples de prédictions.

---

## Commandes rapides

```bash
python -m pip install -r requirements.txt
python scripts/build_index.py
python -m src.cli.translate --text "ⴰⵣⵓⵍ"
streamlit run app/streamlit_app.py
```

---

## Technologies utilisées

- Python
- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Similarité cosinus
- Joblib
- Streamlit

---

## Limites

Ce système ne génère pas une traduction totalement nouvelle comme un modèle neuronal.  
Il fonctionne mieux lorsque la phrase saisie est proche d’une phrase existante dans le corpus.

Ses performances dépendent donc fortement de la qualité et de la couverture du dataset.

---

## Perspectives

Améliorations possibles :

- enrichir le corpus Tamazight → Arabe ;
- ajouter une translittération Latin ↔ Tifinagh ;
- améliorer la normalisation du texte ;
- combiner TF-IDF avec un modèle neuronal comme mT5 ou NLLB ;
- déployer l’application sur Streamlit Cloud ou Hugging Face Spaces.

---

## Auteur

**Zakariae BELLIL et Aymane EL AKKIOUI**

Projet académique en NLP  
Thème : Traduction automatique Tamazight/Tifinagh vers Arabe  
Approche : TF-IDF + mémoire de traduction

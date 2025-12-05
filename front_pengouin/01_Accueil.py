import io
import json
import requests
import streamlit as st
import pandas as pd
from typing import Optional

st.set_page_config(
    page_title="🐧 Front Penguin",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "# 🐧 Front Penguin\nInterface de prédiction pour classifier les espèces de pingouins."
    }
)

# Design inspired by Plotly
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        padding: 2rem;
    }
    h1, h2, h3 {
        color: #1f77b4;
        font-weight: 700;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1f77b4 0%, #17becf 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    .stForm {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Default API base (local FastAPI) — user can switch to the provided remote URL
DEFAULT_LOCAL = "http://127.0.0.1:8000"
REMOTE_URL = "https://penguin-949276358023.europe-west9.run.app/"


def load_local_csv(path: str = "data/pingouins.csv") -> Optional[pd.DataFrame]:
    try:
        # Essayer avec pathlib pour trouver le CSV depuis le dossier courant ou parent
        csv_path = Path(path)
        if not csv_path.exists():
            # Si le chemin relatif ne marche pas, essayer depuis le dossier parent (racine du repo)
            csv_path = Path("..") / path
        if not csv_path.exists():
            return None
        return pd.read_csv(str(csv_path))
    except Exception:
        return None


def probe_url(base: str) -> tuple[Optional[int], str]:
    try:
        r = requests.get(base, timeout=5)
        return r.status_code, r.text[:2000]
    except requests.RequestException as exc:
        return None, str(exc)


def post_predict(base: str, payload: dict) -> tuple[Optional[str], Optional[int], str]:
    url = base.rstrip("/") + "/predict"
    try:
        r = requests.post(url, json=payload, timeout=8)
        return url, r.status_code, r.text
    except requests.RequestException as exc:
        return None, None, str(exc)


def post_predict_batch(base: str, file_bytes: bytes, filename: str = "upload.csv") -> tuple[Optional[int], str]:
    url = base.rstrip("/") + "/predict_batch"
    try:
        files = {"pengouins": (filename, io.BytesIO(file_bytes), "text/csv")}
        r = requests.post(url, files=files, timeout=15)
        return r.status_code, r.text
    except requests.RequestException as exc:
        return None, str(exc)


def post_predict_batch(base: str, file_bytes: bytes, filename: str = "upload.csv") -> tuple[Optional[int], str]:
    url = base.rstrip("/") + "/predict_batch"
    try:
        files = {"pengouins": (filename, io.BytesIO(file_bytes), "text/csv")}
        r = requests.post(url, files=files, timeout=15)
        return r.status_code, r.text
    except requests.RequestException as exc:
        return None, str(exc)


def main():
    # Titre principal avec emoji penguin
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        st.markdown("# 🐧")
    with col2:
        st.markdown("# Front Penguin")
    
    st.markdown("""
    ### Prédisez l'espèce de pingouins avec l'IA 🤖
    
    Bienvenue ! Utilisez le menu à gauche pour :
    - 🎯 **Prédire** une espèce de penguin (single ou batch)
    - 📊 **Explorer** les données et résultats du training
    """)

    st.markdown("---")

    # Configuration de l'API dans la sidebar
    st.sidebar.header("⚙️ Configuration API")
    api_choice = st.sidebar.selectbox(
        "Sélectionnez l'API",
        [DEFAULT_LOCAL, REMOTE_URL],
        index=0,
        help="API locale (défaut) ou API distante (GCP)"
    )
    
    # Test de connexion
    if st.sidebar.button("🔍 Tester la connexion"):
        with st.spinner("Vérification..."):
            status, snippet = probe_url(api_choice)
            if status is None:
                st.sidebar.error(f"❌ Erreur: {snippet}")
            else:
                st.sidebar.success(f"✅ OK (HTTP {status})")

    st.markdown("---")

    # Section Prédiction Single
    st.header("🎯 Prédiction — une ligne")
    st.markdown("Remplissez les caractéristiques du penguin pour obtenir une prédiction.")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            bill_length = st.number_input("Bill Length (mm)", value=45.0, min_value=0.0)
            bill_depth = st.number_input("Bill Depth (mm)", value=14.0, min_value=0.0)
        
        with col2:
            flipper = st.number_input("Flipper Length (mm)", value=190.0, min_value=0.0)
            body_mass = st.number_input("Body Mass (g)", value=3700.0, min_value=0.0)
        
        sex = st.selectbox("Sex", ["Male", "Female"])
        
        submit = st.form_submit_button("🚀 Prédire", use_container_width=True)
    
    if submit:
        payload = {
            "bill_length_mm": float(bill_length),
            "bill_depth_mm": float(bill_depth),
            "flipper_length_mm": float(flipper),
            "body_mass_g": float(body_mass),
            "sex": sex,
        }
        
        with st.spinner("Prédiction en cours..."):
            url, code, text = post_predict(api_choice, payload)
        
        if url is None:
            st.error(f"❌ Erreur: {text}")
        else:
            st.success(f"✅ Réponse {code}")
            try:
                result = json.loads(text)
                st.json(result)
            except Exception:
                st.text(text)

    st.markdown("---")

    # Section Prédiction Batch
    st.header("📤 Prédiction par lot")
    st.markdown("Uploader un fichier CSV pour obtenir des prédictions en batch.")
    
    batch_file = st.file_uploader(
        "Fichier CSV",
        type=["csv"],
        key="batch"
    )
    
    if batch_file is not None:
        st.info(f"📄 Fichier: {batch_file.name} ({batch_file.size} bytes)")
        
        if st.button("📨 Envoyer le batch", use_container_width=True):
            file_bytes = batch_file.read()
            
            with st.spinner("Traitement..."):
                code, text = post_predict_batch(api_choice, file_bytes, filename=batch_file.name)
            
            if code is None:
                st.error(f"❌ Erreur: {text}")
            else:
                st.success(f"✅ Réponse {code}")
                try:
                    result = json.loads(text)
                    st.json(result)
                except Exception:
                    st.text(text)

    st.markdown("---")
    
    st.caption("🔗 Consultez la page **'Analyse & Résultats'** pour explorer les données et voir les résultats du training.")


if __name__ == "__main__":
    main()

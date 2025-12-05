import io
import json
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Optional

# Default API base (local FastAPI) — user can switch to the provided remote URL
DEFAULT_LOCAL = "http://127.0.0.1:8000"
REMOTE_URL = "https://penguin-949276358023.europe-west9.run.app/"


def load_local_csv(path: str = "data/pingouins.csv") -> Optional[pd.DataFrame]:
    try:
        return pd.read_csv(path)
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


def show_charts(df: pd.DataFrame):
    st.subheader("Aperçu des données")
    st.dataframe(df.head(10))

    st.subheader("Histogramme — Flipper length")
    fig = px.histogram(df, x="flipper_length_mm", color="species", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Scatter — Flipper length vs Body mass")
    fig2 = px.scatter(df, x="flipper_length_mm", y="body_mass_g", color="species", hover_data=df.columns)
    st.plotly_chart(fig2, use_container_width=True)

    # 3D scatter if bill_length_mm exists
    if {"bill_length_mm", "bill_depth_mm", "body_mass_g"}.issubset(set(df.columns)):
        st.subheader("Scatter 3D (bill_length, bill_depth, body_mass)")
        fig3 = px.scatter_3d(df, x="bill_length_mm", y="bill_depth_mm", z="body_mass_g", color="species")
        st.plotly_chart(fig3, use_container_width=True)


def main():
    st.set_page_config(page_title="Front Penguin", layout="wide")
    st.title("Front Penguin — Interface Streamlit")

    st.sidebar.header("Configuration")
    api_choice = st.sidebar.selectbox("API base", [DEFAULT_LOCAL, REMOTE_URL], index=0)
    st.sidebar.caption("Choisir l'URL de l'API à utiliser pour les prédictions")

    st.header("Données & Visualisations")
    df = load_local_csv()
    if df is None:
        st.warning("Fichier `data/pingouins.csv` introuvable — vous pouvez uploader un CSV ci-dessous.")
        uploaded = st.file_uploader("Uploader un CSV de pingouins (optionnel)", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
    if df is not None:
        show_charts(df)

    st.markdown("---")

    st.header("Prédiction — une ligne")
    st.markdown("Remplissez les champs ci-dessous pour faire une prédiction via l'endpoint `/predict`. Le champ `sex` doit être \"Male\" ou \"Female\".")
    cols = st.columns(5)
    with cols[0]:
        bill_length = st.number_input("bill_length_mm", value=45.0)
    with cols[1]:
        bill_depth = st.number_input("bill_depth_mm", value=14.0)
    with cols[2]:
        flipper = st.number_input("flipper_length_mm", value=190)
    with cols[3]:
        body_mass = st.number_input("body_mass_g", value=3700)
    with cols[4]:
        sex = st.selectbox("sex", ["Male", "Female"])

    if st.button("Prédire (POST /predict)"):
        payload = {
            "bill_length_mm": float(bill_length),
            "bill_depth_mm": float(bill_depth),
            "flipper_length_mm": float(flipper),
            "body_mass_g": float(body_mass),
            "sex": sex,
        }
        url, code, text = post_predict(api_choice, payload)
        if url is None:
            st.error(f"Erreur requête: {text}")
        else:
            st.success(f"Réponse {code} depuis {url}")
            try:
                st.json(json.loads(text))
            except Exception:
                st.text(text)

    st.markdown("---")

    st.header("Prédiction par lot — Upload CSV")
    st.markdown("Uploader un CSV (même format que `data/pingouins.csv`). L'endpoint `/predict_batch` renvoie une liste de prédictions.")
    batch_file = st.file_uploader("Fichier CSV pour prédiction batch", type=["csv"], key="batch")
    if batch_file is not None:
        st.write(f"Fichier reçu: {batch_file.name} — {batch_file.size} bytes")
        if st.button("Envoyer le fichier à /predict_batch"):
            file_bytes = batch_file.read()
            code, text = post_predict_batch(api_choice, file_bytes, filename=batch_file.name)
            if code is None:
                st.error(f"Erreur envoi: {text}")
            else:
                st.success(f"Réponse {code}")
                try:
                    st.json(json.loads(text))
                except Exception:
                    st.text(text)


if __name__ == "__main__":
    main()

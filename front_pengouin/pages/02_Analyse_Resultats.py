import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Analyse & Résultats", layout="wide")

# Design inspired by Plotly
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 {
        color: #1f77b4;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] button {
        color: #1f77b4;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f77b4 0%, #17becf 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Analyse & Résultats")

st.markdown("""
Explorez les données des pingouins et consultez les résultats du training des modèles de machine learning.
""")

st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        csv_path = Path(__file__).parent.parent.parent / "data" / "pingouins.csv"
        if not csv_path.exists():
            csv_path = Path("data") / "pingouins.csv"
        return pd.read_csv(str(csv_path))
    except Exception as e:
        st.error(f"Erreur: {e}")
        return None

df = load_data()

if df is not None:
    # Tabs pour naviguer entre les sections
    tab1, tab2, tab3 = st.tabs(["📊 EDA — Visualisations", "🤖 Training — Résultats", "📌 Statistiques"])
    
    # ===== TAB 1: EDA VISUALIZATIONS =====
    with tab1:
        st.header("Exploration des Données")
        
        # Sub-tabs pour différents graphiques
        eda_tabs = st.tabs(["Histogramme", "Scatter 2D", "Scatter 3D", "Pairplot", "Distribution des espèces"])
        
        with eda_tabs[0]:
            st.subheader("📈 Distribution de Flipper Length par espèce")
            fig1 = px.histogram(
                df, 
                x="flipper_length_mm", 
                color="species", 
                nbins=25,
                title="Histogramme — Flipper Length (mm)",
                labels={"flipper_length_mm": "Flipper Length (mm)", "species": "Espèce"}
            )
            fig1.update_layout(height=500, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True, key='histogram_flipper')
        
        with eda_tabs[1]:
            st.subheader("🔗 Flipper Length vs Body Mass")
            df_clean = df.dropna(subset=["flipper_length_mm", "body_mass_g", "bill_length_mm"])
            fig2 = px.scatter(
                df_clean, 
                x="flipper_length_mm", 
                y="body_mass_g", 
                color="species",
                size="bill_length_mm",
                hover_data={"species": True, "flipper_length_mm": True, "body_mass_g": True},
                title="Scatter — Flipper Length vs Body Mass"
            )
            fig2.update_layout(height=500, hovermode='closest')
            st.plotly_chart(fig2, use_container_width=True, key='scatter_flipper_mass')
        
        with eda_tabs[2]:
            st.subheader("🎯 Scatter 3D — Dimensions du Penguin")
            if {"bill_length_mm", "bill_depth_mm", "body_mass_g"}.issubset(set(df.columns)):
                df_clean_3d = df.dropna(subset=["bill_length_mm", "bill_depth_mm", "body_mass_g"])
                fig3 = px.scatter_3d(
                    df_clean_3d,
                    x="bill_length_mm",
                    y="bill_depth_mm",
                    z="body_mass_g",
                    color="species",
                    title="3D Scatter — Bill Length, Bill Depth, Body Mass"
                )
                fig3.update_layout(height=600)
                st.plotly_chart(fig3, use_container_width=True, key='scatter_3d')
        
        with eda_tabs[3]:
            st.subheader("🔀 Bill Length vs Bill Depth")
            df_clean_bill = df.dropna(subset=["bill_length_mm", "bill_depth_mm", "body_mass_g"])
            fig4 = px.scatter(
                df_clean_bill,
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
                size="body_mass_g",
                title="Scatter — Bill Length vs Bill Depth (taille = body mass)"
            )
            fig4.update_layout(height=500)
            st.plotly_chart(fig4, use_container_width=True, key='scatter_bill')
        
        with eda_tabs[4]:
            st.subheader("🥧 Distribution des espèces")
            species_counts = df["species"].value_counts()
            fig5 = px.pie(
                values=species_counts.values,
                names=species_counts.index,
                title="Répartition des espèces",
                hole=0.3
            )
            fig5.update_layout(height=500)
            st.plotly_chart(fig5, use_container_width=True, key='pie_species')
    
    # ===== TAB 2: MODEL TRAINING & RESULTS =====
    with tab2:
        st.header("Résultats du Training")
        
        st.markdown("Training de 3 modèles différents pour la classification des espèces...")
        
        with st.spinner("Entraînement des modèles..."):
            # Prepare data
            df_model = df.dropna()
            X = df_model.drop(columns=["species"])
            y = df_model["species"]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Preprocessing
            numeric_cols = X_train.select_dtypes(include=[np.number]).columns
            categorical_cols = X_train.select_dtypes(include=['object']).columns
            
            # Numeric pipeline
            numeric_transformer = StandardScaler()
            numeric_transformer.fit(X_train[numeric_cols])
            X_train_num = numeric_transformer.transform(X_train[numeric_cols])
            X_test_num = numeric_transformer.transform(X_test[numeric_cols])
            
            # Categorical pipeline
            categorical_transformer = OneHotEncoder(sparse_output=False, drop="first")
            categorical_transformer.fit(X_train[categorical_cols])
            X_train_cat = categorical_transformer.transform(X_train[categorical_cols])
            X_test_cat = categorical_transformer.transform(X_test[categorical_cols])
            
            # Combine
            X_train_final = np.concatenate([X_train_num, X_train_cat], axis=1)
            X_test_final = np.concatenate([X_test_num, X_test_cat], axis=1)
            
            # Train models
            models = {
                "Logistic Regression": LogisticRegression(max_iter=200),
                "K-Nearest Neighbors (k=3)": KNeighborsClassifier(n_neighbors=3),
                "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
            }
            
            results = {}
            for name, model in models.items():
                model.fit(X_train_final, y_train)
                y_pred = model.predict(X_test_final)
                accuracy = accuracy_score(y_test, y_pred)
                results[name] = {
                    "model": model,
                    "y_pred": y_pred,
                    "accuracy": accuracy
                }
        
        # Display accuracy comparison
        st.subheader("📊 Comparaison de la Précision (Accuracy)")
        
        accuracies = {name: res["accuracy"] for name, res in results.items()}
        
        col1, col2, col3 = st.columns(3)
        for i, (name, acc) in enumerate(accuracies.items()):
            with [col1, col2, col3][i]:
                st.metric(label=name, value=f"{acc:.2%}")
        
        # Accuracy bar chart
        fig_acc = px.bar(
            x=list(accuracies.keys()),
            y=list(accuracies.values()),
            title="Comparaison de l'Accuracy",
            labels={"x": "Modèle", "y": "Accuracy"},
            color=list(accuracies.values()),
            color_continuous_scale="Blues"
        )
        fig_acc.update_layout(height=400, showlegend=False, hovermode='x unified')
        st.plotly_chart(fig_acc, use_container_width=True, key='accuracy_bar')
        
        st.markdown("---")
        
        # Confusion matrices for each model
        st.subheader("🎲 Matrices de Confusion")
        
        cols = st.columns(len(results))
        for i, (name, res) in enumerate(results.items()):
            with cols[i]:
                st.markdown(f"**{name}**")
                cm = confusion_matrix(y_test, res["y_pred"])
                
                fig_cm = go.Figure(data=go.Heatmap(
                    z=cm,
                    x=np.unique(y),
                    y=np.unique(y),
                    colorscale="Blues",
                    text=cm,
                    texttemplate="%{text}",
                    textfont={"size": 12}
                ))
                fig_cm.update_layout(
                    title=f"Confusion Matrix — {name}",
                    xaxis_title="Prédiction",
                    yaxis_title="Réel",
                    height=400
                )
                st.plotly_chart(fig_cm, use_container_width=True, key=f'confusion_{i}')
        
        st.markdown("---")
        
        # Classification report for best model
        st.subheader("📋 Rapport de Classification — Meilleur Modèle")
        
        best_model_name = max(results.items(), key=lambda x: x[1]["accuracy"])[0]
        best_result = results[best_model_name]
        
        st.markdown(f"**Meilleur modèle: {best_model_name}** (Accuracy: {best_result['accuracy']:.2%})")
        
        report_dict = classification_report(y_test, best_result["y_pred"], output_dict=True)
        report_df = pd.DataFrame(report_dict).transpose()
        st.dataframe(report_df, use_container_width=True)
    
    # ===== TAB 3: STATISTICS =====
    with tab3:
        st.header("Statistiques du Dataset")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total d'observations", len(df))
        with col2:
            st.metric("Nombre de features", len(df.columns))
        with col3:
            st.metric("Nombre d'espèces", df['species'].nunique())
        with col4:
            st.metric("Valeurs manquantes", df.isna().sum().sum())
        
        st.markdown("---")
        
        st.subheader("🥧 Distribution des espèces")
        species_counts = df["species"].value_counts()
        fig_species = px.pie(
            values=species_counts.values,
            names=species_counts.index,
            title="Répartition des espèces",
            hole=0.3
        )
        fig_species.update_layout(height=500)
        st.plotly_chart(fig_species, use_container_width=True, key='pie_species_stats')
        
        st.markdown("---")
        
        st.subheader("📋 Informations du Dataset")
        st.dataframe(df.describe(), use_container_width=True)

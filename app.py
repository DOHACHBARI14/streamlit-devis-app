import streamlit as st
import pandas as pd
from io import BytesIO

def calculate_prix_vente(df, marge, mo, mod, cf, cp, fa):
    df['Prix Vente'] = marge * (((df['PA_HT'] * (1 + 0) + fa) * cf) + (df['MO_HEURE_EQUIPE'] * mo * mod)) / (1 - cp)
    return df

def generate_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Devis Automatique', index=False)
    output.seek(0)
    return output

st.title("📝 Générateur de Devis Automatique")

uploaded_file = st.file_uploader("Téléchargez votre fichier Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=1)
    df = df.rename(columns={'Unnamed: 1': 'DESIGNATION', 'Unnamed: 5': 'UNITE', 'Unnamed: 6': 'QTE', 'Unnamed: 7': 'PA_HT', 'Unnamed: 9': 'MO_HEURE_EQUIPE'})
    df = df[['DESIGNATION', 'UNITE', 'QTE', 'PA_HT', 'MO_HEURE_EQUIPE']].dropna()

    # Paramètres personnalisables
    marge = st.number_input("Marge", value=1.3)
    mo = st.number_input("Main d'œuvre (équipe de 2)", value=73.75)
    mod = st.number_input("Main d'œuvre déplacement", value=1.0)
    cf = st.number_input("Charges financières appro", value=1.2075)
    cp = st.number_input("Compte prorata", value=0.02)
    fa = st.number_input("Frais annexes", value=1.0)
    
    if st.button("📊 Générer le devis"):
        df = calculate_prix_vente(df, marge, mo, mod, cf, cp, fa)
        excel_file = generate_excel(df)
        st.download_button("📥 Télécharger le devis", excel_file, file_name="Devis_Automatique.xlsx")

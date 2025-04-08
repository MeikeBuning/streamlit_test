import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt  # Alleen nog gebruikt voor fallback instellingen

# CSV inladen
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

# Datumkolom naar datetime
df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'])

# Maandkolom genereren
df['maand'] = df['aankoopdatum'].dt.to_period('M').dt.to_timestamp()

# Selectie van maand
maanden = sorted(df['maand'].dt.strftime('%Y-%m').unique())
gekozen_maand_str = st.selectbox("📅 Kies een eindmaand", maanden)
gekozen_maand = pd.to_datetime(gekozen_maand_str)
start_maand = gekozen_maand - pd.DateOffset(months=12)
start_ytd = pd.Timestamp(year=gekozen_maand.year, month=1, day=1)

# Filters
df_13mnd = df[(df['maand'] >= start_maand) & (df['maand'] <= gekozen_maand)]
df_ytd = df[(df['aankoopdatum'] >= start_ytd) & (df['aankoopdatum'] <= gekozen_maand)]
df_geselecteerde_maand = df[df['maand'] == gekozen_maand]

# KPI-cijfers
omzet_maand = df_geselecteerde_maand['totaal_bedrag'].sum()
omzet_ytd = df_ytd['totaal_bedrag'].sum()

# === Streamlit layout ===
st.title("💼 Omzet Dashboard")

# KPI's
col1, col2 = st.columns(2)
col1.metric(f"📆 Omzet in {gekozen_maand.strftime('%B %Y')}", f"€ {omzet_maand:,.2f}")
col2.metric(f"📈 Omzet YTD tot {gekozen_maand.strftime('%d %B %Y')}", f"€ {omzet_ytd:,.2f}")

# === Plotly grafiek 1: omzet per maand ===
maand_omzet = df_13mnd.groupby('maand')['totaal_bedrag'].sum().reset_index()
fig1 = px.bar(
    maand_omzet,
    x='maand',
    y='totaal_bedrag',
    title="📊 Omzet per Maand (Laatste 13 maanden)",
    labels={'maand': 'Maand', 'totaal_bedrag': 'Omzet (€)'},
    text_auto='.2s'
)
fig1.update_layout(xaxis_tickformat='%Y-%m')
st.plotly_chart(fig1, use_container_width=True)

# === Plotly grafiek 2: omzet per merk in geselecteerde maand ===
merk_omzet = df_geselecteerde_maand.groupby('merk')['totaal_bedrag'].sum().reset_index()
merk_omzet = merk_omzet.sort_values('totaal_bedrag', ascending=True)

fig2 = px.bar(
    merk_omzet,
    x='totaal_bedrag',
    y='merk',
    orientation='h',
    title=f"🥿 Omzet per Merk – {gekozen_maand.strftime('%B %Y')}",
    labels={'totaal_bedrag': 'Omzet (€)', 'merk': 'Merk'},
    text_auto='.2s'
)
st.plotly_chart(fig2, use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Layout fix voor plotly/matplotlib
plt.rcParams.update({'figure.autolayout': True})

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

# Filter voor 13 maanden en YTD
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

# === Grafiek 1: Omzet per maand (13 maanden) ===
maand_omzet = df_13mnd.groupby('maand')['totaal_bedrag'].sum().reset_index()
maand_omzet = maand_omzet.sort_values('maand')

fig1, ax1 = plt.subplots()
ax1.bar(maand_omzet['maand'].dt.strftime('%Y-%m'), maand_omzet['totaal_bedrag'])
ax1.set_xlabel("Maand")
ax1.set_ylabel("Omzet (€)")
ax1.set_title("📊 Omzet per Maand (Laatste 13 maanden)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# === Grafiek 2: Omzet per merk in geselecteerde maand ===
merk_omzet = df_geselecteerde_maand.groupby('merk')['totaal_bedrag'].sum().reset_index()
merk_omzet = merk_omzet.sort_values('totaal_bedrag')

fig2, ax2 = plt.subplots()
bars = ax2.barh(merk_omzet['merk'], merk_omzet['totaal_bedrag'])

# Data labels toevoegen
for bar in bars:
    width = bar.get_width()
    ax2.text(width + 5, bar.get_y() + bar.get_height() / 2,
             f"€ {width:,.2f}", va='center', fontsize=9)

ax2.set_xlabel("Omzet (€)")
ax2.set_ylabel("Merk")
ax2.set_title(f"🥿 Omzet per Merk – {gekozen_maand.strftime('%B %Y')}")
st.pyplot(fig2)


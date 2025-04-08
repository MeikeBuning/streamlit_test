import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV inladen
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

# Datumkolom omzetten naar datetime
df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'])

# Maand-jaar kolom toevoegen
df['maand'] = df['aankoopdatum'].dt.to_period('M').dt.to_timestamp()

# Unieke maanden voor de selectbox (gesorteerd)
maanden = sorted(df['maand'].dt.strftime('%Y-%m').unique())

# Maandfilter bovenaan
gekozen_maand_str = st.selectbox("📅 Kies een eindmaand", maanden)

# Gekozen maand als datetime
gekozen_maand = pd.to_datetime(gekozen_maand_str)

# Startmaand = 12 maanden eerder (dus 13 maanden in totaal inclusief gekozen maand)
start_maand = gekozen_maand - pd.DateOffset(months=12)

# Filteren op de 13-maandsperiode
df_filtered = df[(df['maand'] >= start_maand) & (df['maand'] <= gekozen_maand)]

# Groeperen op maand en optellen van totaal_bedrag
maand_omzet = df_filtered.groupby('maand')['totaal_bedrag'].sum().reset_index()
maand_omzet = maand_omzet.sort_values('maand')

# Plot
st.title(f"Omzet per Maand – {start_maand.strftime('%b %Y')} t/m {gekozen_maand.strftime('%b %Y')}")
fig, ax = plt.subplots()
ax.bar(maand_omzet['maand'].dt.strftime('%Y-%m'), maand_omzet['totaal_bedrag'])
ax.set_xlabel("Maand")
ax.set_ylabel("Omzet (€)")
ax.set_title("Omzet laatste 13 maanden")
plt.xticks(rotation=45)
st.pyplot(fig)

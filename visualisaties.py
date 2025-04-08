import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV inladen
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

# Datumkolom omzetten naar datetime
df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'])

# Maand-jaar kolom toevoegen
df['maand'] = df['aankoopdatum'].dt.to_period('M').astype(str)

# Groeperen op maand en optellen van totaal_bedrag
maand_omzet = df.groupby('maand')['totaal_bedrag'].sum().reset_index()

# Sorteren op datum (voor correcte volgorde in de grafiek)
maand_omzet['maand'] = pd.to_datetime(maand_omzet['maand'])
maand_omzet = maand_omzet.sort_values('maand')

# Plotten
st.title("Omzet per Maand")
fig, ax = plt.subplots()
ax.bar(maand_omzet['maand'].dt.strftime('%Y-%m'), maand_omzet['totaal_bedrag'])
ax.set_xlabel("Maand")
ax.set_ylabel("Omzet (€)")
ax.set_title("Omzet per Maand")
plt.xticks(rotation=45)
st.pyplot(fig)

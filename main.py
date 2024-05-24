import streamlit as st
import pandas as pd

# Fonction pour lire le fichier CSV et le charger en DataFrame
@st.cache_data
def load_data():
    try:
        return pd.read_csv('shoplist.csv', sep=';')
    except FileNotFoundError:
        return pd.DataFrame(columns=["product", "brand", "quantity", "by", "where", "check"])

# Fonction pour sauvegarder le DataFrame dans un fichier CSV
def save_data(df):
    df.to_csv('shoplist.csv', sep=';', index=False)

# Chargement des données
df = load_data()

# Premier onglet: Consultation et ajout de produits
tab1, tab2 = st.tabs(["Liste des produits", "Au magasin"])

with tab1:
    st.header("Liste des produits à acheter")
    
    st.subheader("Ajouter un nouveau produit")
    product = st.text_input("Produit")
    brand = st.text_input("Marque")
    quantity = st.text_input("Quantité")
    by = st.text_input("Par")
    where = st.text_input("Où")
    
    if st.button("Ajouter produit"):
        if product and brand and quantity and by and where:
            new_product = {"product": product, "brand": brand, "quantity": quantity, "by": by, "where": where, "check": False}
            new_df = pd.DataFrame([new_product])
            df = pd.concat([df, new_df], ignore_index=True)
            save_data(df)
            st.success("Produit ajouté avec succès!")
        else:
            st.error("Tous les champs doivent être remplis pour ajouter un produit.")
    
    st.subheader("Liste actuelle des produits")
    st.dataframe(df)

with tab2:
    st.header("Liste des produits à acheter en magasin")

    # Filtrer les produits non cochés
    df_unchecked = df[df['check'] == False]
    
    # Afficher les produits avec cases à cocher et sections réductibles
    checked_items = []
    for index, row in df_unchecked.iterrows():
        if st.checkbox(f"{row['product']}", key=row['product']):
            checked_items.append(index)
        with st.expander("Détails", expanded=False):
            st.write(f"Marque: {row['brand']}")
            st.write(f"Quantité: {row['quantity']}")
            st.write(f"Par: {row['by']}")
            st.write(f"Où: {row['where']}")

    if st.button("Confirmer"):
        df.loc[checked_items, 'check'] = True
        save_data(df)
        st.success("Liste mise à jour avec succès!")
        
        # Mettre à jour la liste des produits à acheter
        df_unchecked = df[df['check'] == False]

    # Afficher la liste filtrée
    st.subheader("Produits restants à acheter")
    st.dataframe(df_unchecked)

# Recharger les données après modification
df = load_data()

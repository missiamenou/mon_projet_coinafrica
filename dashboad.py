import pandas as pd
import numpy as np

def cap_outliers_iqr(df, column):
    """Caps outliers in a DataFrame column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])

    return df

def traiter_donnees_villas_(data):
    # Charger en DataFrame si ce n'est pas déjà fait
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # On sélectionne uniquement les colonnes utiles
    df = data[["Nombre_de_pieces", "Nombre_salles_bain", "Superficie", "Adresse"]].copy()

    # Nettoyage de la colonne 'Superficie'
    df['Superficie'] = df['Superficie'].astype(str).str.replace(' m2', '', regex=False)
    df['Superficie'] = pd.to_numeric(df['Superficie'], errors='coerce')

    # Conversion en numérique
    df['Nombre_de_pieces'] = pd.to_numeric(df['Nombre_de_pieces'], errors='coerce')
    df['Nombre_salles_bain'] = pd.to_numeric(df['Nombre_salles_bain'], errors='coerce')

    # Renommer les colonnes
    df.rename(columns={
        'Nombre_de_pieces': 'Pieces',
        'Nombre_salles_bain': 'Salles_bain'
    }, inplace=True)

    # Capping des outliers
    numerical_cols = ['Pieces', 'Salles_bain', 'Superficie']
    for col in numerical_cols:
        df = cap_outliers_iqr(df, col)

    # Remplissage des valeurs manquantes
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())
    # Réinitialisation des index
    return df.reset_index(drop=True)


def traiter_donnees_terrains_(data):
    # S'assurer que c'est bien un DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Garder uniquement les colonnes utiles
    df = data[["Superficie", "Prix", "Adresse", "Lien_image-href"]].copy()

    # Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # Nettoyage des colonnes numériques
    df["Prix"] = pd.to_numeric(
        df["Prix"].astype(str).str.replace(" CFA", "", regex=False).str.replace(" ", ""),
        errors='coerce'
    )
    # Renommer les colonnes
    df.rename(columns={
        'Lien_image-href': 'Lien_image	',
    }, inplace=True)

    df["Superficie"] = pd.to_numeric(
        df["Superficie"].astype(str).str.replace(" m2", "", regex=False).str.replace(" ", ""),
        errors='coerce'
    )

    # Capping des outliers
    for col in ['Superficie', 'Prix']:
        df = cap_outliers_iqr(df, col)

    # Remplacer les valeurs manquantes par la médiane
    df["Superficie"].fillna(df["Superficie"].median(), inplace=True)
    df["Prix"].fillna(df["Prix"].median(), inplace=True)

    return df.reset_index(drop=True)

def traiter_donnees_appartements_(data):
    # Assurer que c’est bien un DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Sélection des colonnes pertinentes
    df = data[["Nombre_pieces", "Nombre_salles_bain", "Superficie", "Adresse"]].copy()

    # Suppression des doublons
    df.drop_duplicates(inplace=True)

    # Nettoyage des colonnes
    df["Superficie"] = df["Superficie"].astype(str).str.replace(" m2", "", regex=False)
    df["Superficie"] = pd.to_numeric(df["Superficie"], errors="coerce")

    df["Nombre_salles_bain"] = df["Nombre_salles_bain"].astype(str).str.replace(" m2", "", regex=False)
    df["Nombre_salles_bain"] = pd.to_numeric(df["Nombre_salles_bain"], errors="coerce")

    df["Nombre_pieces"] = pd.to_numeric(df["Nombre_pieces"], errors="coerce")

    # Renommer les colonnes
    df = df.rename(columns={
        "Nombre_pieces": "Pieces",
        "Nombre_salles_bain": "Nb_Salles_bain"
    })

    # Traitement des outliers
    numerical_cols = ["Pieces", "Nb_Salles_bain", "Superficie"]
    for col in numerical_cols:
        df = cap_outliers_iqr(df, col)

    # Remplissage des valeurs manquantes
    for col in numerical_cols:
        df[col].fillna(df[col].median(), inplace=True)

    if df["Adresse"].isnull().sum() > 0:
        df["Adresse"].fillna(df["Adresse"].mode()[0], inplace=True)

    return df.reset_index(drop=True)
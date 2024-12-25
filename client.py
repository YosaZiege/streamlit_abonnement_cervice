import streamlit as st
import psycopg2


st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.3s;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }

    .stButton>button:active {
        background-color: #367636;
        transform: scale(1.02);
    }

    .error-message {
        color: red; // it changes the color of Error Message
        display:none;
        position:absolute;
        opacity:0.85;
        font-size: 24px;  // it changes the font size of Error Message
        z-index:5;
        border-radu
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour insérer l'utilisateur dans la base de données
def register_user(username, email, password, phone_number):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            dbname="streamlitdatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Insérer les données d'utilisateur
        query = """
        INSERT INTO users (name, email, password, phone_number)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, password, phone_number))
        conn.commit()

        cursor.close()
        conn.close()
        return "Inscription réussie !"
    except Exception as e:
        return f"Erreur : {e}"

# Interface utilisateur
st.header("Bienvenue sur notre plateforme")
st.subheader("Veuillez remplir les informations suivantes")
st.markdown("<h3 style='color:blue;'>Formulaire d'inscription</h3>", unsafe_allow_html=True)

# Champs d'inscription
username = st.text_input("Nom d'utilisateur")
email = st.text_input("Adresse e-mail")
password = st.text_input("Mot de passe", type="password")
confirm_password = st.text_input("Confirmez le mot de passe", type="password")
phone_number = st.text_input("Numéro de téléphone")  # Nouveau champ ajouté

# Bouton pour s'inscrire
if st.button("S'inscrire"):
    if password != confirm_password:
        st.markdown('<div class="error-message">Les mots de passe ne correspondent pas !</div>', unsafe_allow_html=True)
    elif not username or not email or not password or not phone_number:
        st.markdown('<div class="error-message">Veuillez remplir tous les champs.</div>', unsafe_allow_html=True)
    else:
        result = register_user(username, email, password, phone_number)
        st.markdown(f'<div class="success-message">{result}</div>', unsafe_allow_html=True)



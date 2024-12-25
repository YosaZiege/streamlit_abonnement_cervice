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
        color: red; 
        opacity:0.85;
        font-size: 24px; 
    }


    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .form-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    .form-container input {
        margin-bottom: 10px;
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
st.subheader("Veuillez remplir les informations suivantes")
st.markdown("<h3 style='color:black;'>Formulaire d'inscription</h3>", unsafe_allow_html=True)

# Champs d'inscription
st.markdown('<div class="form-container">', unsafe_allow_html=True)
username = st.text_input("Nom d'utilisateur")
email = st.text_input("Adresse e-mail")
password = st.text_input("Mot de passe", type="password")
confirm_password = st.text_input("Confirmez le mot de passe", type="password")
phone_number = st.text_input("Numéro de téléphone")  # Nouveau champ ajouté
st.markdown('</div>', unsafe_allow_html=True)

# Bouton pour s'inscrire
if st.button("S'inscrire"):
    if password != confirm_password:
        st.markdown('<div class="error-message">Les mots de passe ne correspondent pas !</div>', unsafe_allow_html=True)
    elif not username or not email or not password or not phone_number:
        st.markdown('<div class="error-message">Veuillez remplir tous les champs.</div>', unsafe_allow_html=True)
    else:
        result = register_user(username, email, password, phone_number)
        st.markdown(f'<div class="success-message">{result}</div>', unsafe_allow_html=True)




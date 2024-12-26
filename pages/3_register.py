import time
import streamlit as st
import psycopg2
from psycopg2 import errors 
from streamlit_option_menu import option_menu # Importer les erreurs spécifiques de psycopg2
# Styles personnalisés
st.set_page_config(initial_sidebar_state="collapsed", page_title="Ma Page", page_icon=":guardsman:")

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
        opacity: 0.85;
        font-size: 18px; 
        font-weight: bold;
    }

    .error-duplicate-email {
        color: #d9534f; /* Couleur personnalisée pour l'email dupliqué */
        font-size: 18px;
        font-weight: bold;
        opacity: 0.9;
    }

    .success-message {
        color: green; 
        opacity: 0.85;
        font-size: 18px; 
        font-weight: bold;
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
    except errors.UniqueViolation:  # Erreur spécifique pour contrainte d'unicité
        return "duplicate_email"
    except Exception as e:
        return f"Erreur : {e}"

# Initialiser les champs avec session_state
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "confirm_password" not in st.session_state:
    st.session_state.confirm_password = ""
if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""

# Interface utilisateur
st.subheader("Veuillez remplir les informations suivantes")
st.markdown("<h3 style='color:black;'>Formulaire d'inscription</h3>", unsafe_allow_html=True)

# Champs d'inscription avec formulaire
with st.form("my_form"):
    st.session_state.username = st.text_input("Nom d'utilisateur", value=st.session_state.username)
    st.session_state.email = st.text_input("Adresse e-mail", value=st.session_state.email)
    st.session_state.password = st.text_input("Mot de passe", type="password", value=st.session_state.password)
    st.session_state.confirm_password = st.text_input("Confirmez le mot de passe", type="password", value=st.session_state.confirm_password)
    st.session_state.phone_number = st.text_input("Numéro de téléphone", value=st.session_state.phone_number)

    # Bouton pour soumettre le formulaire
    submit = st.form_submit_button("S'inscrire")
    
# Logique après soumission
   
if submit:
    if st.session_state.password != st.session_state.confirm_password:
        st.markdown('<div class="error-message">Les mots de passe ne correspondent pas !</div>', unsafe_allow_html=True)
    elif not st.session_state.username or not st.session_state.email or not st.session_state.password or not st.session_state.phone_number:
        st.markdown('<div class="error-message">Veuillez remplir tous les champs.</div>', unsafe_allow_html=True)
    else:
        result = register_user(st.session_state.username, st.session_state.email, st.session_state.password, st.session_state.phone_number)
        if result == "duplicate_email":
            st.markdown('<div class="error-duplicate-email">Cet email est déjà utilisé.</div>', unsafe_allow_html=True)
        elif "Inscription réussie" in result:
            # Réinitialiser les champs après succès
            st.session_state.username = ""
            st.session_state.email = ""
            st.session_state.password = ""
            st.session_state.confirm_password = ""
            st.session_state.phone_number = ""
            st.markdown(f'<div class="success-message">{result}</div>', unsafe_allow_html=True)
            time.sleep(1)
            st.switch_page("pages/2_login.py")
        else:
            st.markdown(f'<div class="error-message">{result}</div>', unsafe_allow_html=True)
if st.button("vous etes deja inscrit ?", key="register_button", help="vous etes deja inscrit"):
    st.switch_page("pages/2_login.py")
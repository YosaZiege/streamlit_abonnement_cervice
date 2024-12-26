import streamlit as st
import psycopg2
from psycopg2 import sql
import time

st.set_page_config(initial_sidebar_state="collapsed", page_title="Ma Page", page_icon=":guardsman:")

# Connexion à la base de données PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="streamlitdatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"                      # Port par défaut de PostgreSQL
        )
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour vérifier les identifiants
def verify_user(email, password):
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()

    # Requête pour vérifier si l'utilisateur et le mot de passe existent
    query = sql.SQL("SELECT * FROM users WHERE email = %s AND password = %s")
    cursor.execute(query, (email, password))

    # Si l'utilisateur existe, on retourne True
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user is not None


st.title("Login Page")

    # Demander à l'utilisateur son nom d'utilisateur et son mot de passe

with st.form("my_form"):
    username = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    submit = st.form_submit_button("Se connecter")

    # Vérifier si l'utilisateur a entré des informations
if submit:
    if username and password:
        if verify_user(username, password):
            if username == "admin@gmail.com" and password == "root" :
                st.switch_page("pages/6_admin.py")
            else :
                st.success(f"Connexion réussie ! Bienvenue, {username}!")
                time.sleep(1)
                    # Redirection vers une autre page après la connexion
                st.session_state['login_in'] = True
                st.session_state['email_user'] = username
                st.switch_page("1_app.py")
                # Par exemple : st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    else:
        st.error("Veuillez entrer votre nom d'utilisateur et votre mot de passe.")
if st.button("Pas encore inscrit ? Inscrivez-vous ici", key="register_button", help="Cliquez pour vous inscrire"):
    st.switch_page("pages/3_register.py")
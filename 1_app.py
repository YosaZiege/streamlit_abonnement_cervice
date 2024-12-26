import streamlit as st
from streamlit_option_menu import option_menu
import time
import psycopg2
from psycopg2 import sql

# Style personnalisé pour le menu
if 'login_in' not in st.session_state:
    st.session_state['login_in'] = False

st.set_page_config(initial_sidebar_state="collapsed", page_title="Ma Page", page_icon=":guardsman:")

styles = {
    "container": {"background-color": "#f8f9fa", "padding": "10px", "border-radius": "8px", "font-size": "10px"},
    "icon": {"color": "#007bff", "font-size": "18px"},
    "nav-link": {"color": "#495057", "font-size": "15px", "text-align": "center", "border-radius": "4px", "padding": "8px"},
    "nav-link-selected": {"background-color": "#007bff", "color": "white", "font-weight": "bold"},
}

menu_options = ["Home", "About", "Contact"]
lsite_icons = ["house", "question-circle", "envelope"]

if not st.session_state['login_in']:  # Afficher "Login" uniquement si l'utilisateur n'est pas connecté
    menu_options.append("Login")
    lsite_icons.append('pen')
else:
    menu_options.append("Déconnexion")
    lsite_icons.append("sign-out")

# Utilisation de la barre de navigation avec style
selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=lsite_icons,  # Ajout des icônes pour toutes les options
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=styles
)

# Connexion à la base de données PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="streamlitdatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"  # Port par défaut de PostgreSQL
        )
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour récupérer les données des cartes depuis la base de données
def get_data_for_cards():
    conn = connect_db()
    if conn is None:
        return []

    cursor = conn.cursor()

    # Exemple de requête pour récupérer les données des cartes
    query = sql.SQL("""
        SELECT id, name, price, internet_limit, call_minutes, social_networks, international_minutes, inwi_calls_unlimited
        FROM subscriptions
    """)
    cursor.execute(query)

    # Récupérer les résultats
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return data

# Logique de la page en fonction de la sélection
if selected == "Home":
    if st.session_state['login_in']:
        st.title("Welcome to Home Page")
        st.write("Voici les informations sélectionnées depuis la base de données :")

        # Récupérer les données des cartes depuis la base de données
        cards_data = get_data_for_cards()

        # Afficher les cartes cliquables
        for card in cards_data:
            card_id, card_name, card_price, internet_limit, call_minutes, social_networks, international_minutes, inwi_calls_unlimited = card
            with st.expander(card_name):  # Utiliser un expander pour chaque carte
                # Appliquer des couleurs aux informations
                st.markdown(f"<h3 style='color: black; font-size: 15px; font-weight: bold;'>Price: <span style='color: #F59E0B;'>{card_price}€</span></h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black; font-size: 15px; font-weight: bold;'>Internet Limit:<span style='font-weight: 600;'> {internet_limit}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black; font-size: 15px; font-weight: bold;'>Call Minutes:<span style='color: red;'> {call_minutes}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black; font-size: 15px; font-weight: bold;'>Social Networks:<span style='font-weight: 600;'> {social_networks}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black; font-size: 15px; font-weight: bold;'>International Minutes:<span style='font-weight: 600;'> {international_minutes}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: black; font-size: 15px; font-weight: bold;'>Inwi Calls Unlimited:<span style='font-weight: 600;'> {inwi_calls_unlimited}</span></p>", unsafe_allow_html=True)

                if st.button(f"Subscribe {card_name}", key=card_id):
                    # Action lors du clic sur une carte
                    st.session_state['id_choosen'] = card_id
                    st.session_state['card_price'] = card_price
                    time.sleep(0.5)
                    st.switch_page("pages/4_abonnement.py")
    else:
        svg_content = """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M87.9547 69.2084C87.9547 69.2084 120.114 93.6121 169.004 47.9812C212.423 7.45662 247.875 71.3952 248.124 102.014C248.446 141.678 204.704 173.414 225.931 199.466C247.159 225.518 183.835 268.538 149.706 231.307C107.252 184.993 95.7505 222.623 71.5519 222.623C54.1842 222.623 18.5265 179.469 42.6058 147.363C62.8681 120.347 51.8178 111.38 46.4651 102.014C38.7462 88.5059 57.0788 51.8407 87.9547 69.2084Z" fill="#DEE9FF"/>
        <path d="M139.987 124.697V215.258L69.6744 184.887L70.0098 94.6547L139.987 124.697Z" fill="#418DF9"/>
        <path d="M139.988 124.751V215.312L209.958 185.991V94.9438L139.988 124.751Z" fill="#A2BDFF"/>
        <path d="M139.987 124.697L210.299 95.247L140.539 64.3242L69.6744 94.5108L139.987 124.697Z" fill="#699CFF"/>
        <path d="M96.1796 83.2202L166.224 113.708L166.86 135.925L186.458 127.839L185.865 105.481L113.749 75.7362L96.1796 83.2202Z" fill="#418DF9"/>
        <path d="M162.235 157.243C163.345 157.243 164.245 155.6 164.245 153.574C164.245 151.548 163.345 149.905 162.235 149.905C161.125 149.905 160.225 151.548 160.225 153.574C160.225 155.6 161.125 157.243 162.235 157.243Z" fill="white"/>
        <path d="M194.618 144.049C195.728 144.049 196.628 142.407 196.628 140.381C196.628 138.354 195.728 136.712 194.618 136.712C193.508 136.712 192.608 138.354 192.608 140.381C192.608 142.407 193.508 144.049 194.618 144.049Z" fill="white"/>
        <path d="M173.883 176.612L172.578 176.105C175.47 168.659 179.096 164.558 183.357 163.914C187.433 163.298 190.866 166.106 192.111 167.676L191.014 168.546C190.153 167.46 187.136 164.759 183.566 165.298C179.89 165.854 176.542 169.766 173.883 176.612Z" fill="white"/>
        </svg>
        </div>
        """
        st.markdown(svg_content, unsafe_allow_html=True)

elif selected == "About":
    st.title("About Page")
    st.write("Cette page vous en dira plus sur le projet.")

elif selected == "Login":
    if st.session_state['login_in']:
        st.title("Bienvenue")
        st.write("Vous êtes déjà connecté.")
    else:
        st.switch_page("pages/2_login.py")

elif selected == "Déconnexion":  # Si l'utilisateur souhaite se déconnecter
    st.session_state['login_in'] = False  # Réinitialiser l'état de connexion
    st.success("Vous avez été déconnecté avec succès.")
    time.sleep(1)
    st.switch_page("1_app.py")

else:
    st.title("Contact Page")
    st.switch_page("pages/5_contact.py")

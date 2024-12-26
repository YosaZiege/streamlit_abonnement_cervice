import streamlit as st
import psycopg2
from psycopg2 import sql
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

st.set_page_config(initial_sidebar_state="collapsed", page_title="Subscription Page", page_icon=":guardsman:")

# Connexion à la base de données PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="streamlitdatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour envoyer un e-mail
def send_email(receiver_email, subject, body):
    sender_email = "omarkhabou063@gmail.com"  # Remplacez par votre adresse e-mail
    password = "wgqy oedl uuek jykt"  # Remplacez par votre mot de passe d'application ou SMTP

    try:
        # Créer le message e-mail
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Envoyer l'e-mail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        st.success("Email sent successfully!")
        time.sleep(1)
        st.switch_page("1_app.py")
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")



# Fonction pour ajouter les données à la table payments
def add_payment_to_db(subscription_id, amount_paid, months_paid, start_date, end_date):
    try:
        # Récupérer l'ID utilisateur basé sur l'email stocké dans session_state
        user_email = st.session_state.get('email_user')
        if not user_email:
            st.error("User email not found in session_state.")
            return

        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            # Récupérer l'ID utilisateur depuis la base de données
            query_user_id = "SELECT id,name FROM users WHERE email = %s"
            cur.execute(query_user_id, (user_email,))
            user_id_result = cur.fetchone()
            if not user_id_result:
                st.error(f"No user found with email {user_email}")
                return
            user_id = user_id_result[0]
            name_user = user_id_result[1]
            # Préparer la requête d'insertion dans la table payments
            query = """
                INSERT INTO payments (user_id, subscription_id, amount_paid, payment_date, months_paid, start_date, abandoned)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            """
            abandoned = False
            cur.execute(query, (user_id, subscription_id, amount_paid, months_paid, start_date, abandoned))
            conn.commit()
            cur.close()
            conn.close()

            # Notification de succès
            st.success("Subscription successfully added!")

            # Envoi de l'e-mail
            email_subject = "Subscription Confirmation"
            email_body = f"""
            Dear {name_user},

            Your subscription has been successfully processed.
            Details:
            - Subscription ID: {subscription_id}
            - Amount Paid: ${amount_paid}
            - Start Date: {start_date}
            - End Date: {end_date}
            - Months Paid: {months_paid}

            Thank you for your trust!
            """
            send_email(user_email, email_subject, email_body)
    except Exception as e:
        st.error(f"Error adding payment to database: {e}")

# Interface utilisateur
st.title("Subscription Page")

with st.form("subscription_form"):
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())
    submit = st.form_submit_button("Subscribe")

if submit and st.session_state.get('id_choosen'):
    if end_date < start_date:
        st.error("The end date must be after the start date.")
    else:
        subscription_id = st.session_state['id_choosen']  # ID de l'abonnement choisi
        months_paid = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        amount_paid = months_paid * st.session_state.get('card_price', 0)  # Montant total basé sur le prix par mois
        add_payment_to_db(subscription_id, amount_paid, months_paid, start_date, end_date)

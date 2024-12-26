import streamlit as st
import psycopg2
from psycopg2 import sql


# Fonction de connexion à la base de données PostgreSQL
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


# Fonction pour récupérer les informations de l'utilisateur
def get_user_details():
    user_email = st.session_state.get('email_user')
    if not user_email:
        st.error("L'email de l'utilisateur est introuvable dans session_state.")
        return None, None

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            # Récupérer l'ID et le nom de l'utilisateur depuis la base de données
            query_user_id = "SELECT id, name FROM users WHERE email = %s"
            cur.execute(query_user_id, (user_email,))
            user_id_result = cur.fetchone()
            conn.close()

            if not user_id_result:
                st.error(f"Aucun utilisateur trouvé avec l'email {user_email}")
                return None, None

            return user_id_result[0], user_id_result[1]
        except Exception as e:
            st.error(f"Erreur lors de la récupération des détails de l'utilisateur : {e}")
            return None, None
    return None, None


# Fonction pour envoyer un email
def send_email(receiver_email, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "omarkhabou063@gmail.com"
    app_password = "wgqy oedl uuek jykt"  # Remplacez par le mot de passe d'application généré
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Préparation de l'email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Envoi de l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        st.success("Email envoyé avec succès.")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email : {e}")


# Interface utilisateur avec formulaire
user_id, name_user = get_user_details()
if name_user:
    with st.form("comment_form"):
        st.write(f"Bonjour, {name_user}. Veuillez entrer votre commentaire ci-dessous :")
        user_comment = st.text_area("Votre commentaire")
        submit = st.form_submit_button("Envoyer")

    if submit:
        if not user_comment.strip():
            st.error("Veuillez entrer un commentaire avant d'envoyer.")
        else:
            # Préparation de l'email
            email_subject = "Nouveau commentaire utilisateur"
            email_body = f"""
            Bonjour Administrateur,

            L'utilisateur {name_user} (ID: {user_id}) a envoyé le commentaire suivant :
            
            {user_comment}

            Merci de le traiter rapidement.
            """

            # Envoi de l'email
            send_email("admin_email@example.com", email_subject, email_body)

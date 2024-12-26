import pandas as pd
import streamlit as st
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from streamlit_option_menu import option_menu

# Database connection parameters
host = "localhost"
port = 5432
dbname = "streamlitdatabase"
user = "postgres"
password = "root"

st.set_page_config(initial_sidebar_state="collapsed", page_title="Ma Page", page_icon=":guardsman:")

def db_connection():
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return connection
    except Exception as error:
        st.error(f"Database connection error: {error}")
        return None

def fetch_data(query):
    connection = db_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
    finally:
        connection.close()

def create_bar_graph(data, x_col, y_col, title, xlabel, ylabel):
    data[y_col] = data[y_col].astype(int)
    plt.figure(figsize=(10, 6))
    fig = plt.gcf()
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#0E1117')  # Set the figure background color
    ax.set_facecolor('#0E1117')  # Set the axes background color
    ax.bar(data[x_col], data[y_col], color='skyblue')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel(ylabel, color='white')
    ax.set_title(title, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def create_pie_chart(data, x_col, y_col, title):
    data[y_col] = data[y_col].astype(int)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data[y_col], labels=data[x_col], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title(title, color='white')
    ax.set_facecolor('#0E1117')  # Set background color
    plt.tight_layout()
    return fig

def save_graphs_to_pdf(graphs):
    with PdfPages('dashboard_graphs.pdf') as pdf:
        for graph in graphs:
            pdf.savefig(graph)
            plt.close(graph)

def insert_subscription(name, price, internet_limit, call_minutes, social_networks, international_minutes, inwi_calls_unlimited, description):
    connection = db_connection()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO subscriptions 
                (name, price, internet_limit, call_minutes, social_networks, international_minutes, inwi_calls_unlimited, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, price, internet_limit, call_minutes, social_networks,
                international_minutes, inwi_calls_unlimited, description
            ))
            connection.commit()
            st.success("Subscription added successfully!")
    except Exception as e:
        st.error(f"Error inserting subscription: {e}")
    finally:
        connection.close()

# Sidebar navigation
st.sidebar.title("Navigation")
nav_items = ["Dashboard", "Users Details", "Subscriptions Details", "Payments Details", "Add a Subscription"]
styles = {
    "container": {
        "background-color": "#212121",  # Darker background for better contrast
        "padding": "10px",
        "border-radius": "12px",  # Slightly rounded corners for a modern look
        "font-size": "18px",  # Balanced font size for readability
        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.3)",  # Soft shadow for depth
    },
    "icon": {
        "color": "#ffffff",  # White icons for better contrast on dark background
        "font-size": "22px",  # Slightly larger icons for better visibility
    },
    "nav-link": {
        "color": "#bdbdbd",  # Light grey color for unselected links
        "font-size": "16px",  # Slightly bigger text for clarity
        "text-align": "center",
        "border-radius": "6px",  # Smooth rounded edges
        "padding": "10px 20px",  # Better padding for a comfortable clickable area
        "transition": "background-color 0.3s, color 0.3s",  # Smooth transition for hover effect
    },
    "nav-link-selected": {
        "background-color": "#007bff",  # Blue background for selected item
        "color": "white",  # White text for selected items
        "font-weight": "bold",  # Bold text for emphasis
        "box-shadow": "0 4px 10px rgba(0, 123, 255, 0.5)",  # Soft shadow for selected items
    },
    "menu-title": {
        "font-size": "20px",  # Adjusted title size for prominence
        "font-weight": "bold",  # Bold title for better emphasis
        "color": "#ffffff",  # White color to match the theme
    },
}

# Use selected to navigate through pages
selected = option_menu(
    menu_title="Navigation",  # Title for the navigation bar
    options=nav_items,  # List of navigation items
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=styles
)


# Dashboard
if selected == "Dashboard":
    st.title("Admin Subscriptions Dashboard")
    graphs = []

    # Most Purchased Subscriptions
    st.header("Most Purchased Subscriptions")
    subscriptions_query = """
        SELECT s.name, COUNT(p.id) AS purchases
        FROM payments p
        JOIN subscriptions s ON p.subscription_id = s.id
        GROUP BY s.name
        ORDER BY purchases DESC;
    """
    subscriptions_df = fetch_data(subscriptions_query)
    if subscriptions_df is not None and not subscriptions_df.empty:
        st.pyplot(create_bar_graph(subscriptions_df, 'name', 'purchases', 'Most Purchased Subscriptions', 'Subscription Plan', 'Number of Purchases'))
        graphs.append(create_bar_graph(subscriptions_df, 'name', 'purchases', 'Most Purchased Subscriptions', 'Subscription Plan', 'Number of Purchases'))
    else:
        st.write("No data available for most purchased subscriptions.")

    # Most Profitable Subscriptions
    st.header("Most Profitable Subscriptions")
    profitable_query = """
        SELECT s.name, SUM(p.amount_paid) AS total_revenue
        FROM payments p
        JOIN subscriptions s ON p.subscription_id = s.id
        GROUP BY s.name
        ORDER BY total_revenue DESC;
    """
    profitable_df = fetch_data(profitable_query)
    if profitable_df is not None and not profitable_df.empty:
        st.pyplot(create_bar_graph(profitable_df, 'name', 'total_revenue', 'Most Profitable Subscriptions', 'Subscription Plan', 'Total Revenue (DH)'))
        graphs.append(create_bar_graph(profitable_df, 'name', 'total_revenue', 'Most Profitable Subscriptions', 'Subscription Plan', 'Total Revenue (DH)'))
    else:
        st.write("No data available for most profitable subscriptions.")

    # Most Abandoned Subscriptions (Pie chart)
    st.header("Most Abandoned Subscriptions")
    abandoned_query = """
        SELECT s.name, COUNT(p.id) AS abandoned_count
        FROM payments p
        JOIN subscriptions s ON p.subscription_id = s.id
        WHERE p.abandoned = TRUE
        GROUP BY s.name
        ORDER BY abandoned_count DESC;
    """
    abandoned_df = fetch_data(abandoned_query)
    if abandoned_df is not None and not abandoned_df.empty:
        st.pyplot(create_pie_chart(abandoned_df, 'name', 'abandoned_count', 'Most Abandoned Subscriptions'))
        graphs.append(create_pie_chart(abandoned_df, 'name', 'abandoned_count', 'Most Abandoned Subscriptions'))
    else:
        st.write("No data available for most abandoned subscriptions.")

    # Save all the graphs to PDF
    if st.button("Export All Graphs as PDF"):
        save_graphs_to_pdf(graphs)
        st.success("All graphs have been exported to PDF.")

# Users Details
elif selected == "Users Details":
    st.title("User Details")
    users_query = "SELECT * FROM users;"
    users_df = fetch_data(users_query)
    if users_df is not None and not users_df.empty:
        user_name = st.selectbox("Select a user:", users_df["name"].tolist())
        if user_name:
            selected_user = users_df[users_df["name"] == user_name]
            st.subheader(f"Details for {user_name}:")
            st.write(selected_user)
    else:
        st.write("No users found.")

# Subscriptions Details
elif selected == "Subscriptions Details":
    st.title("Subscription Details")
    subscriptions_query = "SELECT * FROM subscriptions;"
    subscriptions_df = fetch_data(subscriptions_query)
    if subscriptions_df is not None and not subscriptions_df.empty:
        st.dataframe(subscriptions_df)
    else:
        st.write("No subscriptions found.")

# Payments Details
elif selected == "Payments Details":
    st.title("Payment Details")
    payments_query = """
        SELECT p.id, u.name AS user_name, s.name AS subscription_name, p.amount_paid, 
               p.payment_date, p.months_paid, p.start_date, p.abandoned
        FROM payments p
        JOIN users u ON p.user_id = u.id
        JOIN subscriptions s ON p.subscription_id = s.id;
    """
    payments_df = fetch_data(payments_query)
    if payments_df is not None and not payments_df.empty:
        st.dataframe(payments_df)
    else:
        st.write("No payments found.")

# Add a Subscription
elif selected == "Add a Subscription":
    st.title("Add Subscription")

    # Subscription Form
    with st.form("add_subscription_form"):
        name = st.text_input("Subscription Name")
        price = st.number_input("Price (DH)", min_value=0.0, step=0.01)
        internet_limit = st.text_input("Internet Limit (e.g., 2GB, 15GB, Unlimited)")
        call_minutes = st.text_input("Call Minutes (e.g., Unlimited, 100 min, etc.)")
        social_networks = st.text_area("Social Networks (Comma-separated list)", "Facebook, Instagram, WhatsApp")
        international_minutes = st.text_input("International Minutes (e.g., 120 min, Unlimited)")
        inwi_calls_unlimited = st.checkbox("Unlimited Inwi Calls")
        description = st.text_area("Description")

        submit_button = st.form_submit_button("Add Subscription")
        
        if submit_button:
            insert_subscription(name, price, internet_limit, call_minutes, social_networks, international_minutes, inwi_calls_unlimited, description)

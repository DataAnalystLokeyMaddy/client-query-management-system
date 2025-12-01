import streamlit as st
import mysql.connector
import hashlib
import pandas as pd
from datetime import datetime

# ----------------- BASIC CONFIG -----------------
st.set_page_config(page_title="Client Query Management System")

# ----------------- DB CONNECTION -----------------
def get_db_connection():
    """Create and return a MySQL connection."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",                 # change if your MySQL has password
        database="client_management" # make sure this DB exists
    )
    return conn

# ----------------- PASSWORD HASH -----------------
def hash_password(password: str) -> str:
    """Return SHA-256 hash of a password."""
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------- REGISTER USER -----------------
def register_user(username: str, password: str, role: str) -> bool:
    """
    Insert a new user into the users table.
    Returns True if success, False if fail (e.g. username already exists).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            """,
            (username, password_hash, role)
        )
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        print("Error during registration:", err)
        success = False
    finally:
        cursor.close()
        conn.close()

    return success

# ----------------- AUTHENTICATE USER -----------------
def authenticate_user(username: str, password: str):
    """
    Check username + password.
    Returns role ('Client' or 'Support') if correct, else None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    query = """
        SELECT role FROM users
        WHERE username = %s AND password_hash = %s
    """
    cursor.execute(query, (username, password_hash))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]   # 'Client' or 'Support'
    else:
        return None

# ----------------- CLIENT PAGE -----------------
def show_client_page():
    st.subheader("Client – Submit a New Query")

    with st.form("new_query_form"):
        email = st.text_input("Email ID")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")

        submitted = st.form_submit_button("Submit Query")

    if submitted:
        # Basic validation
        if email == "" or mobile == "" or heading == "" or description == "":
            st.error("Please fill all fields.")
            return

        # mobile number validation
        try:
            mobile_int = int(mobile)
        except ValueError:
            st.error("Mobile number must be numeric.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO queries
            (csv_query_id, client_email, client_mobile, query_heading,
             query_description, status, date_raised, date_closed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        now = datetime.now()
        data = (
            None,           # csv_query_id (no CSV id for new query)
            email,
            mobile_int,
            heading,
            description,
            "Open",         # status
            now,
            None            # date_closed
        )

        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()

        st.success("Your query has been submitted successfully!")

# ----------------- SUPPORT PAGE -----------------
def show_support_page():
    st.subheader("Support – Query Management Dashboard")

    # Filter by status
    status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])

    conn = get_db_connection()

    if status_filter == "All":
        sql = "SELECT * FROM queries"
        df = pd.read_sql(sql, conn)
    else:
        sql = "SELECT * FROM queries WHERE status = %s"
        df = pd.read_sql(sql, conn, params=(status_filter,))

    st.write("### Query List")
    st.dataframe(df)

    # Select a query to close
    open_queries = df[df['status'] == 'Open']

    if not open_queries.empty:
        st.write("### Close an Open Query")

        selected_id = st.selectbox(
            "Select Query ID to Close",
            open_queries['id'].tolist()
        )

        if st.button("Close Selected Query"):
            cursor = conn.cursor()
            update_sql = """
                UPDATE queries
                SET status = %s, date_closed = %s
                WHERE id = %s
            """
            cursor.execute(update_sql, ("Closed", datetime.now(), selected_id))
            conn.commit()
            cursor.close()

            st.success(f"Query ID {selected_id} has been closed.")
            st.rerun()
    else:
        st.info("No open queries to close right now.")

    conn.close()

# ----------------- STREAMLIT APP (MAIN) -----------------

# Use session_state to remember logged-in user
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

st.title("Client Query Management System")

# If not logged in -> show login / register
if st.session_state['role'] is None:
    mode = st.radio("Select Mode", ["Login", "Register"])

    # ---------- LOGIN ----------
    if mode == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = authenticate_user(username, password)

            if role:
                st.session_state['role'] = role
                st.session_state['username'] = username
                st.success(f"Logged in as {role}")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # ---------- REGISTER ----------
    else:
        st.subheader("Register New User")

        new_username = st.text_input("New Username (use email for clients)")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["Client", "Support"])

        if st.button("Register"):
            if new_username == "" or new_password == "":
                st.error("Username and password cannot be empty.")
            else:
                ok = register_user(new_username, new_password, new_role)
                if ok:
                    st.success("User registered successfully! Now switch to Login tab.")
                else:
                    st.error("Registration failed. Username may already exist.")

# If logged in -> show correct page
else:
    st.write(f"Hello, **{st.session_state['username']}**! (Role: {st.session_state['role']})")

    if st.button("Logout"):
        st.session_state['role'] = None
        st.session_state['username'] = None
        st.rerun()

    if st.session_state['role'] == "Client":
        show_client_page()
    elif st.session_state['role'] == "Support":
        show_support_page()

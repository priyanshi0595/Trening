import streamlit as st
import sqlite3
import datetime

# ------------------ Database Connection ------------------
def con():
    c = sqlite3.connect("fittrack.db", check_same_thread=False)
    cr = c.cursor()

    cr.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT
        )
    """)

    cr.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            wid INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            date TEXT,
            exercise TEXT,
            duration INTEGER,
            calories_burned INTEGER,
            FOREIGN KEY(userid) REFERENCES users(id)
        )
    """)
    c.commit()
    return c


conn = con()
cursor = conn.cursor()

# ------------------ Streamlit UI ------------------
st.title("🏃 FitTrack - Personal Fitness Tracker")

menu = st.sidebar.selectbox(
    "Main Menu",
    ["Register User", "Log Exercise", "View User Workouts", "View All Users"]
)

# ------------------ Register User ------------------
if menu == "Register User":
    st.header("Register New User")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    if st.button("Register"):
        cursor.execute(
            "INSERT INTO users (name, age, gender) VALUES (?, ?, ?)",
            (name, age, gender)
        )
        conn.commit()
        st.success(f"User **{name}** registered successfully!")

# ------------------ Log Exercise ------------------
elif menu == "Log Exercise":
    st.header("Log Exercise")

    user_id = st.number_input("User ID", min_value=1, step=1)
    exercise = st.text_input("Exercise Name")
    duration = st.number_input("Duration (minutes)", min_value=1, step=1)
    calories = st.number_input("Calories Burned", min_value=1, step=1)

    if st.button("Log Exercise"):
        date = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute(
            """INSERT INTO workouts 
               (userid, date, exercise, duration, calories_burned)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, date, exercise, duration, calories)
        )
        conn.commit()
        st.success("Exercise logged successfully!")

# ------------------ View User Workouts ------------------
elif menu == "View User Workouts":
    st.header("User Workouts")

    user_id = st.number_input("Enter User ID", min_value=1, step=1)

    if st.button("View Workouts"):
        cursor.execute(
            "SELECT date, exercise, duration, calories_burned FROM workouts WHERE userid = ?",
            (user_id,)
        )
        rows = cursor.fetchall()

        if rows:
            st.table(rows)
        else:
            st.warning("No workouts found for this user.")

# ------------------ View All Users ------------------
elif menu == "View All Users":
    st.header("All Registered Users")

    cursor.execute("SELECT id, name, age, gender FROM users")
    users = cursor.fetchall()

    if users:
        st.table(users)
    else:
        st.info("No users registered yet.")
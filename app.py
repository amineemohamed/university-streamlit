import streamlit as st
import psycopg2
import pandas as pd
from psycopg2 import sql


DB_CONFIG = {
    "dbname": "prodject",
    "user": "postgres",
    "password": "amine",
    "host": "localhost",
    "port": 5432
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def fetch_table(table_name):
    q = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    with get_conn() as conn:
        return pd.read_sql(q.as_string(conn), conn)

def execute_query(query, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()


def insert_student(name, role, major, year):
    execute_query("INSERT INTO students (name, role, major, year_of_study) VALUES (%s,%s,%s,%s)",
                  (name, role, major, year))

def update_student(id_, name, major, year):
    execute_query("UPDATE students SET name=%s, major=%s, year_of_study=%s WHERE id=%s",
                  (name, major, year, id_))

def delete_student(id_):
    execute_query("DELETE FROM students WHERE id=%s", (id_,))

def insert_teacher(name, role, department, rank):
    execute_query("INSERT INTO teachers (name, role, department, rank) VALUES (%s,%s,%s,%s)",
                  (name, role, department, rank))

def update_teacher(id_, name, department, rank):
    execute_query("UPDATE teachers SET name=%s, department=%s, rank=%s WHERE id=%s",
                  (name, department, rank, id_))

def delete_teacher(id_):
    execute_query("DELETE FROM teachers WHERE id=%s", (id_,))

def insert_admin(name, role, position, office):
    execute_query("INSERT INTO adminstaff (name, role, position, office) VALUES (%s,%s,%s,%s)",
                  (name, role, position, office))

def update_admin(id_, name, position, office):
    execute_query("UPDATE adminstaff SET name=%s, position=%s, office=%s WHERE id=%s",
                  (name, position, office, id_))

def delete_admin(id_):
    execute_query("DELETE FROM adminstaff WHERE id=%s", (id_,))

def insert_course(course_name, credits):
    execute_query("INSERT INTO courses VALUES (%s,%s)", (course_name, credits))

def update_course(old_name, new_name, credits):
    execute_query("UPDATE courses SET course_name=%s, credits=%s WHERE course_name=%s",
                  (new_name, credits, old_name))

def delete_course(course_name):
    execute_query("DELETE FROM courses WHERE course_name=%s", (course_name,))

def insert_grade(student_id, course_name, credits, score, letter):
    query = """
    INSERT INTO grades (student_id, grade)
    VALUES (%s, (ROW((%s,%s)::course_type, %s, %s))::grade_type)
    """
    execute_query(query, (student_id, course_name, credits, score, letter))

# ---------- Streamlit UI ----------
st.set_page_config(page_title="University DB Manager", layout="wide")
st.title("🎓 University System ")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose view", [
    "Show All Tables",
    "Students (CRUD)",
    "Teachers (CRUD)",
    "Adminstaff (CRUD)",
    "Courses (CRUD)",
    "Grades (CRUD)"
])

# Connection test
if st.sidebar.button("Test DB Connection"):
    try:
        with get_conn() as conn:
            st.success("✅ Connected to database 'prodject'")
    except Exception as e:
        st.error(f"❌ Connection error: {e}")

# ---------- SHOW ALL ----------
if page == "Show All Tables":
    st.header("All tables preview")
    tables = ["people", "person_table", "students", "teachers", "adminstaff", "courses", "grades"]
    for t in tables:
        st.subheader(t)
        try:
            st.dataframe(fetch_table(t))
        except Exception as e:
            st.error(f"Error reading {t}: {e}")

# ---------- STUDENTS ----------
if page == "Students (CRUD)":
    st.header("Students — view / add / edit / delete")
    try:
        st.dataframe(fetch_table("students"))
    except Exception as e:
        st.error(e)

    with st.form("add_student"):
        name = st.text_input("Name")
        major = st.text_input("Major")
        year = st.number_input("Year of study", min_value=1, max_value=10, value=1)
        if st.form_submit_button("Add student"):
            insert_student(name, "Student", major, year)
            st.success("Student added")
            st.experimental_rerun()

    with st.form("edit_student"):
        try:
            ids = fetch_table("students")["id"].tolist()
        except Exception:
            ids = []
        id_sel = st.selectbox("Select student id", options=ids)
        new_name = st.text_input("New name")
        new_major = st.text_input("New major")
        new_year = st.number_input("New year", min_value=1, max_value=10, value=1)
        update_btn = st.form_submit_button("Update student")
        delete_btn = st.form_submit_button("Delete student")
        if update_btn:
            update_student(id_sel, new_name, new_major, new_year)
            st.success("Updated")
            st.experimental_rerun()
        elif delete_btn:
            delete_student(id_sel)
            st.success("Deleted")
            st.experimental_rerun()

# ---------- TEACHERS ----------
if page == "Teachers (CRUD)":
    st.header("Teachers — view / add / edit / delete")
    try:
        st.dataframe(fetch_table("teachers"))
    except Exception as e:
        st.error(e)

    with st.form("add_teacher"):
        name = st.text_input("Name")
        department = st.text_input("Department")
        rank = st.text_input("Rank")
        if st.form_submit_button("Add teacher"):
            insert_teacher(name, "Teacher", department, rank)
            st.success("Teacher added")
            st.experimental_rerun()

    with st.form("edit_teacher"):
        try:
            ids = fetch_table("teachers")["id"].tolist()
        except Exception:
            ids = []
        id_sel = st.selectbox("Select teacher id", options=ids)
        new_name = st.text_input("New name")
        new_dept = st.text_input("New department")
        new_rank = st.text_input("New rank")
        update_btn = st.form_submit_button("Update teacher")
        delete_btn = st.form_submit_button("Delete teacher")
        if update_btn:
            update_teacher(id_sel, new_name, new_dept, new_rank)
            st.success("Updated")
            st.experimental_rerun()
        elif delete_btn:
            delete_teacher(id_sel)
            st.success("Deleted")
            st.experimental_rerun()

# ---------- ADMIN ----------
if page == "Adminstaff (CRUD)":
    st.header("Adminstaff — view / add / edit / delete")
    try:
        st.dataframe(fetch_table("adminstaff"))
    except Exception as e:
        st.error(e)

    with st.form("add_admin"):
        name = st.text_input("Name")
        position = st.text_input("Position")
        office = st.text_input("Office")
        if st.form_submit_button("Add admin"):
            insert_admin(name, "Admin", position, office)
            st.success("Admin added")
            st.experimental_rerun()

    with st.form("edit_admin"):
        try:
            ids = fetch_table("adminstaff")["id"].tolist()
        except Exception:
            ids = []
        id_sel = st.selectbox("Select admin id", options=ids)
        new_name = st.text_input("New name")
        new_position = st.text_input("New position")
        new_office = st.text_input("New office")
        update_btn = st.form_submit_button("Update admin")
        delete_btn = st.form_submit_button("Delete admin")
        if update_btn:
            update_admin(id_sel, new_name, new_position, new_office)
            st.success("Updated")
            st.experimental_rerun()
        elif delete_btn:
            delete_admin(id_sel)
            st.success("Deleted")
            st.experimental_rerun()

# ---------- COURSES ----------
if page == "Courses (CRUD)":
    st.header("Courses — view / add / edit / delete")
    try:
        st.dataframe(fetch_table("courses"))
    except Exception as e:
        st.error(e)

    with st.form("add_course"):
        cname = st.text_input("Course name")
        credits = st.number_input("Credits", min_value=1, max_value=10, value=3)
        if st.form_submit_button("Add course"):
            insert_course(cname, credits)
            st.success("Course added")
            st.experimental_rerun()

    with st.form("edit_course"):
        try:
            opts = fetch_table("courses")["course_name"].tolist()
        except Exception:
            opts = []
        old = st.selectbox("Select course", options=opts)
        new_name = st.text_input("New course name")
        new_credits = st.number_input("New credits", min_value=1, max_value=10, value=3)
        update_btn = st.form_submit_button("Update course")
        delete_btn = st.form_submit_button("Delete course")
        if update_btn:
            update_course(old, new_name, new_credits)
            st.success("Updated")
            st.experimental_rerun()
        elif delete_btn:
            delete_course(old)
            st.success("Deleted")
            st.experimental_rerun()

# ---------- GRADES ----------
if page == "Grades (CRUD)":
    st.header("Grades — view / add / delete")
    try:
        df = fetch_table("grades")
        st.dataframe(df)
    except Exception as e:
        st.error(e)

    with st.form("add_grade"):
        try:
            student_opts = fetch_table("students")["id"].tolist()
        except Exception:
            student_opts = []
        s_id = st.selectbox("Student id", options=student_opts)
        course_name = st.text_input("Course name")
        credits = st.number_input("Credits", min_value=1, max_value=10, value=3)
        score = st.number_input("Score", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
        letter = st.text_input("Letter (A/B/C...)")
        if st.form_submit_button("Add grade"):
            insert_grade(s_id, course_name, credits, score, letter)
            st.success("Grade added")
            st.experimental_rerun()

    with st.form("del_grade"):
        try:
            student_opts = fetch_table("grades")["student_id"].unique().tolist()
        except Exception:
            student_opts = []
        sid = st.selectbox("Student id to delete all grades", options=student_opts)
        if st.form_submit_button("Delete grades"):
            execute_query("DELETE FROM grades WHERE student_id=%s", (sid,))
            st.success("Deleted")
            st.experimental_rerun()

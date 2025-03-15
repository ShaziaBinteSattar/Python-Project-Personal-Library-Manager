import streamlit as st
import sqlite3
import pandas as pd

# Database Functions
def create_table():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn TEXT)''')
    conn.commit()
    conn.close()

def add_book(title, author, year, isbn):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", 
              (title, author, year, isbn))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect("library.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df

def update_book(book_id, title, author, year, isbn):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", 
              (title, author, year, isbn, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("📚 Personal Library Manager")

menu = ["Add Book", "View Books", "Update Book", "Delete Book"]
choice = st.sidebar.selectbox("Menu", menu)

create_table()

if choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    isbn = st.text_input("ISBN")

    if st.button("Add Book"):
        add_book(title, author, year, isbn)
        st.success(f"✅ '{title}' by {author} added!")

elif choice == "View Books":
    st.subheader("📖 View Books")
    books = get_books()
    st.dataframe(books)

elif choice == "Update Book":
    st.subheader("✏️ Update Book Details")
    books = get_books()
    book_ids = books["id"].tolist()
    book_id = st.selectbox("Select Book ID", book_ids)
    
    if book_id:
        book_data = books[books["id"] == book_id].iloc[0]
        new_title = st.text_input("Title", book_data["title"])
        new_author = st.text_input("Author", book_data["author"])
        new_year = st.number_input("Year", min_value=0, max_value=2100, step=1, value=int(book_data["year"]))
        new_isbn = st.text_input("ISBN", book_data["isbn"])

        if st.button("Update Book"):
            update_book(book_id, new_title, new_author, new_year, new_isbn)
            st.success("✅ Book updated!")

elif choice == "Delete Book":
    st.subheader("❌ Delete Book")
    books = get_books()
    book_ids = books["id"].tolist()
    book_id = st.selectbox("Select Book ID to Delete", book_ids)

    if st.button("Delete"):
        delete_book(book_id)
        st.warning("🚨 Book deleted!")

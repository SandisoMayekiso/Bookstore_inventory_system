# ============================================
# 📚 Bookstore Inventory System (GUI + SQLite)
# Author: Sandiso Mayekiso
# ============================================

import sqlite3
from tkinter import *
from tkinter import messagebox

# ---------- DATABASE SETUP ----------
def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            isbn TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()
    view()

def view():
    listbox.delete(0, END)
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    for row in rows:
        listbox.insert(END, row)
    conn.close()

def search(title="", author="", year="", isbn=""):
    listbox.delete(0, END)
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR year LIKE ? OR isbn LIKE ?
    """, (f"%{title}%", f"%{author}%", f"%{year}%", f"%{isbn}%"))
    rows = cur.fetchall()
    for row in rows:
        listbox.insert(END, row)
    conn.close()

def delete():
    try:
        selected_item = listbox.curselection()[0]
        book_id = listbox.get(selected_item)[0]
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()
        view()
        messagebox.showinfo("Deleted", "Book deleted successfully!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a book to delete.")

def update():
    try:
        selected_item = listbox.curselection()[0]
        book_id = listbox.get(selected_item)[0]
        conn = sqlite3.connect("books.db")
        cur = conn.cursor()
        cur.execute("""
            UPDATE books
            SET title=?, author=?, year=?, isbn=?
            WHERE id=?
        """, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get(), book_id))
        conn.commit()
        conn.close()
        view()
        messagebox.showinfo("Updated", "Book updated successfully!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a book to update.")

def clear_entries():
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    year_entry.delete(0, END)
    isbn_entry.delete(0, END)

def select_item(event):
    try:
        global selected_book
        index = listbox.curselection()[0]
        selected_book = listbox.get(index)
        clear_entries()
        title_entry.insert(END, selected_book[1])
        author_entry.insert(END, selected_book[2])
        year_entry.insert(END, selected_book[3])
        isbn_entry.insert(END, selected_book[4])
    except IndexError:
        pass

# ---------- GUI SETUP ----------
window = Tk()
window.title("📚 Bookstore Inventory System")
window.config(padx=15, pady=15, bg="#f8f9fa")

# ---------- LABELS ----------
Label(window, text="Title:", bg="#f8f9fa").grid(row=0, column=0, sticky=W)
Label(window, text="Author:", bg="#f8f9fa").grid(row=0, column=2, sticky=W)
Label(window, text="Year:", bg="#f8f9fa").grid(row=1, column=0, sticky=W)
Label(window, text="ISBN:", bg="#f8f9fa").grid(row=1, column=2, sticky=W)

# ---------- ENTRIES ----------
title_text = StringVar()
author_text = StringVar()
year_text = StringVar()
isbn_text = StringVar()

title_entry = Entry(window, textvariable=title_text, width=25)
title_entry.grid(row=0, column=1)

author_entry = Entry(window, textvariable=author_text, width=25)
author_entry.grid(row=0, column=3)

year_entry = Entry(window, textvariable=year_text, width=25)
year_entry.grid(row=1, column=1)

isbn_entry = Entry(window, textvariable=isbn_text, width=25)
isbn_entry.grid(row=1, column=3)

# ---------- LISTBOX & SCROLLBAR ----------
listbox = Listbox(window, height=12, width=70)
listbox.grid(row=2, column=0, columnspan=4, rowspan=6, pady=10)

scrollbar = Scrollbar(window)
scrollbar.grid(row=2, column=4, rowspan=6, sticky='ns')

listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)
listbox.bind('<<ListboxSelect>>', select_item)

# ---------- BUTTONS ----------
Button(window, text="View All", width=14, command=view, bg="#00b4d8", fg="white").grid(row=2, column=5)
Button(window, text="Search", width=14, command=lambda: search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()), bg="#0077b6", fg="white").grid(row=3, column=5)
Button(window, text="Add Book", width=14, command=lambda: insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()), bg="#2a9d8f", fg="white").grid(row=4, column=5)
Button(window, text="Update", width=14, command=update, bg="#f4a261", fg="white").grid(row=5, column=5)
Button(window, text="Delete", width=14, command=delete, bg="#e76f51", fg="white").grid(row=6, column=5)
Button(window, text="Clear", width=14, command=clear_entries, bg="#adb5bd", fg="white").grid(row=7, column=5)
Button(window, text="Close", width=14, command=window.destroy, bg="#6c757d", fg="white").grid(row=8, column=5, pady=(10, 0))

connect()
view()
window.mainloop()

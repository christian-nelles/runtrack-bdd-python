import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import ttkbootstrap as tb
import pwinput

def mdp():
    try:
        user_password = pwinput.pwinput("Entrez votre mot de passe : ")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=user_password,
            database="store"
        )
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("Mot de passe incorrect")
        mdp()

def load_products():
    cursor.execute(
        """SELECT product.id, product.name, category.name, product.price, product.quantity 
        FROM product 
        INNER JOIN category ON product.id_category = category.id"""
    )
    return cursor.fetchall()

def display_products():
    for row in tree.get_children():
        tree.delete(row)
    for product in load_products():
        tree.insert("", "end", values=product)
def load_categories():
    cursor.execute("SELECT id, name FROM category")
    return cursor.fetchall()


def add_product():
    name = entry_name.get().strip()
    price = entry_price.get().strip()
    quantity = entry_quantity.get().strip()
    category_id = entry_category.get().strip()

    if not name or not price.isdigit() or not quantity.isdigit() or not category_id.isdigit():
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
        return

    cursor.execute(
        "INSERT INTO product (name, price, quantity, id_category) VALUES (%s, %s, %s, %s)",
        (name, int(price), int(quantity), int(category_id))
    )
    conn.commit()
    display_products()
    clear_entries()

def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un produit à supprimer.")
        return

    product_id = tree.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    display_products()

def update_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un produit à modifier.")
        return

    product_id = tree.item(selected_item, "values")[0]
    new_price = entry_price.get().strip()
    new_quantity = entry_quantity.get().strip()

    if not new_price.isdigit() or not new_quantity.isdigit():
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
        return

    cursor.execute(
        "UPDATE product SET price = %s, quantity = %s WHERE id = %s",
        (int(new_price), int(new_quantity), product_id)
    )
    conn.commit()
    display_products()

def export_csv():
    products = load_products()
    df = pd.DataFrame(products, columns=["ID", "Nom", "Catégorie", "Prix", "Stock"])
    df.to_csv("stock.csv", index=False)
    messagebox.showinfo("Export", "Exporté avec succès en stock.csv")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_category.delete(0, tk.END)

root = tb.Window(themename="superhero")  
root.title("Gestion de Stock")
root.geometry("900x600")

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

sidebar = ttk.Frame(main_frame, width=200, relief="ridge")
sidebar.pack(side="left", fill="y", padx=10, pady=10)

btn_add = ttk.Button(sidebar, text="➕ Ajouter", command=add_product, bootstyle="success")
btn_add.pack(fill="x", pady=5)

btn_update = ttk.Button(sidebar, text="✏️ Modifier", command=update_product, bootstyle="warning")
btn_update.pack(fill="x", pady=5)

btn_delete = ttk.Button(sidebar, text="❌ Supprimer", command=delete_product, bootstyle="danger")
btn_delete.pack(fill="x", pady=5)

btn_export = ttk.Button(sidebar, text="📤 Exporter CSV", command=export_csv, bootstyle="info")
btn_export.pack(fill="x", pady=5)

content_frame = ttk.Frame(main_frame)
content_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Nom", "Catégorie", "Prix", "Stock")
tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

entry_frame = ttk.Frame(content_frame)
entry_frame.pack(fill="x", pady=10)

ttk.Label(entry_frame, text="Nom").grid(row=0, column=0, padx=5)
entry_name = ttk.Entry(entry_frame)
entry_name.grid(row=0, column=1, padx=5)

ttk.Label(entry_frame, text="Prix").grid(row=0, column=2, padx=5)
entry_price = ttk.Entry(entry_frame)
entry_price.grid(row=0, column=3, padx=5)

ttk.Label(entry_frame, text="Stock").grid(row=1, column=0, padx=5)
entry_quantity = ttk.Entry(entry_frame)
entry_quantity.grid(row=1, column=1, padx=5)

ttk.Label(entry_frame, text="ID Catégorie").grid(row=1, column=2, padx=5)
entry_category = ttk.Entry(entry_frame)
entry_category.grid(row=1, column=3, padx=5)

category_frame = ttk.Frame(content_frame)
category_frame.pack(fill="x", pady=10)

ttk.Label(category_frame, text="Liste des catégories").pack()

category_tree = ttk.Treeview(category_frame, columns=("ID", "Nom"), show="headings", height=5)
category_tree.heading("ID", text="ID")
category_tree.column("ID", width=50)
category_tree.heading("Nom", text="Nom")
category_tree.column("Nom", width=150)

category_tree.pack(fill="x")

def display_categories():
    for row in category_tree.get_children():
        category_tree.delete(row)
    for category in load_categories():
        category_tree.insert("", "end", values=category)

conn, cursor = mdp()

display_categories()
display_products()

root.mainloop()

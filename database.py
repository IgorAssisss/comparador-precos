# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 01:13:47 2025

@author: Assis
"""

import sqlite3

DB_NAME = "google_shopping.db"

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Criar a tabela de produtos corretamente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                produto_id TEXT PRIMARY KEY,
                nome_produto TEXT,
                marca TEXT
            )
        ''')

        # Criar a tabela de ofertas corretamente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ofertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id TEXT,
                nome_produto TEXT,
                marca TEXT,
                vendedor TEXT,
                preco TEXT
            )
        ''')

        conn.commit()

def save_products(products):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for item in products:
            cursor.execute('''
                INSERT OR IGNORE INTO produtos (produto_id, nome_produto, marca) VALUES (?, ?, ?)
            ''', (item['Produto ID'], item['Nome do Produto'], item['Marca']))
        conn.commit()

def get_products_by_brand(brand):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT produto_id, nome_produto FROM produtos WHERE marca = ?", (brand,))
        return cursor.fetchall()

def save_offers(offers):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for item in offers:
            cursor.execute('''
                INSERT INTO ofertas (produto_id, nome_produto, marca, vendedor, preco)
                VALUES (?, ?, ?, ?, ?)
            ''', (item['Produto ID'], item['Nome do Produto'], item['Marca'], item['Vendedor'], item['Preço']))
        conn.commit()

def get_offers_by_brand(brand):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ofertas WHERE marca = ?", (brand,))
        return cursor.fetchall()

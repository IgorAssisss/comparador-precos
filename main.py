# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 00:43:47 2025

@author: Assis
"""

from buscar_ids import main as buscar_ids
from coletar_ofertas import main as coletar_ofertas
from database import create_tables

if __name__ == "__main__":
    create_tables()
    buscar_ids()
    coletar_ofertas()

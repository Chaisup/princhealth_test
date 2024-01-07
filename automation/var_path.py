# ====================================================================================================
# Python script to define global variables of path
# Directory Map
# 📂 princhealth_test       -> root_path
# > 📂 automation           -> this_path
# > > 📃 var_path.py        -> "This and other .py scripts are here."
# > 📂 ProductSalesAmount   -> "This and other output folders are here."
# > 📦 medcury-de.db        -> "The SQLite database"
# ----------------------------------------------------------------------------------------------------
# Import

import os


# ----------------------------------------------------------------------------------------------------
# Declare

this_path = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(this_path, os.pardir))

path_db = os.path.abspath(os.path.join(root_path, 'medcury-de.db'))
# path_db = r'C:\BLACK\OneDrive\Projects\princhealth_test\medcury-de.db'


# ----------------------------------------------------------------------------------------------------
# Test

# print(this_path)
# print(root_path)
# print(path_db)



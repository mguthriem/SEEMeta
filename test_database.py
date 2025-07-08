import os
import json
import traceback
from SEEmeta import material,opposedAnvilCell,anvil
from sqlalchemy import create_engine

# ===================== LOAD MATERIALS DATABASE ================
# Connect to your DB
engine = create_engine("sqlite:///materials/materials.db")
# Load all materials into a list
materials = material.load_all(engine)
nMat = len(materials)
print(f"Loaded {nMat} materials from the database.")
for mat in materials:
    print(mat.name, mat.id)  # Print first 3
    if mat.hasSpectra:
        print(f"Material {mat.name} has {len(mat.spectra)} spectra associated with it.")    

zta = material(engine,name="zta")
print(f"Material ZTA ID: {zta.get_id()}")
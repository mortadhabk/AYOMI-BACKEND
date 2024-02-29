from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from Npi import Npi
from fastapi.middleware.cors import CORSMiddleware
import csv
from fastapi.responses import FileResponse

# init fastapi
app = FastAPI()

# ajoute de CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connection avec la bd ( je peux utiliser un Fichier ENV pour securisé les informations de connexion) 
conn = psycopg2.connect(
    dbname="test_db",
    user="admin@admin.com",
    password="admin",
    host="db",
    port="5432"
)

# defenir la table
create_table_query = """
CREATE TABLE IF NOT EXISTS calculations (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result FLOAT
);
"""

# execute la requete
with conn.cursor() as cursor:
    cursor.execute(create_table_query)
    conn.commit()

# defenir la classe pour les calculs
class Calculation(BaseModel):
    expression: str
   

# defenir les routes
@app.post("/calculate/")
async def calculate(calculation: Calculation):
    try:
        # faire une instance de la classe Npi
        calc = Npi()
        result = calc.calculatrice(calculation.expression)
        
        # inserer les calculs dans la bd
        insert_query = "INSERT INTO calculations (expression, result) VALUES (%s, %s);"
        with conn.cursor() as cursor:
            cursor.execute(insert_query, (calculation.expression, result))
            conn.commit()

        # retourner le resultat
        return {"result": result}
    except psycopg2.Error as e:
        conn.rollback()
        return {"error": str(e)}


# exporter les calculs en format csv
@app.get("/export/csv")
async def export_csv():
        try:
            # recuperer les calculs
            select_query = "SELECT * FROM calculations;"
            with conn.cursor() as cursor:
                cursor.execute(select_query)
                rows = cursor.fetchall()

            # defenir le chemin du fichier
            csv_file_path = "./export.csv"

            # ecrire les calculs dans le fichier
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "expression", "result"])  # Write header
                writer.writerows(rows)  # Write data rows

            return FileResponse(csv_file_path, filename="export.csv")
        except psycopg2.Error as e:
            return {"error": str(e)}
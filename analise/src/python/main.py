import os
import pandas as pd
import xml.etree.ElementTree as ET
from export_excel_retorno_ans import export_excel, extrair_str, extrair_df

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "dados", "Retorno")

#ler a lista de arquivos da pasta

#carregar os dados em df para cada um e fazer um append
df = export_excel(DATA_DIR = DATA_DIR, file = "4175992024010001.XTR")
print(df.head())
print(df.tail())

#exportar para excel






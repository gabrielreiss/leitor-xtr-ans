import os
import pandas as pd
import xml.etree.ElementTree as ET

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "dados", "Retorno")

arquivo = "4175992024010001.XTR"
tree = ET.parse(source = os.path.join(DATA_DIR, arquivo))
root = tree.getroot()
#self.parser = ET.XMLParser(encoding="utf-8") 

#solução para tratar o prefixo ans
#https://stackoverflow.com/questions/40772297/syntaxerror-prefix-a-not-found-in-prefix-map

#extrair um elemento por vez
for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}tipoTransacao"):
    print(desc.text)
    
for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}resumoProcessamento"):
    x = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}nomeArquivo").text
    print(x)

# This code snippet is attempting to extract the text content of elements with the tag
# `{http://www.ans.gov.br/padroes/tiss/schemas}tipoRegistro` under each `resumoProcessamento` element
# in the XML file. However, there is a mistake in the code.
tipoRegistro = []
CNES = []
for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}guiaMonitoramento"):
    temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}tipoRegistro").text
    tipoRegistro.append(temp)
    
    contratadoExecutante = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}contratadoExecutante")
    temp = contratadoExecutante.find("{http://www.ans.gov.br/padroes/tiss/schemas}CNES").text
    CNES.append(temp)    
    
    #agora só reproduzir para todas as variáveis

len(tipoRegistro)
print(tipoRegistro)
    
    
    
    
#tentando transformar em tabela
df = pd.DataFrame(data = {
    "tipoRegistro": tipoRegistro,
    "CNES": CNES
})

print(df)


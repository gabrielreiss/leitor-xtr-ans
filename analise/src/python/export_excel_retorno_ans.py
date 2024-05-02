import os
import pandas as pd
import xml.etree.ElementTree as ET

def export_excel(DATA_DIR: str, file: str) -> pd.DataFrame:
    tree = ET.parse(source = os.path.join(DATA_DIR, file))
    root = tree.getroot()

    tipoRegistro = []
    CNES = []

    for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}guiaMonitoramento"):
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}tipoRegistro").text
        tipoRegistro.append(temp)

        contratadoExecutante = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}contratadoExecutante")
        temp = contratadoExecutante.find("{http://www.ans.gov.br/padroes/tiss/schemas}CNES").text
        CNES.append(temp)    

        #agora só reproduzir para todas as variáveis
        #colocar competência e metadados
        #não esquecer o tipo de erro informado no evento

    return pd.DataFrame(data={"tipoRegistro": tipoRegistro,"CNES": CNES})
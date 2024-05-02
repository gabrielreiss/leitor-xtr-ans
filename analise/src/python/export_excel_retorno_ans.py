import os
import pandas as pd
import xml.etree.ElementTree as ET
from itertools import repeat

def extrair_str(schema: str, name: str, tree: ET.parse) -> str:
    cabecalho = []

    for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}{schema}"):
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}{name}").text
        cabecalho.append(temp)
        
    return cabecalho

def extrair_df(name:str, tree: ET.parse) -> pd.DataFrame:
    #agora só reproduzir para todas as variáveis
    #colocar competência e metadados
    #não esquecer o tipo de erro informado no evento
    
    tipoRegistro = []
    CNES = []
    identificadorExecutante = []
    codigoCNPJ_CPF = []
    numeroGuiaPrestador = []
    numeroGuiaOperadora = []
    identificadorReembolso = []
    dataProcessamento = []
    identificadorCampo = []
    codigoErro = []

    for desc in tree.findall(".//{http://www.ans.gov.br/padroes/tiss/schemas}guiaMonitoramento"):
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}tipoRegistro").text
        tipoRegistro.append(temp)

        contratadoExecutante = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}contratadoExecutante")
        temp = contratadoExecutante.find("{http://www.ans.gov.br/padroes/tiss/schemas}CNES").text
        CNES.append(temp)

        contratadoExecutante = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}contratadoExecutante")
        temp = contratadoExecutante.find("{http://www.ans.gov.br/padroes/tiss/schemas}identificadorExecutante").text
        identificadorExecutante.append(temp)
        
        contratadoExecutante = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}contratadoExecutante")
        temp = contratadoExecutante.find("{http://www.ans.gov.br/padroes/tiss/schemas}codigoCNPJ_CPF").text
        codigoCNPJ_CPF.append(temp)

        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}numeroGuiaPrestador").text
        numeroGuiaPrestador.append(temp)
        
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}numeroGuiaOperadora").text
        numeroGuiaOperadora.append(temp)
        
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}identificadorReembolso").text
        identificadorReembolso.append(temp)
        
        temp = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}dataProcessamento").text
        dataProcessamento.append(temp)
        
        errosGuia = desc.find("{http://www.ans.gov.br/padroes/tiss/schemas}errosGuia")
        temp = errosGuia.find("{http://www.ans.gov.br/padroes/tiss/schemas}identificadorCampo").text
        identificadorCampo.append(temp)
        
        temp = errosGuia.find("{http://www.ans.gov.br/padroes/tiss/schemas}codigoErro").text
        codigoErro.append(temp)
    
    tipoTransacao = pd.Series(repeat(extrair_str("identificacaoTransacao", "tipoTransacao", tree), len(tipoRegistro)))
    print(tipoTransacao)
    numeroLote = repeat(extrair_str("identificacaoTransacao","numeroLote", tree),len(tipoRegistro))
    competenciaLote = repeat(extrair_str("identificacaoTransacao","competenciaLote", tree),len(tipoRegistro))
    dataRegistroTransacao = repeat(extrair_str("identificacaoTransacao","dataRegistroTransacao", tree),len(tipoRegistro))
    horaRegistroTransacao = repeat(extrair_str("identificacaoTransacao","horaRegistroTransacao", tree),len(tipoRegistro))
    registroANS = repeat(extrair_str("cabecalho", "registroANS", tree),len(tipoRegistro))
    versaoPadrao = repeat(extrair_str("cabecalho", "versaoPadrao", tree),len(tipoRegistro))
    nomeArquivo = pd.Series(repeat(extrair_str("resumoProcessamento", "nomeArquivo",tree),len(tipoRegistro)))

    return pd.DataFrame(data={"tipoRegistro": tipoRegistro,"CNES": CNES, "identificadorExecutante": identificadorExecutante, "codigoCNPJ_CPF": codigoCNPJ_CPF, "numeroGuiaPrestador": numeroGuiaPrestador, "numeroGuiaOperadora": numeroGuiaOperadora, "identificadorReembolso": identificadorReembolso, "dataProcessamento": dataProcessamento, "identificadorCampo": identificadorCampo, "codigoErro": codigoErro, "tipoTransacao": tipoTransacao, "numeroLote": numeroLote, "competenciaLote": competenciaLote, "dataRegistroTransacao": dataRegistroTransacao, "horaRegistroTransacao": horaRegistroTransacao, "registroANS": registroANS, "versaoPadrao": versaoPadrao, "nomeArquivo": nomeArquivo})

def export_excel(DATA_DIR: str, file: str) -> pd.DataFrame:
    tree = ET.parse(source = os.path.join(DATA_DIR, file))
    root = tree.getroot()

    tipoTransacao = extrair_str("identificacaoTransacao", "tipoTransacao", tree)
    numeroLote = extrair_str("identificacaoTransacao","numeroLote", tree)
    competenciaLote = extrair_str("identificacaoTransacao","competenciaLote", tree)
    dataRegistroTransacao = extrair_str("identificacaoTransacao","dataRegistroTransacao", tree)
    horaRegistroTransacao = extrair_str("identificacaoTransacao","horaRegistroTransacao", tree)
    registroANS = extrair_str("cabecalho", "registroANS", tree)
    versaoPadrao = extrair_str("cabecalho", "versaoPadrao", tree)
    nomeArquivo = extrair_str("resumoProcessamento", "nomeArquivo",tree)
    
    df_cabecalho = pd.DataFrame(data={
        "tipoTransacao": tipoTransacao,
        "numeroLote": numeroLote,
        "competenciaLote": competenciaLote,
        "dataRegistroTransacao": dataRegistroTransacao,
        "horaRegistroTransacao": horaRegistroTransacao,
        "registroANS": registroANS,
        "versaoPadrao": versaoPadrao,
        "nomeArquivo": nomeArquivo
    })

    df_conteudo = extrair_df("guiaMonitoramento", tree)

    #return df_cabecalho.join(df_conteudo, how = "right")
    #return df_cabecalho.merge(df_conteudo, left_on = True, right_on = True)
    #return pd.concat([df_cabecalho, df_conteudo], axis = 1)
    #return pd.merge(df_cabecalho, df_conteudo, how="cross")
    return df_conteudo
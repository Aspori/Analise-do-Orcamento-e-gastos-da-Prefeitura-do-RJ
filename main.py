import pandas as pd
import sqlite3
import openpyxl

df = pd.read_excel('data/data.xlsx', header=5)

df.columns = ['ano', 'tipo_renuncia', 'cnpj', 'nome_titular', 'valor_total', 'quantidade_inscricao', 'inscricao']

# tira as linhas que estão completamente vazias
df = df.dropna(how='all')

# Limpa valor total, removendo o símbolo de moeda e convertendo para float
if df['valor_total'].dtype == 'object':
    df['valor_total'] = (df['valor_total'].astype(str)
                          .str.replace('R$', '', regex=False)
                          .str.replace('.', '', regex=False)
                          .str.replace(',', '.', regex=False)
                          .astype(float))

df["cnpj"] = (df["cnpj"].astype(str)
              .str.replace(r"\D", "", regex=True)   # tira tudo que não é dígito
              .str.zfill(14))                        # recoloca zeros à esquerda

#tira todas as linhas duplicadas
df = df.drop_duplicates()

con = sqlite3.connect('data/data.db')
df.to_sql('renuncia', con, if_exists='replace', index=False)

print(df.shape)
print(df['ano'].unique())
print(df['tipo_renuncia'].unique())
print(df['valor_total'].describe())

con.close()
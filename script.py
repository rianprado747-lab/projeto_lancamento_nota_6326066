import pyautogui as py
import webbrowser as web
import time
import pandas as pd
import numpy as np
import os
py.PAUSE = 0.5
link = 'https://docs.google.com/forms/d/e/1FAIpQLSdA4reFjax6TAqGeDaQUu2N0RJXP_-NQJ-HGf8KCNjvNjhp-A/viewform?usp=header'
tabela_alunos = pd.read_csv("notas_alunos.csv", sep=';')


def tratar_tabela(tabela_alunos):
    tabela_alunos['RA'] = tabela_alunos['RA'].astype(str).str.replace(r'\D', '', regex=True)
    tabela_alunos['Nome'] = tabela_alunos['Nome'].str.strip().str.title()
    tabela_alunos['Nome'] = tabela_alunos['Nome'].str.replace('  ',' ', regex=False) 

    colunas_notas = ['Nota01', 'TF01', 'Nota02', 'TF02']
    for coluna in colunas_notas:
        tabela_alunos[coluna] = tabela_alunos[coluna].astype(str)
        tabela_alunos[coluna] = tabela_alunos[coluna].str.replace(',', '.')
        substituicoes = ['FALTOU', 'falta', 'N/A', 'nan', '-', ' ']
        for palavra in substituicoes:
            tabela_alunos[coluna] = tabela_alunos[coluna].str.replace(palavra, '0.0', regex=False)
        tabela_alunos[coluna] = pd.to_numeric(tabela_alunos[coluna], errors='coerce').fillna(0.0)
    #limita as notas ao máximo de 10.0
    tabela_alunos['Nota01'] = np.where(tabela_alunos['Nota01'] > 10.0, 10.0, tabela_alunos['Nota01'])
    tabela_alunos['Nota02'] = np.where(tabela_alunos['Nota02'] > 10.0, 10.0, tabela_alunos['Nota02'])
    #limita as notas do tf ao máximo de 2.0
    tabela_alunos['TF01'] = np.where(tabela_alunos['TF01'] > 2.0, 2.0, tabela_alunos['TF01'])
    tabela_alunos['TF02'] = np.where(tabela_alunos['TF02'] > 2.0, 2.0, tabela_alunos['TF02'])
    return tabela_alunos


def abrir_link(link):
    web.open(link)
    time.sleep(5)


def preencher_forms(nome,ra,nota1,tf01,nota2,tf02,nf1,nf2,media,situacao): 
    py.scroll(5000)
    py.click(666,385)
    campos = [nome,ra,nota1,tf01,nota2,tf02,nf1,nf2,media,situacao]
    for dado in campos:
        py.write(str(dado), interval=0.05)
        py.press('tab')
    py.press('enter')


def cadastro_alunos(tabela):
    confirmacao = py.confirm(
        text='Por favor, verifique se o Google Forms está aberto e se a ordem das perguntas é exatamente: nome,ra,nota1,tf01,nota2,tf02,nf1,nf2,media,situacao).\n\nPodemos iniciar a digitação?',
        title='Verificação de Segurança do Robô',
        buttons=['Sim, tudo certo!', 'Não, cancelar']
    )
    
    if confirmacao != 'Sim, tudo certo!':
        print('Automação cancelada pelo usuário. Ajuste o Forms e tente novamente.')
        return 
    
    print('Iniciando o preenchimento automático')
    for l in tabela.index:
        nome = tabela.loc[l,'Nome']
        ra = tabela.loc[l,'RA']
        nota1 = tabela.loc[l,'Nota01']
        tf1 = tabela.loc[l,'TF01']
        nota2 = tabela.loc[l,'Nota02']
        tf2 = tabela.loc[l,'TF02']
        nf1 = tabela.loc[l,'Nota_Final_01']
        nf2 = tabela.loc[l,'Nota_Final_02']
        media = tabela.loc[l,'Media_Final']
        situacao = tabela.loc[l,'Situacao']
        preencher_forms(nome,ra,nota1,tf1,nota2,tf2,nf1,nf2,media,situacao)
        time.sleep(3)
        py.hotkey('ctrl','l')
        py.write(link)
        py.press('enter')
        time.sleep(4)


def calcular_notas(tabela):
    tabela['Nota_Final_01'] = (tabela['Nota01'] * 0.8 ) + (tabela['TF01'] * 0.2)
    tabela['Nota_Final_02'] = (tabela['Nota02'] * 0.8 ) + (tabela['TF02'] * 0.2)
    tabela['Media_Final'] = (tabela['Nota_Final_01'] + tabela['Nota_Final_02']) / 2
    tabela['Situacao'] = np.where(tabela['Media_Final'] >= 7.0, 'Aprovado', 'Reprovado')
    colunas_calculadas = ['Nota_Final_01', 'Nota_Final_02', 'Media_Final']
    tabela[colunas_calculadas] = tabela[colunas_calculadas].round(2)
    return tabela


def busca_dados(tabela):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        busca = str(input('Digite nome ou ra do aluno:[1-SAIR]')).strip()
        if busca == '1':
            break
        aluno = tabela[(tabela['RA']== busca) | (tabela['Nome'] == busca)]
        if not aluno.empty:
            print(aluno)
        else:
            print('Aluno não encontrado')

        input("\nPressione ENTER para buscar outro aluno...")

tabela_alunos = tratar_tabela(tabela_alunos)
tabela_alunos = calcular_notas(tabela_alunos)
abrir_link(link)
cadastro_alunos(tabela_alunos)
busca_dados(tabela_alunos)

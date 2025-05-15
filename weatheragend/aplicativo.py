import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import geocoder
import os
import sys
from win32com.client import Dispatch
import winshell
from pathlib import Path
import ctypes.wintypes
import subprocess

'''istalar o PyInstaller''' 
def instalar_pyinstaller():
    try:
        import PyInstaller
        print("PyInstaller já instalado.")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def criar_exe(nome_script):
    caminho_script = os.path.abspath(nome_script)
    diretorio_script = os.path.dirname(caminho_script)
    os.chdir(diretorio_script)
    print(f"Diretório atual: {os.getcwd()}")
    print(f"Compilando script: {caminho_script}")
    comando = [sys.executable, "-m", "PyInstaller", "--onefile", "--windowed", caminho_script]
    subprocess.check_call(comando)

if __name__ == "__main__":
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    nome_do_script = os.path.join(pasta_atual, "previsaotempo.py")

    if not os.path.isfile(nome_do_script):
        print(f"Erro: arquivo {nome_do_script} não encontrado.")
        sys.exit(1)

    instalar_pyinstaller()
    criar_exe(nome_do_script)



'''Criar atalho na área de trabalho'''
def criar_atalho_no_desktop(nome_atalho, caminho_alvo):
    desktop = winshell.desktop()
    caminho_atalho = os.path.join(desktop, f"{nome_atalho}.lnk")

    shell = Dispatch('WScript.Shell')
    atalho = shell.CreateShortcut(caminho_atalho)
    atalho.TargetPath = caminho_alvo
    atalho.WorkingDirectory = os.path.dirname(caminho_alvo)
    atalho.IconLocation = caminho_alvo
    atalho.save()
    print(f"Atalho criado em: {caminho_atalho}")

if __name__ == "__main__":
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(pasta_atual, "dist", "previsaotempo.exe")

    if not os.path.isfile(exe_path):
        print("Erro: Executável não encontrado. Compile o exe antes de criar o atalho.")
        sys.exit(1)

    criar_atalho_no_desktop("PrevisaoTempo", exe_path)


'''Localizar o usuario'''
g = geocoder.ip('me')
cidade = g.city
pais = g.country


API_KEY = 'f735300abb8fadb243af1cbcba5d4d81'
CIDADE = f'{cidade},{pais}'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIDADE}&appid={API_KEY}&units=metric&lang=pt_br"

'''Estrutura da Janela'''
Tela_inicial = Tk()
Tela_inicial.title("Water Diary")
Tela_inicial.geometry("900x600")
Tela_inicial.resizable(True, True)
Tela_inicial.config(bg="Silver") 


'''Titulo'''
label_titulo = tk.Label(Tela_inicial, text="Previsão do Tempo", font=("Helvetica", 24, "bold"), bg="Silver")
label_titulo.pack(pady=20)


'''Icone do Tempo'''
label_icone = tk.Label(Tela_inicial, bg="Silver")
label_icone.pack()


'''Tenoeratura'''
label_temp = tk.Label(Tela_inicial, font=("Helvetica", 48), bg="Silver")
label_temp.pack()


'''descrição'''
label_desc = tk.Label(Tela_inicial, font=("Helvetica", 20), bg="Silver")
label_desc.pack()


'''Umildade'''
label_umidade = tk.Label(Tela_inicial, font=("Helvetica", 16), bg="Silver")
label_umidade.pack()


'''atualizar ao iniciar'''
def atualizar_clima():
    try:
        resposta = requests.get(URL)
        dados = resposta.json()
        print(dados)

        if resposta.status_code != 200:
            raise Exception(dados.get("message", "Erro ao obter dados."))
        
        temp = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        umidade = dados['main']['humidity']
        icone_id = dados['weather'][0]['icon']

        
        label_temp.config(text=f"{temp:.1f} °C")
        label_desc.config(text=descricao.capitalize())
        label_umidade.config(text=f"Umidade: {umidade}%")

        
        icone_url = f"http://openweathermap.org/img/wn/{icone_id}@2x.png"
        icone_img = Image.open(BytesIO(requests.get(icone_url).content))
        icone_tk = ImageTk.PhotoImage(icone_img)
        label_icone.config(image=icone_tk)
        label_icone.image = icone_tk

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível atualizar o clima.\n{e}")

atualizar_clima()


'''Inicia programa'''
Tela_inicial.mainloop()

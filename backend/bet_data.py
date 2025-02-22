import pandas as pd
import numpy as np
import matplotlib as mpl
import json


def seteKBET():
    df = pd.read_json(r'data\data7KBET.json', encoding='utf-8')
    qtd = len(df["data"])
    qtd
    acc = 0
    print("\n7KBET\n")
    
    while acc < qtd:
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        print(partida)
        print(aposta)
        print(odd)
        acc +=1
        
def apostaTudo():
    df = pd.read_json(r'data\dataAPOSTATUDO.json', encoding='utf-8')
    qtd = len(df["data"])
    qtd
    acc1 = 0
    acc2 = 0
    print("\nAPOSTATUDO\n")
    
    while acc1 < qtd:
        partida = df["data"][acc1][10]
        odd = df["data"][acc1][19][0][7][0][4]
        aposta = df["data"][acc1][19][0][7][0][1]["BR-PT"]
        if odd == 0 or aposta == "Não":
            pass
        else:
            print(partida)    
            print(aposta)
            print(odd)
        acc1 +=1
    
    while acc2 < qtd:
        partida = df["data"][acc2][10]
        odd = df["data"][acc2][19][0][7][1][4]
        aposta = df["data"][acc2][19][0][7][1][1]["BR-PT"]
        if odd == 0 or aposta == "Não":
            pass
        else:
            print(partida)     
            print(aposta)
            print(odd)
        acc2 +=1
      


def bateuBET():
    df = pd.read_json(r'data\dataBATEUBET.json', encoding='utf-8')
    qtd = len(df["data"])
    qtd
    acc = 0
    print("\nBATEUBET\n")
    
    while acc < qtd:
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        print(partida) 
        print(aposta)
        print(odd)
        acc +=1

def cassinoBET():
    df = pd.read_json(r'data\dataCASSINOBET.json', encoding='utf-8')
    qtd = len(df["data"])
    qtd
    acc = 0
    print("\nCASSINOBET\n")
    
    while acc < qtd:
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        print(partida) 
        print(aposta)
        print(odd)
        acc +=1

def veraBET():
    df = pd.read_json(r'data\dataVERABET.json', encoding='utf-8')
    qtd = len(df["data"])
    qtd
    acc = 0
    print("\nVERABET\n")
    
    while acc < qtd:
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        print(partida) 
        print(aposta)
        print(odd)
        acc +=1
        
seteKBET()
apostaTudo()
bateuBET()
cassinoBET()
veraBET()
﻿import numpy as np
import pandas as pd
from pyodide.http import open_url
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from js import document
import joblib
import requests
from io import BytesIO

url="https://raw.githubusercontent.com/KenroyDytrim/PyScript/main/pickle_model.pkl"

clf = joblib.load(BytesIO(requests.get(url).content))

names=["Изменение контуров замыкательных пластинок", "Клиновидная форма тел позвонков", "Грыжи Шморля", "Остеопороз тел позвонков", "Уменьшение высоты межпозвоночного диска", "Изменение контуров апофизов", "Признаки остеохондроза", "ЭНМГ"]

ch=['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']
an=['an1', 'an2', 'an3', 'an4', 'an5', 'an6', 'an7', 'an8', 'an9']

r1=['r1_1', 'r1_2', 'r1_3', 'r1_4', 'r1_5', 'r1_6', 'r1_7', 'r1_8']

def analysis(*args, **kwargs):
  error = document.getElementById('err')
  error.setAttribute('style', 'width: 45vw; display:none;')

  main = document.getElementById('main')
  main.setAttribute('style', 'display:none;')
  
  st=""
  for i in r1:
    resS = Element(i)
    res = document.getElementById(i)
    resS.write(st)
    res.setAttribute('style', 'display:none')

  y1=[]
  pr=[]
    
  text=[]
  for i in range(len(an)):
    buff = document.getElementById(an[i])
    if buff.value != '':
        text.append(buff.value)
    else:
        error.setAttribute('style', 'width: 45vw;')
        return

  buff = document.getElementById('an10')
  if(buff.checked):
    text.append(1)
  else:
    text.append(0)  
      
  namet=np.array(['Cal', 'Fos', 'Oks', 'EksKal', 'EksFos', 'EksOks', 'DCT', 'Time', 'Kifoz', 'StabIzmen'])
  td=np.array(text)
  test=pd.DataFrame(columns= namet)
  test.loc[ len(test.index )] =td
  
  st1=''

  kol=0

  for i in range(len(ch)):
    buff = document.getElementById(ch[i])
    if(buff.checked):
      kol+=1
      y1.append(int(buff.value))

  if kol > 0:
      main.setAttribute('style', 'display:flex; justify-content: space-around; align-items: baseline; flex-wrap: nowrap; font-size: 18px;')
    
  y_pred=clf.predict(test)

  for i in y1:
    st1="{0}: {1} ".format(names[i], y_pred[0][i])
    res1 = Element(r1[i])
    res1.write(st1)
    resT = document.getElementById(r1[i])
    resT.style.display = 'block'

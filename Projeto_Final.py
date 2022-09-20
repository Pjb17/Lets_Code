#!/usr/bin/env python
# coding: utf-8

# In[19]:


import requests as r
#Importa o requests e "apelidamos" como "r" para facilitar


# In[20]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)
#url recebe o endereço da api e r.get recebe a url armazenando os dados na variável resp


# In[21]:


resp.status_code
#Verifica o status dos dados; 200=ok


# In[22]:


raw_data = resp.json()
#raw_data recebe o arquivo .json contendo os dados da api


# In[23]:


raw_data[0]
#Apresenta um dicionário contendo o header obtido por meio da api


# In[24]:


final_data =[]
for obs in raw_data:
    final_data.append([obs['Confirmed'],obs['Deaths'],obs['Recovered'],obs['Active'],obs['Date']])
#final_data recebe apenas os dados filtrados, sendo eliminados os demais


# In[25]:


final_data.insert(0, ['Confirmados', 'Mortes', 'Recuperados', 'Ativos', 'Data'])
#recebe apenas os dados definidos como esseciais
final_data


# In[26]:


Confirmados = 0
Mortes = 1
Recuperados = 2
Ativos = 3
Data = 4
#Para facilitar, cada coluna recebe um número de acordo com a posição na tabela, sempre começando de 0


# In[27]:


for i in range(1, len(final_data)):
    final_data[i][Data]= final_data[i][Data][:10]


# In[28]:


final_data


# In[29]:


import datetime as dt
#Importamos a biblioteca datetime apelidando como dt


# In[30]:


import csv
#importamos a biblioteca csv


# In[31]:


with open ('brasil-covid.csv','w',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)
#Inicio da escrita de um arquivo .csv usando os dados de final_data


# In[32]:


for i in range(1, len(final_data)):
    final_data[i][Data] = dt.datetime.strptime(final_data[i][Data],'%Y-%m-%d')
#Transforma as datas que até então eram strings em datas próriamente ditas, no formato "YYYY/MM/DD"


# In[33]:


final_data


# In[48]:


def get_datasets(y, labels):
    #Responsável pelos chave dataset da API Quickchart que constrói os dados de 'Y'
    if type(y[0]) == list:
        #Verifica se o valor de y é uma lista
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
            #Variável datasets recebe um dicionário com as chaves label e data, que recebem respectivamente os labels e valores de y na posdição 'i'.
        return datasets
        #Retorn o dicionário 'datasets'
    else:
    #Caso não seja uma lista, recebe label na posição 0 e o valor de y nas chaves label e data, respectivamente, retornando o resultado posteriormente.
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]


# In[49]:


def set_title(title=''):
    #Responsável pelo título do gráfico que será gerado.
    if title != '':
    #Verifica se title é uma string vazia
        display = 'true'
    else:
        display = 'false'
    return {
    #Retorna um dicionário contendo titúlo e display, que serão apresentados ou não dependendo do resultado da condicional
        'title': title,
        'display': display
    }


# In[50]:


def create_chart (x, y, labels, kind='bar', title=''):
    #Responsável pela criação do gráfico recebendo valores de 'x' e 'y', labels, tipo do gráfico e o título.
    datasets = get_datasets (y, labels)
    #Referencia a função criada anteriormente afim de criar os datasets do gráfico
    options = set_title(title)
    #Refencia a função criada anteriormente para a criação do título que será mostrado no gráfico
    
    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    #Recebe um dicionário contendo o tipo do gráfico, os dados (valor de x e datasets), e as configurações do gráfico
    
    return chart


# In[51]:


def get_api_chart(chart):
    #Responsável por enviar os dados das funções definidas anteriormente para a API afim da criação do gráfico
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content
    #Retorn um valor .content pois será um valor binário, não um .json
    


# In[52]:


def save_image(path, content):
    #Responsável por salvar a imagem
    with open (path, 'wb') as image:
        #Abre o path (caminho da imagem gerada) em modo de escrita (write), mais especificamente 'wb', que é a escrita de binário.
        image.write(content)


# In[53]:


pip install Pillow
#Instalação da biblioteca Pillow


# In[54]:


from PIL import Image
from IPython.display import display
#Importação de duas funções específicas para mostrar a imagem na próxima função a ser definida


# In[57]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)
    #img_pil recebe o resultado da função Image sobre o path, eentão a função display apresenta a imagem como resultado


# In[76]:


y_data1 = []
for obs in final_data[1::10]:
    y_data1.append(obs[Confirmados])
#y_data1 recebe os valores de casos confirmados 

y_data2 = []
for obs in final_data[1::10]:
    y_data2.append(obs[Recuperados])
#y_data2 recebe o número de casos recuperados
    
labels = ['Confirmados', 'Recuperados']
#labels recebe o nome dos dados pra que o gráfico apresente como legenda 

x = []
for obs in final_data[1::10]:
    x.append(obs[Data].strftime('%d/%m/%Y'))
#x recebe as datas transformando de volta em string por meio do strftime
    
chart = create_chart(x, [y_data1,y_data2], labels, title='Gráfico confirmados vs recuperados')
#Ao chamar a função chart fornecemos os valores de x(datas), uma lista contendo y_data1 e y_data2, os labels, e o título do gráfico, quanto ao tipo o padrão será o gráfico de barra, portanto não é necessário especificar, a não ser que deseje outro tipo de gráfico
chart_content = get_api_chart(chart)
#A função chart content recebe o resultado de get_api_chart tendo os valores da função anterior como dados
save_image('meu-primeiro-grafico-python.png', chart_content)
#save_image recebe o nome do arquivo e o content a ser transformado em imagem
display_image('meu-primeiro-grafico-python.png')
#mostra a imagem ao usuário


# In[77]:


from urllib.parse import quote


# In[78]:


def get_api_qrcode(link):
    text = quote(link)
    #parsing do link para url
    url_base = 'https://quickchart.io/qr'
    #recebe o endereço para a api quickchart
    resp = r.get(f'{url_base}?text={text}')
    #recebe o r.get do link que irá gerar o QR Code
    return resp.content
    #retorna o content


# In[79]:


url_base = 'https://quickchart.io/chart'
link =f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:





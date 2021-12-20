
import pandas as pd
import os
import json
import tqdm 
import re
import plotly.express as px

FOLDER_PATH ='D:/Polytechnique/Etudes/Trimestre Automn 2021/Advanced Concepts in cloud computing/TP/TP3/results'

def plot(df,name):
    

    fig = px.line(df, x=3, y=9, title=f'power consumption for {name}')
    fig.update_layout(xaxis_title='time (s)',
                    yaxis_title='Energy consumption (Joule)')
    # print(fig)
    # images = os.path.join(FOLDER_PATH, 'images')
    if not os.path.exists("images"):
        os.mkdir("images")
    
    fig.write_image(f"images/{name}.jpeg")
    
    
    


files = [os.path.join(FOLDER_PATH, filename) for filename in os.listdir(FOLDER_PATH)]
total_energy={}
for file in tqdm.tqdm(files):
    name=os.path.basename(file)
    name=re.split('[/.]', name)[0]
    df = pd.read_csv(file, sep='=|;| ', 
                    engine='python', header=None)
    df[9]=df[9]*.001
    df[3]=(df[3]-df[3][0])/1000
    total_energy[name]=df[9].sum()
    plot(df,name)

fig1 = px.bar(x=total_energy.keys(), y=total_energy.values(), title=f'total power consumption')
fig1.update_layout(xaxis_title='instance',
                yaxis_title='Energy consumption (Joule)')

fig1.write_image(f"images/total.jpeg")
print(total_energy)
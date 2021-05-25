from datetime import datetime
import os
def GerarId():
    dat=datetime.now()

    return str(dat.day)+str(dat.month)+str(dat.year)+str(dat.hour)+str(dat.minute)+str(dat.second)

def CarregarAreas():
    
    pasta='./static/img/areas'
    dados=[p for p in os.walk(pasta)]
    
    areas=dados[0][1]
   
    data=[x[2] for x in dados[1:]]
    #print(areas)
    resultado={}
    for a,x in zip(areas,data):
        resultado[a]=[v.split(".")[0] for v in x]
        #print(x)
    
    return resultado
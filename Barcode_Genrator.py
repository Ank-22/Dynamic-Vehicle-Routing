import csv  
from PIL import Image
import barcode
import pandas as  pd
from barcode.writer import ImageWriter
import numpy as np
from random import randint

def GenrateBarcode_ID(Name,Address,):
    compare_Mdata=pd.read_csv('./MainData.csv')
    IDs=compare_Mdata.filter(['BarcodeID'])
    IDs=IDs.values
    EAN = barcode.get_barcode_class('ean13')
    flag=1
    while(flag==1):
            flag=0
            temp_id=randint(100000000000, 999999999999) 
            for j in range(len(IDs)):
                if(temp_id==IDs[j]):
                    flag=1
    IDs=np.append(arr=IDs,values=[temp_id])
    fields=pd.DataFrame({'Name':[Name],  
                             'Address':[Address], 
                            'Barcode_Id':[str(temp_id)]}
                            )
    with open('./MainData.csv', 'a') as f:                    
            fields.to_csv(f, header=False,index=False)
    ean = EAN(str(temp_id), writer=ImageWriter())
    fullname = ean.save('./static/Barcode/'+str(temp_id)+'.png') 
    print("Bar code genrated",fullname)     

if __name__ == '__main__':
    GenrateBarcode_ID('test','Address',)
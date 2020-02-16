import pandas as pd
import numpy as np


address_data=pd.read_csv('./MainData.csv')
barcode=address_data.filter(["BarcodeID"])
address_data=address_data.filter(["Address"])
data=pd.DataFrame({'ID':barcode["BarcodeID"],
                    'Address':address_data["Address"]})
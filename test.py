import pandas as pd 
import numpy as np 
from haversine import haversine,Unit

vehical_data=pd.read_csv("./vehical.csv")
depo_data=pd.read_csv("./Depo.csv")


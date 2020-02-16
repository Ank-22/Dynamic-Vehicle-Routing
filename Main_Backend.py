import Function_scripts as fs



def Call_Depopackage():
   var1,var2=fs.Call_Depo_Program()
   return var1,var2
    

def Call_Addpackage(PackageDepoCall,var1,var2):
   PackageDepoCall=int(PackageDepoCall)
   var3,var4=fs.Add_New_package(PackageDepoCall,var1,var2)
   return var3,var4
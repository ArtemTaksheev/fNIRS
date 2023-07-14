import numpy as np
import pandas as pd
from fnirs import fnirs
import os as os
class patient_fnirs:

    def __init__(self,name, fon_file, conditions) -> None:
        self.patient_name = name

        # self.fon_file = fnirs(fon_file,event_type="fon")
        # self.conditions = []
        # for i in conditions:
        #     self.conditions.append(fnirs(i,event_type="T1"))
        self.data = []
        if (fon_file != ""):
                self.data.append(fnirs(fon_file,event_type="fon"))
        for i in conditions:
            self.data.append(fnirs(i,event_type="T1"))

    def copy(self):
        print("not realized yet")
        return -1
    
    def export(self,path = "results"):
        # self.average.to_excel(path + self.file_name + "output.xlsx")
        os.makedirs(path, exist_ok=True)
        for i in self.data:
            i.average.to_csv(path  +'/'+ self.patient_name+ '_' + i.file_name + '_' + "output.csv",index=False) 
        # self.fon_file.average.to_csv(path + self.patient_name + '_' + self.fon_file.file_name + '_' + "output.csv",index=False)

    def patient_average(self):
        # self.fon_file.genegate_average_values()
        for i in self.data:
            i.genegate_average_values()
            
    def compare_easy(self,first,second,mode = [1, -1]):
        result = self.data[first].compare_easy(self.data[second],mode)
        self.data.append(result)

    def get_first_data(self):
        return self.data[0]
    
    def get_last_data(self):
        return self.data[len(self.data) - 1]

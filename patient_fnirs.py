from fnirs import fnirs
import os as os
class patient_fnirs:

    def __init__(self,name, file_path, marks_for_files) -> None:
        self.patient_name = name
        self.data = []
        for i in range(0,len(file_path)):
            self.data.append(fnirs(file_path[i],event_type=marks_for_files[i]))

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
    
    def add_filtered(self,index):
        filtered = self.data[index].create_filtered()
        self.data.append(filtered)

    def patient_filter(self):
        for i in self.data:
            i.filter()
    
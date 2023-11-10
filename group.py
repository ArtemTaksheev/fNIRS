from patient_fnirs import patient_fnirs
import os as os
import pandas as pd
class group_fnirs:

    def __init__(self,name = "group1", patients = []) -> None:
        self.group_name = name

        # self.fon_file = fnirs(fon_file,event_type="fon")
        # self.conditions = []
        # for i in conditions:
        #     self.conditions.append(fnirs(i,event_type="T1"))
        self.patients_data = []
        # for i in patients:
        #     self.patients_data.append(i)

    def add_patient_to_the_group(self,patient):
        self.patients_data.append(patient)

    def copy(self):
        print("not realized yet")
        return -1
    
    def export(self,path = "results",cond = 0,segment = 1,mode = "raw",name_of_result = "result01"):
        # self.average.to_excel(path + self.file_name + "output.xlsx")
        name = []
        result = []


        os.makedirs(path, exist_ok=True)
        try:
            if mode == "raw":
                for x in self.patients_data:
                    name.append(x.patient_name)
                    print(x.patient_name)
                    result.append(x.data[cond].average.loc[segment].values)
            else:
                for x in self.patients_data:
                    name.append(x.patient_name)
                    print(x.patient_name)
                    tmp_results = []
                    columns = []
                    
                    for i in range(0,len(x.data[cond].average.loc[segment].values)-2,2):
                        columns.append(x.data[cond].average.columns[i])
                        if mode == "total":
                            tmp_results.append(x.data[cond].average.loc[segment].values[i] + x.data[cond].average.loc[segment].values[i+1])
                        else:
                            tmp_results.append(x.data[cond].average.loc[segment].values[i] - x.data[cond].average.loc[segment].values[i+1])
                    result.append(tmp_results)
            result = pd.DataFrame(result)
            if mode == "raw":
                result.columns = x.data[cond].average.columns
            else:
                result.columns =columns
            result.insert(0,"Names",name)
            result.to_csv(path  +'/'+ name_of_result  + "output.csv",index=False) 
        except:
            print("Not enough data")

    def export_diff(self,path = "results"):
        # self.average.to_excel(path + self.file_name + "output.xlsx")
        fons = []
        vcpt1 = []
        vcpt2 = []
        vcpt3 = []
        name = []
        columns = []
        os.makedirs(path, exist_ok=True)

        for x in self.patients_data:
            name.append(x.patient_name)
            print(x.patient_name)
            # tmp = x.data[0].average.loc[1].values
            columns = []
            tmp_fons = []
            tmp_vcpt1 = []
            tmp_vcpt2 = []
            tmp_vcpt3 = []
            for i in range(0,len(x.data[0].average.loc[1].values)-2,2):
                columns.append(x.data[0].average.columns[i])
                tmp_fons.append(x.data[0].average.loc[1].values[i] - x.data[0].average.loc[1].values[i+1])
                tmp_vcpt1.append(x.data[1].average.loc[1].values[i] - x.data[1].average.loc[1].values[i+1])
                tmp_vcpt2.append(x.data[2].average.loc[1].values[i] - x.data[2].average.loc[1].values[i+1])
                tmp_vcpt3.append(x.data[3].average.loc[1].values[i] - x.data[3].average.loc[1].values[i+1])


            fons.append(tmp_fons)
            vcpt1.append(tmp_vcpt1)
            vcpt2.append(tmp_vcpt2)
            vcpt3.append(tmp_vcpt3)

        fons = pd.DataFrame(fons)
        fons.columns = columns
        fons.insert(0,"Names",name)
        fons.to_csv(path  +'/'+  'fons_diff_' + "output.csv",index=False) 

        vcpt1 = pd.DataFrame(vcpt1)
        vcpt1.columns = columns
        vcpt1.insert(0,"Names",name)
        vcpt1.to_csv(path  +'/'+  'vcpt1_diff_' + "output.csv",index=False) 

        vcpt2 = pd.DataFrame(vcpt2)
        vcpt2.columns = columns
        vcpt2.insert(0,"Names",name)
        vcpt2.to_csv(path  +'/'+  'vcpt2_diff_' + "output.csv",index=False) 

        vcpt3 = pd.DataFrame(vcpt3)
        vcpt3.columns = columns
        vcpt3.insert(0,"Names",name)
        vcpt3.to_csv(path  +'/'+  'vcpt3_diff_' + "output.csv",index=False) 

    def group_average(self):
        # self.fon_file.genegate_average_values()
        for i in self.patients_data:
            i.patient_average()
            
    def compare_easy(self,first,second,mode = [1, -1]):
        result = self.data[first].compare_easy(self.data[second],mode)
        self.data.append(result)

    def get_first_data(self):
        return self.data[0]
    
    def get_last_data(self):
        return self.data[len(self.data) - 1]
    
    def init_group(self, path):
        # working slow, how it can be speed up?
        dir = os.listdir(path)

        # print(dir)
        unique_dir = []
        for x in [s.split('_') for s in dir]:
            if x[0] not in unique_dir:
                unique_dir.append(x[0])
        print(unique_dir)

        for y in unique_dir:
            name = y
            marks = []
            paths = []
            for x in dir:
                if x.find(y) != -1:
                    if x.find("fon") != -1:
                        marks.append(["O1","C1"])
                    elif x.find("psy") != -1:
                        marks.append(["M1","E1","S1","E2","K1"])
                    else:
                        marks.append(["T1"])
                    paths.append(path +'\\'+ x)
            print(name)
            self.patients_data.append(patient_fnirs(name,paths,marks))   

    def filter_all_patients_data(self):
        print("Start filter")
        for i in self.patients_data:
            i.patient_filter()
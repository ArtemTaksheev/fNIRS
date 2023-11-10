
from fnirs import fnirs
from scipy import signal
import pandas as pd
import os as os
from patient_fnirs import patient_fnirs
from group import group_fnirs
def filter_data(fnirs):
    b, a = signal.butter(8, [0.025,0.45], 'bandpass')   # Конфигурационный фильтр 8 указывает порядок фильтра
    filtered = signal.filtfilt(b, a, fnirs.data)  # данные - это сигнал, который нужно отфильтровать
    fnirs.data = pd.DataFrame(filtered)

def try_fons():
    fon = fnirs()
    fon.fnirs_parser("fon.txt","fon")
    fon.print_plot_two_chanel(0,if_events=True)
    print(fon.events)
    fon.genegate_average_values()
    fon.print_average_stairs(0)
def try_vcpt_compare():
    print('--Parsing fnirs file--')
    filepath = 'eotest.txt'
    event_type = "C1"
    vcpt1 = fnirs()
    vcpt3 = fnirs()

    vcpt1.fnirs_parser("vcpt1.txt","T1")
    vcpt3.fnirs_parser("vcpt3.txt","T1")
    print(vcpt1.data.head(5))


    # vcpt1.print_plot_two_chanel(0)
    # vcpt1.print_events()
    vcpt1.print_plot_two_chanel(2, if_events=True)

    # filter_data(vcpt1)
    # vcpt1.normalize_data()
    print(vcpt1.data.head(5))
    vcpt1.print_plot_two_chanel(2, if_events=True)

    vcpt3.print_plot_two_chanel(2, if_events=True)
    # vcpt3.normalize_data()
    vcpt3.print_plot_two_chanel(2, if_events=True)
    vcpt1.genegate_average_values()
    print(vcpt1.average.head(5))
    vcpt1.print_average_stairs(0)

    vcpt3.genegate_average_values()
    print(vcpt3.average.head(5))
    vcpt3.print_average_stairs(0)
    mode = [1,-1]
    comp_1_3 = vcpt1.compare_easy(vcpt3,mode)
    print(comp_1_3.average.head(5))
    comp_1_3.print_average_stairs(0)
def patiens_filter():

    tmp = fnirs("data/vcpt1.txt",event_type="T1")
    tmp.print_plot_two_chanel(0,if_events=True)
    filtered = tmp.create_filtered()
    filtered.print_plot_two_chanel(0,if_events=True)
    filter_data(tmp)
    tmp.print_plot_two_chanel(0)

def patiens_export():
    files = ["data/fon.txt","data/vcpt1.txt","data/vcpt3.txt"]
    marks = [["O1","C1"],["T1"],["T1"]]

    patient1 = patient_fnirs("Patient",files,marks)

    patient1.patient_average()
    # for i in patient1.data:
    #     i.print_average_stairs(0)
    patient1.compare_easy(0,1)
    patient1.get_last_data().print_average_stairs(0)
    patient1.export()

def main():
    # patiens_export()
    # file = fnirs("E:\\data\\fnirs_data_psy\\first\\baa_7_fon.txt",event_type=["O1","C1"])
    # file.print_plot_two_chanel(2)
    # file.filter()
    # file.print_plot_two_chanel(2)
    # file = fnirs("e:\\data\\fnirs_txt_data\\lag_29vcpt3.txt","T1")
    # print(file.data)
    # print(file.events)
    path = "E:\\data\\fnirs_data_psy\\first"
    group = group_fnirs()

    group.init_group(path=path)
    # for i in group.patients_data:
    #     print(i.patient_name)
    # group.patients_data[0].data[0].print_plot_two_chanel(0,True)   
    group.filter_all_patients_data()
    group.group_average()             

    print("export")
    res_path = "withhyd"
    cond_text = ["fon_","psy_","vcpt1_","vcpt3_"]
    for i in range (0,4):
        group.export(res_path,cond = i,segment = 1, mode= "raw", name_of_result= cond_text[i])
        group.export(res_path,cond = i,segment = 1, mode= "diff", name_of_result= cond_text[i] + "diff_")
        group.export(res_path,cond = i,segment = 1, mode= "total", name_of_result= cond_text[i] + "total_")

    group.export(res_path,cond = 1,segment = 3, mode= "raw", name_of_result= "psy_se_")
    group.export(res_path,cond = 1,segment = 3, mode= "diff", name_of_result= "psy_se_diff_")
    group.export(res_path,cond = 1,segment = 3, mode= "total", name_of_result= "psy_se_total_")

    group.export(res_path,cond = 1,segment = 5, mode= "raw", name_of_result= "psy_ke_")
    group.export(res_path,cond = 1,segment = 5, mode= "diff", name_of_result= "psy_ke_diff_")
    group.export(res_path,cond = 1,segment = 5, mode= "total", name_of_result= "psy_ke_total_")



''
if __name__ == "__main__":
    main()

from fnirs import fnirs
from scipy import signal
import pandas as pd
from patient_fnirs import patient_fnirs

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


    # vcpt1 = fnirs()
    # vcpt3 = fnirs()

    # vcpt1.fnirs_parser("vcpt1.txt","T1")
    # vcpt3.fnirs_parser("vcpt3.txt","T1")
    # print(vcpt1.data.head(5))


    # # vcpt1.print_plot_two_chanel(0)
    # # vcpt1.print_events()
    # vcpt1.print_plot_two_chanel(2, if_events=True)

    # # filter_data(vcpt1)
    # # vcpt1.normalize_data()
    # print(vcpt1.data.head(5))
    # vcpt1.print_plot_two_chanel(2, if_events=True)

    # vcpt3.print_plot_two_chanel(2, if_events=True)
    # # vcpt3.normalize_data()
    # vcpt3.print_plot_two_chanel(2, if_events=True)
    # vcpt1.genegate_average_values()
    # print(vcpt1.average.head(5))
    # vcpt1.print_average_stairs(0)

    # vcpt3.genegate_average_values()
    # print(vcpt3.average.head(5))
    # vcpt3.print_average_stairs(0)
    # mode = [1,-1]
    # comp_1_3 = vcpt1.compare_easy(vcpt3,mode)
    # print(comp_1_3.average.head(5))
    # comp_1_3.print_average_stairs(0)
def main():
    fon = "data/fon.txt"
    conditions = ["data/vcpt1.txt","data/vcpt3.txt"]

    patient1 = patient_fnirs("Patient",fon,conditions)

    patient1.patient_average()
    # for i in patient1.data:
    #     i.print_average_stairs(0)
    patient1.compare_easy(0,1)
    patient1.get_last_data().print_average_stairs(0)
    patient1.export()
if __name__ == "__main__":
    main()
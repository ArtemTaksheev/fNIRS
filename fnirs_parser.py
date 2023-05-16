
from fnirs import fnirs

def main():
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
    # vcpt1.print_plot_two_chanel(2, if_events=True)

    vcpt1.genegate_average_values()
    print(vcpt1.average.head(5))
    # vcpt1.print_average_stairs(0)

    vcpt3.genegate_average_values()
    print(vcpt3.average.head(5))
    # vcpt3.print_average_stairs(0)



    mode = [1,-1]
    comp_1_3 = vcpt1.compare_easy(vcpt3,mode)

    print(comp_1_3.average.head(5))
    comp_1_3.print_average_stairs(0)
    
if __name__ == "__main__":
    main()
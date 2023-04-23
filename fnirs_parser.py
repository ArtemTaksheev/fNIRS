import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt


rx_dict = {
    'export_of': re.compile(r'OxySoft export of:\t(?P<export>.*)\n'),
    'export_date': re.compile(r'Export date:\t(?P<export_date>.*)\n'),
    'start_of_measurment': re.compile(r'Start of measurement:\t(?P<start_of_measurment>.*)\n'),
    'sample_rate': re.compile(r'Datafile sample rate:\t(?P<sample_rate>.*)\tHz\n'),
    'duration': re.compile(r'Datafile duration:\t(?P<duration>.*)\ts\n'),
    'number_of_samples':re.compile(r'Datafile total number of samples:\t(?P<nsamples>.*)\n'),
    'description':re.compile(r'Description:\t\n'),
    'light_source_wavelengths': re.compile(r'Light source wavelengths:\n'),
    'legend': re.compile(r'Legend:\n'),
    'data':re.compile(r'1	2	3	4.*\n'),
    
}

def _parse_line(line):

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def fnirs_parser(filepath,event_type = "test"):
    data = []  # create an empty list to collect the data
    light_source_wavelengths_data = []
    legend_data = []
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            if key == 'export_of':
                export_path = match.group('export')
                print("found export path: " + export_path)

            if key == 'export_date':
                export_data = match.group('export_date')
                print("found export data: " + export_data)
            
            if key == 'start_of_measurment':
                start_of_measurment = match.group('start_of_measurment')
                print("found start of measurment: " + start_of_measurment)

            if key == 'sample_rate':
                sample_rate = match.group('sample_rate')
                sample_rate = float(sample_rate)
                print("found sample rate: ", str(sample_rate))

            if key == 'duration':
                duration = match.group('duration')
                duration = float(duration)
                print("found duration: ", str(duration))
            
            if key == 'number_of_samples':
                nsamples = match.group('nsamples')
                nsamples = int(nsamples)
                print("found number of samples: ", str(nsamples))
            
            if key == 'description':
                #parsing of description
                print("Description is not implemented")
            
            if key == 'light_source_wavelengths':
                print("found light_source_wavelengths")
                # read legend line (device, index, wavelengths) we dont need it
                line= file_object.readline()
                line= file_object.readline()
                while line.strip():
                    device, index, wavelengths, nm = line.strip().split('\t')
                    row = {
                        'device': int(device),
                        'index': int(index),
                        'wavelengths': int(wavelengths)
                    }
                    light_source_wavelengths_data.append(row)
                    line = file_object.readline()

            if key == 'legend':
                print("found legend")
                # read legend line we dont need it
                line = file_object.readline()
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip().split('\t')
                while (len(line) > 2):
                    column,	trace,	start,	end = line
                    row = {
                        'Trace (Measurement)': trace,
                        'Start': int(start),
                        'End':int(end)
                    }
                    legend_data.append(row)
                    line = file_object.readline()
                    line = line.strip().split('\t')

            if key == 'data':
                print("found data")
                # read legend line we dont need it
                line = file_object.readline()
                while line.strip():
                    data_line = line.strip().split('\t')
                    data.append(data_line)
                    line = file_object.readline()
            line = file_object.readline()
                




    # create a pandas DataFrame from the list of dicts
    light_source_wavelengths_data = pd.DataFrame(light_source_wavelengths_data)
    legend_data = pd.DataFrame(legend_data)
    data = pd.DataFrame(data)
    events =  data[data.columns[[len(data.columns)-2,len(data.columns)-1]]]
    print(events)
    print(events.index[16994].value)
    events = events.index[events[events.columns[0]] == event_type].tolist()
    
    data = data.drop(data.columns[[0, len(data.columns)-2, len(data.columns)-1]], axis=1)
    

    data.columns = legend_data['Trace (Measurement)']
    data = data.astype(float)

    return data, light_source_wavelengths_data, legend_data,events

def print_plot_two_chanel(data,index,if_events = False,events = []):
    if (index > -1) and index < (len(data.columns)-1):
        plt.suptitle('Graph')
        ax1 = plt.subplot(1,1,1)
        
        OHb = data[data.columns[index]].values.tolist()
        ax1.plot(OHb,color="red",label=data.columns[index])
        HHb = data[data.columns[index+1]].values.tolist()
        ax1.plot(HHb,color="blue",label=data.columns[index+1])
        difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
        ax1.plot(difference,color="black",label="difference")
        if if_events:
            for i in events:
                ax1.axvline(i,color = 'green')
        plt.legend()
        plt.show()
    else:
        print("index must be from 0 to ", len(data.columns)-1)

    
    # plt.figure()
    # plt.suptitle('Image Histogram ')
    # for i in range(0, len(data.columns)-1, 2):
    #     ax1 = plt.subplot(len(data.columns),1,i+1)
    #     ax1.plot(data[data.columns[i]],color="blue",label=data.columns[i])
    #     ax1.plot(data[data.columns[[i+1]]],color="red",label=data.columns[i+1])
    #     difference = data.apply(lambda x: x[data.columns[i+1]] - x[data.columns[[i]]], axis=1)
    #     ax1.plot(difference,color="black",label="difference")

def print_events(events):
        plt.suptitle('Events ')
        for i in events:
            print(i)
            plt.axvline(i,color = 'green',label = "events")
        plt.legend()
        plt.show()
        
    # for i in events.columns:
    #     print(i)
    #     if i == 'C1':
    #         # print(i)
    #         ax1.axvline(i.index('C1'),color = 'green',label = "events")
        # event_list = events[events.columns[0]].values.tolist()
    # # print(event_list.index('C1'))
    # print(events.iloc[17124,0])
    # print(event_list)


def genegate_average_values(data,events):
    chanel_list = []
    for j in range(0, len(data.columns)):
        pred_event = 0
        events_list = []
        for i in events:
            tmp = data.loc[pred_event:i,data.columns[j]]
            value = tmp.mean()
            # print('from ',pred_event,' to ', i , ' average value on ', data.columns[j], ' = ',value)
            events_list.append(value)
            pred_event = i
        tmp = data.loc[pred_event:len(data.index),data.columns[j]]
        value = tmp.mean()
        # print('from ',pred_event,' to ', len(data.index) , ' average value on ', data.columns[j], ' = ',value)
        events_list.append(value)
        chanel_list.append(events_list)
    
    average = pd.DataFrame(chanel_list)
    average = average.transpose()
    average.columns = data.columns
    return average

def print_average_stairs(average,index,edges_for_events):
    plt.figure()
    plt.suptitle('Average values')
    ax1 = plt.subplot(1,1,1)

    OHb = average[average.columns[index]].values.tolist()
    ax1.stairs(OHb,color="red",label=average.columns[index],baseline=None,edges = edges_for_events)

    HHb = average[average.columns[index+1]].values.tolist()
    ax1.stairs(HHb,color="blue",label=average.columns[index+1],baseline=None,edges = edges_for_events)

    difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
    ax1.stairs(difference,color="black",label="difference",baseline=None,edges = edges_for_events)
    plt.legend()
    plt.show()

def main():
    print('--Parsing fnirs file--')
    filepath = 'eotest.txt'
    event_type = "C1"
    data, light_source_wavelengths_data, legend_data, events = fnirs_parser(filepath, event_type)

    # print(light_source_wavelengths_data.head(5))

    # print(legend_data.head(5))

    # print(data.head(5))

    print_plot_two_chanel(data,0)
    print_events(events)

    print_plot_two_chanel(data,2, if_events=True, events=events)

    # plt.figure()
    # for i in range(0, len(data.columns)-1, 2):
    #     print_plot_two_chanel(data,i)

    
    average = genegate_average_values(data,events)
    print(average.head(5))

    edges_for_events = events
    edges_for_events.insert(0,0)
    edges_for_events.append(len(data.index))

    print_average_stairs(average,0,edges_for_events)
    # for i in range(0, len(average.columns)-1, 2):
    #     print_average_stairs(average,i,edges_for_events)

    

    # data_copy = data.copy().transpose()
    # print(data_copy.head(5))
    
if __name__ == "__main__":
    main()
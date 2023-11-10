import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
class fnirs:
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
    def __init__(self,filepath = "",event_type = ["test"],print_log = False) -> None:
        self.file_name = ""
        self.data = []  # create an empty list to collect the data
        self.light_source_wavelengths_data = []
        self.legend_data = []
        self.events = []
        self.edges_for_events = []
        self.average = []
        self.sample_rate = 0
        if (filepath != ""):
            self.fnirs_parser(filepath,event_type,print_log)
    # def __init__(self,name,dataframe):
    #     self.name = name
    #     self.data = dataframe
    #     self.legend_data = []
    #     self.events = []
    #     self.average = []

    def copy(self):
        result = fnirs()
        result.file_name = self.file_name
        result.data = self.data.copy()
        result.light_source_wavelengths_data = self.light_source_wavelengths_data.copy()
        result.legend_data = self.legend_data.copy()
        result.events = self.events
        result.average = self.average.copy()
        result.edges_for_events = self.edges_for_events.copy()
        result.sample_rate = self.sample_rate
        return result
    
    def export(self,path = ""):
        # self.average.to_excel(path + self.file_name + "output.xlsx")
        self.average.to_csv(path + self.file_name + "output.csv",index=False) 

    def _parse_line(self,line):

        for key, rx in self.rx_dict.items():
            match = rx.search(line)
            if match:
                return key, match
        # if there are no matches
        return None, None
    
    def fnirs_parser(self,filepath,event_type = ["test"],print_log = False):
        # open the file and read through it line by line
        with open(filepath, 'r') as file_object:
            line = file_object.readline()
            while line:
                # at each line check for a match with a regex
                key, match = self._parse_line(line)

                if key == 'export_of':
                    export_path = match.group('export')
                    if(print_log):
                        print("found export path: " + export_path)

                if key == 'export_date':
                    export_data = match.group('export_date')
                    if(print_log):
                        print("found export data: " + export_data)
                
                if key == 'start_of_measurment':
                    start_of_measurment = match.group('start_of_measurment')
                    if(print_log):
                        print("found start of measurment: " + start_of_measurment)

                if key == 'sample_rate':
                    sample_rate = match.group('sample_rate')
                    self.sample_rate = float(sample_rate)
                    if(print_log):
                        print("found sample rate: ", str(sample_rate))

                if key == 'duration':
                    duration = match.group('duration')
                    duration = float(duration)
                    if(print_log):
                        print("found duration: ", str(duration))
                
                if key == 'number_of_samples':
                    nsamples = match.group('nsamples')
                    nsamples = int(nsamples)
                    if(print_log):
                        print("found number of samples: ", str(nsamples))
                
                if key == 'description':
                    #parsing of description
                    if(print_log):
                        print("Description is not implemented")
                
                if key == 'light_source_wavelengths':
                    if(print_log):
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
                        self.light_source_wavelengths_data.append(row)
                        line = file_object.readline()

                if key == 'legend':
                    if(print_log):
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
                        self.legend_data.append(row)
                        line = file_object.readline()
                        line = line.strip().split('\t')

                if key == 'data':
                    if(print_log):
                        print("found data")
                    # read legend line we dont need it
                    line = file_object.readline()
                    while line.strip():
                        data_line = line.strip().split('\t')
                        self.data.append(data_line)
                        line = file_object.readline()
                line = file_object.readline()

        filepath = filepath.split('/')
        self.file_name = filepath[len(filepath)-1]
        # create a pandas DataFrame from the list of dicts
        self.light_source_wavelengths_data = pd.DataFrame(self.light_source_wavelengths_data)
        self.legend_data = pd.DataFrame(self.legend_data)
        self.data = pd.DataFrame(self.data)
        self.data = self.data.drop(self.data.columns[[0]], axis=1)
        # self.events = self.data[self.data.columns[[len(self.data.columns)-1]]]
        self.events = self.data[self.data.columns[[len(self.legend_data)]]]
        event_tmp = []
        for i in range (0,len(event_type)):
            event_tmp = event_tmp + self.events.index[self.events[self.events.columns[0]] == event_type[i]].tolist() 
        self.events = event_tmp
        # if event_type!='fon':
        #  self.events = self.events.index[self.events[self.events.columns[0]] == event_type].tolist()   
        # else:
        #     self.events = self.events.index[self.events[self.events.columns[0]] == 'O1'].tolist() + self.events.index[self.events[self.events.columns[0]] == 'C1'].tolist()
        
        
        while len(self.data.columns) != len(self.legend_data):
            self.data = self.data.drop(self.data.columns[[len(self.data.columns)-1]], axis=1) #if we have none columns
        self.data.columns = self.legend_data['Trace (Measurement)']
        self.data = self.data.astype(float)

        self.edges_for_events = self.events.copy()
        self.edges_for_events.insert(0,0)
        self.edges_for_events.append(len(self.data.index))

    def normalize_data(self):
        # self.data = (self.data-self.data.mean())/self.data.std()
        self.data =(self.data-self.data.min())/(self.data.max()-self.data.min())

    def print_plot_two_chanel(self,index,if_events = False):
        if (index > -1) and index < (len(self.data.columns)-1):
            plt.suptitle('Graph '+self.file_name)
            ax1 = plt.subplot(1,1,1)
            
            OHb = self.data[self.data.columns[index]].values.tolist()
            ax1.plot(OHb,color="red",label=self.data.columns[index])
            HHb = self.data[self.data.columns[index+1]].values.tolist()
            ax1.plot(HHb,color="blue",label=self.data.columns[index+1])
            difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
            ax1.plot(difference,color="black",label="difference")
            if if_events:
                for i in self.events:
                    ax1.axvline(i,color = 'green')
            plt.legend()
            plt.show()
        else:
            print("index must be from 0 to ", len(self.data.columns)-1)
    
    def print_events(self):
        plt.suptitle('Events ' + self.file_name)
        for i in self.events:
            print(i)
            plt.axvline(i,color = 'green',label = "events")
        plt.legend()
        plt.show()

    def genegate_average_values(self):
        chanel_list = []
        for j in range(0, len(self.data.columns)):
            pred_event = 0
            events_list = []
            for i in self.events:
                tmp = self.data.loc[pred_event:i,self.data.columns[j]]
                value = tmp.mean()
                # print('from ',pred_event,' to ', i , ' average value on ', self.data.columns[j], ' = ',value)
                events_list.append(value)
                pred_event = i
            tmp = self.data.loc[pred_event:len(self.data.index),self.data.columns[j]]
            value = tmp.mean()
            # print('from ',pred_event,' to ', len(self.data.index) , ' average value on ', self.data.columns[j], ' = ',value)
            events_list.append(value)
            chanel_list.append(events_list)
        
        self.average = pd.DataFrame(chanel_list)
        self.average = self.average.transpose()
        self.average.columns = self.data.columns

    def print_average_stairs(self,index):
        plt.figure()
        plt.suptitle('Average values ' + self.file_name)
        ax1 = plt.subplot(1,1,1)

        # print(self.edges_for_events)

        OHb = self.average[self.average.columns[index]].values.tolist()
        ax1.stairs(OHb,color="red",label=self.average.columns[index],baseline=None,edges = self.edges_for_events)

        HHb = self.average[self.average.columns[index+1]].values.tolist()
        ax1.stairs(HHb,color="blue",label=self.average.columns[index+1],baseline=None,edges = self.edges_for_events)

        difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
        ax1.stairs(difference,color="black",label="difference",baseline=None,edges = self.edges_for_events)
        plt.legend()
        plt.show()

    def compare_easy(self,second,mode):
        result = self.copy()
        result.file_name = result.file_name + " & " + second.file_name
        for i in range(0,len(self.average)-1):
            for j in range(0,len(self.average.columns)-1):
                result.average.iloc[i,j] = self.average.iloc[i,j] * mode[0] + second.average.iloc[i,j] * mode[1]
        return result
    def create_filtered(self):
        b, a = signal.butter(8, [0.025,0.45], 'bandpass')   # Конфигурационный фильтр 8 указывает порядок фильтра
        filtered = signal.filtfilt(b, a, self.data)  # данные - это сигнал, который нужно отфильтровать
        tmp = self.copy()
        tmp.data = pd.DataFrame(filtered)
        tmp.data.columns = self.data.columns
        tmp.file_name = tmp.file_name + "_filtered"
        tmp.genegate_average_values()
        return tmp
    
    def filter(self): #filter data 
        sos = signal.butter(3,[0.01,0.09],btype='bandpass',output='sos',fs = self.sample_rate)
        result = pd.DataFrame()
        for i in range(0,len(self.data.columns)):
            
            what_filter = self.data[self.data.columns[i]].values.tolist()
            filtered = signal.sosfilt(sos, what_filter)  # данные - это сигнал, который нужно отфильтровать
            result.insert(i,self.data.columns[i],filtered)
        self.data = result

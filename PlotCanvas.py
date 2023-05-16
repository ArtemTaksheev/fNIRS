import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)


    def plot(self):
        data = ([0,1,2,3,4], [0,1,2,3,4])
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def print_plot_two_chanel(self,fnirs,index,if_events = False):
        self.axes.cla()
        if (index > -1) and index < (len(fnirs.data.columns)-1):
            
            self.axes.set_title('Graph '+fnirs.file_name)
            
            OHb = fnirs.data[fnirs.data.columns[index]].values.tolist()
            self.axes.plot(OHb,color="red",label=fnirs.data.columns[index])
            HHb = fnirs.data[fnirs.data.columns[index+1]].values.tolist()
            self.axes.plot(HHb,color="blue",label=fnirs.data.columns[index+1])
            difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
            self.axes.plot(difference,color="black",label="difference")
            if if_events:
                for i in fnirs.events:
                    self.axes.axvline(i,color = 'green')
            self.axes.legend()
            self.draw()
        else:
            print("index must be from 0 to ", len(fnirs.data.columns)-1)
    
    def print_events(self,fnirs):
        plt.suptitle('Events ' + fnirs.file_name)
        for i in fnirs.events:
            print(i)
            plt.axvline(i,color = 'green',label = "events")
        plt.legend()
        plt.show()

    
    def print_average_stairs(self,fnirs,index):
        self.axes.set_title('Average values ' + fnirs.file_name)

        # print(self.edges_for_events)

        OHb = fnirs.average[fnirs.average.columns[index]].values.tolist()
        self.axes.stairs(OHb,color="red",label=fnirs.average.columns[index],baseline=None,edges = fnirs.edges_for_events)

        HHb = fnirs.average[fnirs.average.columns[index+1]].values.tolist()
        self.axes.stairs(HHb,color="blue",label=fnirs.average.columns[index+1],baseline=None,edges = fnirs.edges_for_events)

        difference = [OHb[i]-HHb[i] for i in range(0,len(OHb))]
        self.axes.stairs(difference,color="black",label="difference",baseline=None,edges = fnirs.edges_for_events)
        self.axes.legend()
        self.draw()
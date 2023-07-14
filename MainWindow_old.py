from PyQt5.QtWidgets import *
import sys

import design_old as design # design of main window

from fnirs import fnirs

class MainWindow(QMainWindow, design.Ui_MainWindow): # main window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.data = []

        self.load_button.clicked.connect(self.load_file)
        self.data_load_button.clicked.connect(self.data_visualise)
        self.average_button.clicked.connect(self.average_visualise)
        self.export_button.clicked.connect(self.export_data)

    def export_data(self):
        self.data.export()

    def load_file(self):
        fileName = QFileDialog.getOpenFileName(self,
                "Open Image", "/home/vcpt", "Image Files (*.txt)")
        if fileName[0]:
            self.data = fnirs(fileName[0],"T1")
            # self.data.fnirs_parser(fileName[0],"T1")
            print("Load data succesffully")
            print(fileName[0])
        
    def data_visualise(self):
        self.sc.axes.cla()
        self.sc.print_plot_two_chanel(self.data,0)
        self.sc.draw()
    def average_visualise(self):
        self.data.genegate_average_values()
        print("Average value generated")
        self.sc.axes.cla()
        self.sc.print_average_stairs(self.data,0)
        self.sc.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window = MainWindow() 
    window.show()  
    app.exec_()  
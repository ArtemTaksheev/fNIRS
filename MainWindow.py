from PyQt5.QtWidgets import *
import sys

import project as project # design of main window

from patient_fnirs import patient_fnirs

class MainWindow(QMainWindow, project.Ui_MainWindow): # main window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.patients = []
        self.currentPatient = 0
        self.currentChannel = 0
        self.currentFon = ""
        self.currentConditions = []
        self.currentConditionsIndex = 0
        self.plotType = "raw"
        self.data = []
        # main buttons
        self.vButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.gButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        # patient Widget
        self.fonFileButton.clicked.connect(lambda: self.load_file("fon"))
        self.addPatientsFile.clicked.connect(lambda: self.load_file("vcpt"))
        self.addPatient.clicked.connect(lambda: self.add_patient())

        # visualize Widget
        self.showRawButton.clicked.connect(lambda: self.data_visualise(0,"raw"))
        self.showAverage.clicked.connect(lambda: self.data_visualise(0,"aver"))
        self.vPComboBox.currentIndexChanged.connect(self.update_current_patient)
        self.update_current_patient(self.vPComboBox.currentIndex())
        self.resComboBox.currentIndexChanged.connect(self.update_current_condition)
        self.update_current_condition(self.resComboBox.currentIndex())
        self.prevChannel.clicked.connect(lambda: self.show_prev_channel())
        self.nextChannel.clicked.connect(lambda: self.show_next_channel())
        self.compareButton.clicked.connect(lambda: self.compare())
        self.exportButton.clicked.connect(lambda: self.export_data())

    def update_current_patient(self,index):
        if self.patients:   
            self.currentPatient = index
            self.currentConditionsIndex = 0
            self.resComboBox.clear()
            # self.resComboBox.addItem(self.patients[self.currentPatient].data[0].file_name)
            for i in self.patients[self.currentPatient].data:
                self.resComboBox.addItem(i.file_name)
                # add to compare cBox
                self.firstResearchComboBox.addItem(i.file_name)
                self.secondResearchComboBox.addItem(i.file_name)
            # self.data_visualise(self.currentConditionsIndex,self.plotType)

    def update_current_condition(self,index):
        if self.patients:
            self.currentConditionsIndex = index
            self.data_visualise(self.currentConditionsIndex,self.plotType)

    def show_prev_channel(self):
        if self.currentChannel:
            self.currentChannel = self.currentChannel - 2
            self.data_visualise(self.currentChannel,self.plotType)
    def show_next_channel(self):
         if self.currentChannel < len(self.patients[self.currentPatient].data[self.currentConditionsIndex].data) - 1:
            self.currentChannel = self.currentChannel + 2
            self.data_visualise(self.currentChannel,self.plotType)

    def compare(self):
        self.patients[self.currentPatient].compare_easy(self.firstResearchComboBox.currentIndex(),self.secondResearchComboBox.currentIndex())
        self.resComboBox.addItem(self.patients[self.currentPatient].get_last_data().file_name)
        self.data_visualise(self.currentChannel,self.plotType)
        self.statusbar.showMessage("Compare succesffully")
        
    def export_data(self):
        # path = QFileDialog.getSaveFileName(self,"Save results","/results",)
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.patients[self.currentPatient].export(folderpath)
        self.statusbar.showMessage("Export was succesffull")


    def load_file(self,type):
        fileName = QFileDialog.getOpenFileNames(self,
                "Open Image", "/home/vcpt", "Image Files (*.txt)")
        if fileName[0]:
            if type == "fon":
                self.currentFon = fileName[0][0]
                print("Get fon path succesffully")
            if type == "vcpt":
                self.currentConditions.clear()
                self.currentConditions = fileName[0]
                print("Get conditions path succesffully")
            print(fileName[0])

    def add_patient(self):
        self.statusbar.clearMessage()
        patient = patient_fnirs(self.patientsName.text(),self.currentFon,self.currentConditions)
        self.patientsName.setText('')
        self.patients.append(patient)
        self.currentPatient = len(self.patients)-1
        self.statusbar.showMessage("Patient added succesffully")
        for i in self.patients[self.currentPatient].data:
            i.genegate_average_values()
        self.vPComboBox.addItem(patient.patient_name)

    def data_visualise(self,chanel,type):
        self.plot.axes.cla()
        if type == "raw":
            self.plotType = "raw"
            self.plot.print_plot_two_chanel(self.patients[self.currentPatient].data[self.currentConditionsIndex],chanel)
            if self.stackedWidget.currentIndex() == 0:
                self.statusbar.showMessage("Showing raw data")
        if type == "aver":
            self.plotType = "aver"
            self.plot.print_average_stairs(self.patients[self.currentPatient].data[self.currentConditionsIndex],chanel)
            self.statusbar.showMessage("Show average data")
        self.plot.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window = MainWindow() 
    window.show()  
    app.exec_()  
import mne
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os   
def read_raw_data():
    plt.switch_backend('QtAgg')
    plt.ion() #Makes plot interactive
    raw = mne.io.read_raw_edf("eeg.edf", stim_channel='Event marker',
                                    misc=['Temp rectal'],preload=True)

    # annot_train = mne.read_annotations("eeg.edf")
    # raw_train.set_annotations(annot_train, emit_warning=False)

    # plot some data
    # scalings were chosen manually to allow for simultaneous visualization of
    # different channel types in this specific dataset
    raw.plot(start=0, duration=60,
                scalings=dict(eeg=1e-4, resp=1e3, eog=1e-4, emg=1e-7,
                                misc=1e-1))

    
def main():
    read_raw_data()

if __name__ == "__main__":
    main()
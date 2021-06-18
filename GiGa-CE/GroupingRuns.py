import numpy as np
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

class groupingwindow():
    def __init__(self, parent):
        """
        Calls start to open new window
        """
        self.num_samples = 4 # may get changed later
        self.num_time_analyzed_per_sample = 3 # may get changed later
        self.parent = parent
        self.start()
    
    def start(self):
        self.app = Grouping(self)
        self.app.mainloop()

    def close(self):
        # may rewrite this to pass back information
        #self.parent.volume = self.volume
        self.app.destroy()
        return

class Grouping(tk.Tk):
    """
    Helps with populating grouping window
    """
    def __init__(self, parent,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Populate all the main windows this program will display
        frame = grouping_info(container, self, parent)
        self.frames[grouping_info] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        

        self.show_frame(grouping_info)
    
    def show_frame(self, cont):
        """Moves the frame of interest to the top"""
        
        frame = self.frames[cont]
        frame.tkraise()


class grouping_info(tk.Frame):
    """
    similar to hydrostatic class in Injection.py
    """
    def __init__(self, parent, controller, starter):
        """
        Asks number of samples,
        number of times analyzed per sample
        """
        self.starter=starter
        tk.Frame.__init__(self,parent) # initialize frame

        num_samples_label = Label(self, text = "Number of Samples: ")
        num_samples_label.grid()
        self.num_samples_edit= Spinbox(self)
        self.num_samples_edit.grid()
        self.num_samples_edit.bind('<FocusOut>', self.on_focusout)

        num_times_analyzed_per_sample_label=Label(self, text = "Number of Times Analyzed Per Sample: ")
        num_times_analyzed_per_sample_label.grid()
        self.num_times_analyzed_per_sample_edit=Spinbox(self)
        self.num_times_analyzed_per_sample_edit.grid()
        self.num_times_analyzed_per_sample_edit.bind('<FocusOut>', self.on_focusout)

        # add another button for selecting a grouping
        self.fileselection=Button(self, text = "Select Files in Group", command=self.select_files)
        self.fileselection.grid()

        self.submit=Button(self, text = "Submit", command = starter.close)
        self.submit.grid()
    
    def on_focusout(self,event):
        """Saves edits and can do calculations of grouping matrix in here (self.group_assignments)"""
        if self.num_samples_edit.get() != '':
            self.num_samples = int(float(self.num_samples_edit.get()))
        if self.num_times_analyzed_per_sample_edit.get() != '':
            self.num_times_analyzed_per_sample = int(float(self.num_times_analyzed_per_sample_edit.get()))
        
        if self.num_samples_edit.get() != '' and self.num_times_analyzed_per_sample_edit.get() != '':
            # later change to the number of files imported
            num_runs = self.num_samples * self.num_times_analyzed_per_sample

            # set up num_times_analyzed_per_sample x num_samples array
            self.group_assignments = np.zeros([self.num_times_analyzed_per_sample, self.num_samples])

            # make array of the position in the group for each file number
            num_in_group_array = list()
            for i in range(self.num_times_analyzed_per_sample):
                for j in range(self.num_samples):
                    num_in_group_array.append(i)

            # loop through each file number and assign to group
            for file_num in range(num_runs):
                # find group the file number should be assigned to
                group = file_num % self.num_samples

                # find the position in that group
                num_in_group = num_in_group_array[file_num]

                # fill in group array with this file number
                self.group_assignments[num_in_group, group] = file_num
            # take print statement out eventually
            print(self.group_assignments)

    def select_files(self):
        """allows user to select the files in a group
        might have issues with selecting all in one window"""
        pass

'''        
num_samples = 4
num_times_analyzed_per_sample = 3

# later change to the number of files imported
num_runs = num_samples * num_times_analyzed_per_sample

# set up num_times_analyzed_per_sample x num_samples array
group_assignments = np.zeros([num_times_analyzed_per_sample, num_samples])

# make array of the position in the group for each file number
num_in_group_array = list()
for i in range(num_times_analyzed_per_sample):
    for j in range(num_samples):
        num_in_group_array.append(i)

# loop through each file number and assign to group
for file_num in range(num_runs):
    # find group the file number should be assigned to
    group = file_num % num_samples

    # find the position in that group
    num_in_group = num_in_group_array[file_num]

    # fill in group array with this file number
    group_assignments[num_in_group, group] = file_num
print(group_assignments)

# example of extracting file number from name
# assumes csv file (or other filie with 3 character code)
file_name = '20210204 sf s1pf standards_00001.csv'
split_name = file_name.split('.')
name_without_type = split_name[0]
five_digit_number = name_without_type[len(name_without_type)-5:len(name_without_type)]
file_num = int(five_digit_number)
print(file_num)

index = np.where(group_assignments==file_num)
index_num_times_analyzed_per_sample = int(index[0])
index_num_samples = int(index[1])
print(index_num_samples) # remember 0 based indexing!!
# name = name of 1st in column + (row + 1)
'''
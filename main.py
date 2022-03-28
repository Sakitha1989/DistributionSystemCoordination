######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# Need two command line inputs;
#           1. Directory path
#           2. System name
#
# The script assumes that there are 'inputData' and 'outputData' folders exist inside the directory. Also, inside the
# 'inputData' folder there must be folder for the system containing all the data files.

# VOLL has set to 1000
# max flow on lines has set 99999
# base value for conductance and susceptance has set to 10000

import numpy as np
import numpy.random

from GUI import *

np.random.seed(10)

# global variables
directory = ""
network_name = ""
system_name = ""
num_systems = 0
num_iterations = 300
input_dir = ""
output_dir = ""


# main frame
root = tk.Tk()
root.title("Exchange Electricity")
root.iconbitmap(r"images/appIcon.ico")
root.geometry("900x500")
root.config(bg="#80c1ff")

main_frame(root)

button_exit = tk.Button(root, text="Exit", command=root.quit, bg="white", fg="black")
button_exit.place(relx=0.9, rely=.93, relwidth=0.08, relheight=0.05)


root.mainloop()

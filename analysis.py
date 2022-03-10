######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/01/2022
# Project:  Distribution system coordination
######################################################################################################################

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
# import plotly.express as px
# import plotly


def display_graphs():
    def create_plot():
        out_dir = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\outputData\\IEEE\\"

        system_data = pd.read_csv(out_dir + 'IEEE1.csv')

        plt.plot(system_data['Objective_Function_Value'])
        plt.grid(True)
        return plt.gcf()

        # x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # fig = px.line(system_data, x=x, y="Objective_Function_Value", title='Objective function value')
        # plotly.offline.plot(fig, filename='file.html')
        # fig.show()

    graph_layout = [
        [sg.Text('Graph')],
        [sg.Canvas(key="-CANVAS-")],
        [sg.Exit()]
    ]

    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    graph_window = sg.Window("Graph", graph_layout, finalize=True, element_justification='center')

    draw_figure(graph_window['-CANVAS-'].TKCanvas, create_plot())

    while True:
        event, value = graph_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    graph_window.close()

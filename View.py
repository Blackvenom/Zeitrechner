import tkinter as tk
from tkinter import ttk

class View(ttk.Frame):

    _text_title="Zeitrechner"
    _text_StartTime="Kommen-Zeit [hh:mm]"
    _text_LeaveTime="Gehen-Zeit [hh:mm]"
    _text_WorkingTime="Arbeits-Zeit [hh:mm]"

    _string_StartTime = ""
    _string_LeaveTime = ""
    _string_WorkingTime = ""

    def set_controller(self, controller):
        self.controller = controller

    def entryFocusLost(self, event):
        #get text from correct entry
        if(self.controller):
            _string_EntryTime = ""
            if(event.widget._name == 'startEntry'): _string_EntryTime = _string_StartTime.get()
            elif(event.widget._name == 'leaveEntry'): _string_EntryTime = _string_LeaveTime.get()
            elif(event.widget._name == 'workingEntry'): _string_EntryTime = _string_WorkingTime.get()

            #check if entered values are in correct format
            self.controller.checkEntryTime(event.widget._name, _string_EntryTime)

            #check which calculation mode is needed
            self.controller.checkCalcuationMethod(_string_StartTime.get(), _string_LeaveTime.get(), _string_WorkingTime.get())

    def __init__(self, parent):
        super().__init__(parent)

        #root window
        parent.geometry('460x400')
        parent.resizable(False, False)
        parent.title(self._text_title)

        global _string_StartTime
        global _string_LeaveTime
        global _string_WorkingTime
        _string_StartTime = tk.StringVar()
        _string_LeaveTime = tk.StringVar()
        _string_WorkingTime = tk.StringVar()

        #label: StartTime
        self.label_StartTime = ttk.Label(parent, text=self._text_StartTime)
        self.label_StartTime.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        #label: LeaveTime
        self.label_LeaveTime = ttk.Label(parent, text=self._text_LeaveTime)
        self.label_LeaveTime.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        #label: WorkingTime
        self.label_WorkingTime = ttk.Label(parent, text=self._text_WorkingTime)
        self.label_WorkingTime.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        #entry: StartTime
        self.entry_StartTime = ttk.Entry(parent, textvariable=_string_StartTime, name='startEntry')
        self.entry_StartTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_StartTime.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        #entry: LeaveTime
        self.entry_LeaveTime = ttk.Entry(parent, textvariable=_string_LeaveTime, name='leaveEntry')
        self.entry_LeaveTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_LeaveTime.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        #entry: WorkingTime
        self.entry_WorkingTime = ttk.Entry(parent, textvariable=_string_WorkingTime, name='workingEntry')
        self.entry_WorkingTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_WorkingTime.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.controller = None

    def show_success(self, control):
        if(control == 'startEntry'):
            self.entry_StartTime['foreground'] = 'green'
        elif(control == 'leaveEntry'):
            self.entry_LeaveTime['foreground'] = 'green'
        elif(control == 'workingEntry'):
            self.entry_WorkingTime['foreground'] = 'green'

    def show_error(self, control):
        if(control == 'startEntry'):
            self.entry_StartTime['foreground'] = 'red'
        elif(control == 'leaveEntry'):
            self.entry_LeaveTime['foreground'] = 'red'
        elif(control == 'workingEntry'):
            self.entry_WorkingTime['foreground'] = 'red'
    
    def show_time(self, control, value):
        if(control == 'startEntry'):
            global _string_StartTime
            _string_StartTime.set(value)
        elif(control == 'leaveEntry'):
            global _string_LeaveTime
            _string_LeaveTime.set(value)
        elif(control == 'workingEntry'):
            global _string_WorkingTime
            _string_WorkingTime.set(value)
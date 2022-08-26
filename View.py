import tkinter as tk
from tkinter import ACTIVE, DISABLED, ttk

class View(ttk.Frame):

    _text_title="Zeitrechner"
    _text_StartTime="Kommen-Zeit [hh:mm]"
    _text_LeaveTime="Gehen-Zeit [hh:mm]"
    _text_WorkingTime="Arbeits-Zeit [hh:mm]"
    _text_BreakTime="Pausen-Zeit [hh:mm]"
    _text_ErrResultNegative="Berechnete Zeit ist negativ. Bitte angegebene Zeiten überprüfen."
    _text_ErrInvalidTime="Ungültige Zeit. Bitte angegebene Zeit überprüfen."

    _string_StartTime = ""
    _string_LeaveTime = ""
    _string_WorkingTime = ""
    _string_BreakTime = ""
    _string_Status = ""

    def __init__(self, parent):
        super().__init__(parent)

        #root window
        parent.geometry('420x155')
        parent.resizable(False, False)
        parent.title(self._text_title)
        parent.columnconfigure((0,1), weight=1)

        global _string_StartTime
        global _string_LeaveTime
        global _string_WorkingTime
        global _string_BreakTime
        global _string_Status
        _string_StartTime = tk.StringVar()
        _string_LeaveTime = tk.StringVar()
        _string_WorkingTime = tk.StringVar()
        _string_BreakTime = tk.StringVar()
        _string_Status = tk.StringVar()
        _string_BreakTime.set("00:50")

        #label: StartTime
        self.label_StartTime = ttk.Label(parent, text=self._text_StartTime, font='CorpoA 11')
        self.label_StartTime.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        #label: LeaveTime
        self.label_LeaveTime = ttk.Label(parent, text=self._text_LeaveTime, font='CorpoA 11')
        self.label_LeaveTime.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        #label: WorkingTime
        self.label_WorkingTime = ttk.Label(parent, text=self._text_WorkingTime, font='CorpoA 11')
        self.label_WorkingTime.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        #label: BreakTime
        self.label_BreakTime = ttk.Label(parent, text=self._text_BreakTime, font='CorpoA 11')
        self.label_BreakTime.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        #label: Status
        self.label_Status = ttk.Label(parent, textvariable=_string_Status, font='CorpoA 11')
        self.label_Status.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5, columnspan=2)
        self.label_Status['foreground'] = 'red'

        #entry: StartTime
        self.entry_StartTime = ttk.Entry(parent, textvariable=_string_StartTime, name='startEntry', width=10)
        self.entry_StartTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_StartTime.grid(column=1, row=0, padx=5, pady=5)

        #entry: LeaveTime
        self.entry_LeaveTime = ttk.Entry(parent, textvariable=_string_LeaveTime, name='leaveEntry', width=10)
        self.entry_LeaveTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_LeaveTime.grid(column=1, row=1, padx=5, pady=5)

        #entry: WorkingTime
        self.entry_WorkingTime = ttk.Entry(parent, textvariable=_string_WorkingTime, name='workingEntry', width=10)
        self.entry_WorkingTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_WorkingTime.grid(column=1, row=2, padx=5, pady=5)

        #entry: BreakTime
        self.entry_BreakTime = ttk.Entry(parent, textvariable=_string_BreakTime, name='breakEntry', width=10)
        self.entry_BreakTime.bind('<FocusOut>', self.entryFocusLost)
        self.entry_BreakTime.grid(column=1, row=3, padx=5, pady=5)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def show_status(self, status):
            # set status text
            global _string_Status
            if(status == 'NoErr'):
                _string_Status.set("")
            elif(status == 'ErrResultNegative'):
                _string_Status.set(self._text_ErrResultNegative)
            elif(status == 'ErrInvalidTime'):
                _string_Status.set(self._text_ErrInvalidTime)

    def errorFree(self):
        if(str(self.entry_StartTime['foreground']) == 'red' or
           str(self.entry_LeaveTime['foreground']) == 'red' or
           str(self.entry_WorkingTime['foreground']) == 'red'):
            return False
        else:
            self.show_status("NoErr")
            return True

    def entryFocusLost(self, event):
        # get text from correct entry
        if(self.controller):
            _string_EntryTime = ""
            if(event.widget._name == 'startEntry'): _string_EntryTime = _string_StartTime.get()
            elif(event.widget._name == 'leaveEntry'): _string_EntryTime = _string_LeaveTime.get()
            elif(event.widget._name == 'workingEntry'): _string_EntryTime = _string_WorkingTime.get()
            elif(event.widget._name == 'breakEntry'): _string_EntryTime = _string_BreakTime.get()

            # check if entered values are in correct format
            self.controller.checkEntryTime(event.widget._name, _string_EntryTime)
            
            if(self.errorFree()):
                # check which calculation mode is needed
                self.controller.doStateMachineMagic(_string_StartTime.get(), _string_LeaveTime.get(), _string_WorkingTime.get(), _string_BreakTime.get())
                # calculate the needed time
                self.controller.calculateTime()

    def reset_labels(self):
        # reset to non-bold labels
        self.label_StartTime.configure(font='CorpoA 11')
        self.label_LeaveTime.configure(font='CorpoA 11')
        self.label_WorkingTime.configure(font='CorpoA 11')

    def highlight_label(self, control):
        self.reset_labels()

        if(control == 'startLabel'):
            self.label_StartTime.configure(font='CorpoA 11 bold')
        elif(control == 'leaveLabel'):
            self.label_LeaveTime.configure(font='CorpoA 11 bold')
        elif(control == 'workingLabel'):
            self.label_WorkingTime.configure(font='CorpoA 11 bold')

    def show_success(self, control):
        if(control == 'startEntry'):
            self.entry_StartTime['foreground'] = 'green'
        elif(control == 'leaveEntry'):
            self.entry_LeaveTime['foreground'] = 'green'
        elif(control == 'workingEntry'):
            self.entry_WorkingTime['foreground'] = 'green'
        elif(control == 'breakEntry'):
            self.entry_BreakTime['foreground'] = 'green'

    def show_error(self, control):
        if(control == 'startEntry'):
            self.entry_StartTime['foreground'] = 'red'
        elif(control == 'leaveEntry'):
            self.entry_LeaveTime['foreground'] = 'red'
        elif(control == 'workingEntry'):
            self.entry_WorkingTime['foreground'] = 'red'
        elif(control == 'breakEntry'):
            self.entry_BreakTime['foreground'] = 'red'

        self.show_status("ErrInvalidTime")
    
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
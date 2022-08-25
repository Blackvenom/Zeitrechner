import tkinter as tk
from tkinter import ttk
import Model, View, Controller

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
        
        

class Model:
    def __init__(self, breakHours, breakMinutes):
        self._intStartHours = self._intStartMinutes = 0
        self._intLeaveHours = self._intLeaveMinutes = 0
        self._intWorkingHours = self._intWorkingMinutes = 0
        self._intBreakHours = breakHours
        self._intBreakMinutes = breakMinutes

    @property
    def intStartHours(self):
        return self._intStartHours
    @intStartHours.setter
    def intStartHours(self, value):
        self._intStartHours = value

    @property
    def intStartMinutes(self):
        return self._intStartMinutes
    @intStartMinutes.setter
    def intStartMinutes(self, value):
        self._intStartMinutes = value

    @property
    def intLeaveHours(self):
        return self._intLeaveHours
    @intLeaveHours.setter
    def intLeaveHours(self, value):
        self._intLeaveHours = value

    @property
    def intLeaveMinutes(self):
        return self._intLeaveMinutes
    @intLeaveMinutes.setter
    def intLeaveMinutes(self, value):
        self._intLeaveMinutes = value

    @property
    def intWorkingHours(self):
        return self._intWorkingHours
    @intWorkingHours.setter
    def intWorkingHours(self, value):
        self._intWorkingHours = value

    @property
    def intWorkingMinutes(self):
        return self._intWorkingMinutes
    @intWorkingMinutes.setter
    def intWorkingMinutes(self, value):
        self._intWorkingMinutes = value

    @property
    def intBreakHours(self):
        return self._intBreakHours
    @intBreakHours.setter
    def intBreakHours(self, value):
        self._intBreakHours = value

    @property
    def intBreakMinutes(self):
        return self._intBreakMinutes
    @intBreakMinutes.setter
    def intBreakMinutes(self, value):
        self._intBreakMinutes = value

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def checkEntryTime(self, entry, strTime):
        try:
            if(strTime):
                hours = int(strTime[:2])
                minutes = int(strTime[3:])
                if(hours < 0 or hours > 23) or (minutes < 0 or minutes > 59):
                    self.view.show_error(entry)
                else:
                    self.view.show_success(entry)
                    self.storeEntryTime(entry, hours, minutes)
                    
        except:
            self.view.show_error(entry)

    def storeEntryTime(self, entry, hours, minutes):
        if(entry == 'startEntry'):
            self.model.intStartHours = hours
            self.model.intStartMinutes = minutes
        elif(entry == 'leaveEntry'):
            self.model.intLeaveHours = hours
            self.model.intLeaveMinutes = minutes
        elif(entry == 'workingEntry'):
            self.model.intWorkingHours = hours
            self.model.intWorkingMinutes = minutes

    def checkCalcuationMethod(self, _strStartTime, _strLeaveTime, _strWorkingTime):
        try:
            if( _strStartTime and not _strLeaveTime and _strWorkingTime):
                print('todo: Modus: Gehen-Zeit ermitteln')
            elif( _strStartTime and _strLeaveTime and not _strWorkingTime):
                #calculate working time
                self.getWorkingTime()
                #output working time
                
                self.view.show_time('workingEntry', f"{str(self.model.intWorkingHours).rjust(2, '0')}:{str(self.model.intWorkingMinutes).rjust(2, '0')}")
                
        except ValueError as error:
            self.view.show_error(error)
    
    def getWorkingTime(self):
        #Get all present minutes
        presentMinutes = (self.model.intLeaveHours - self.model.intStartHours)*60
        presentMinutes += self.model.intLeaveMinutes - self.model.intStartMinutes

        #remove minutes for reserved-break (50min)
        presentMinutes -= self.model.intBreakMinutes

        #store working-time in model
        self.model.intWorkingHours = int(presentMinutes / 60.0)
        self.model.intWorkingMinutes = presentMinutes-(self.model.intWorkingHours*60)
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Zeitrechner')

        # create a model (default break: 50min)
        model = Model(0, 50)

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
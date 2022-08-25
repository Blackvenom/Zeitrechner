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
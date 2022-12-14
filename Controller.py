class State():
    IDLE = 1
    STARTTIMEMODE = 2
    LEAVETIMEMODE = 3
    WORKINGTIMEMODE = 4

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.state = State.IDLE

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if(value == State.IDLE):
            self.view.reset_labels()
        elif(value == State.LEAVETIMEMODE):
            self.view.highlight_label('leaveLabel')
        elif(value == State.WORKINGTIMEMODE):
            self.view.highlight_label('workingLabel')
        elif(value == State.STARTTIMEMODE):
            self.view.highlight_label('startLabel')

        self._state = value

    def checkEntryTime(self, entry, strTime):
        try:
            if(strTime):
                # time-format 'hh:mm'
                if(':' in strTime and len(strTime) == 5):
                    hours = int(strTime[:2])
                    minutes = int(strTime[3:])
                # time-format 'hhmm'
                elif(len(strTime)==4):
                    hours = int(strTime[:2])
                    minutes = int(strTime[2:])

                    # apply new format to view
                    self.view.show_time(entry, f"{strTime[:2].rjust(2, '0')}:{strTime[2:].rjust(2, '0')}")

                # check for valid range
                if(hours < 0 or hours > 23) or (minutes < 0 or minutes > 59):
                    self.state = State.IDLE
                    self.view.show_error(entry)
                else:
                    self.view.show_success(entry)
                    self.storeEntryTime(entry, hours, minutes)
                    
        except:
            self.state = State.IDLE
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
        elif(entry == 'breakEntry'):
            self.model.intBreakHours = hours
            self.model.intBreakMinutes = minutes

    def doStateMachineMagic(self, _strStartTime, _strLeaveTime, _strWorkingTime, _strBreakTime):
            if((not _strStartTime and not _strLeaveTime and not _strWorkingTime) or
               (not _strStartTime and not _strLeaveTime and _strWorkingTime) or
               (not _strStartTime and _strLeaveTime and not _strWorkingTime) or
               (_strStartTime and not _strLeaveTime and not _strWorkingTime)):
               self.state = State.IDLE
            elif( _strStartTime and not _strLeaveTime and _strWorkingTime) or not _strBreakTime:
                self.state = State.LEAVETIMEMODE
            elif( _strStartTime and _strLeaveTime and not _strWorkingTime):
                self.state = State.WORKINGTIMEMODE
            elif( not _strStartTime and _strLeaveTime and _strWorkingTime):
                self.state = State.STARTTIMEMODE

    def calculateTime(self):
        try:
            if(self.state == State.IDLE): 
                return
            elif(self.state == State.STARTTIMEMODE):
                #calculate start time
                self.calculateStartTime()
                #output start time
                if(self.model.intStartHours >= 0 and self.model.intStartMinutes >= 0):
                    self.view.show_time('startEntry', f"{str(self.model.intStartHours).rjust(2, '0')}:{str(self.model.intStartMinutes).rjust(2, '0')}")
                else:
                    self.view.show_status("ErrResultNegative")
            elif(self.state == State.LEAVETIMEMODE):
                #calculate leave time
                self.calculateLeaveTime()
                #output working time
                if(self.model.intLeaveHours >= 0 and self.model.intLeaveMinutes >= 0):
                    self.view.show_time('leaveEntry', f"{str(self.model.intLeaveHours).rjust(2, '0')}:{str(self.model.intLeaveMinutes).rjust(2, '0')}")
                else:
                    self.view.show_status("ErrResultNegative")
            elif(self.state == State.WORKINGTIMEMODE):
                #calculate working time
                self.calculateWorkingTime()
                #output working time
                if(self.model.intWorkingHours >= 0 and self.model.intWorkingMinutes >= 0):
                    self.view.show_time('workingEntry', f"{str(self.model.intWorkingHours).rjust(2, '0')}:{str(self.model.intWorkingMinutes).rjust(2, '0')}")
                else:
                    self.view.show_status("ErrResultNegative")
                
        except ValueError as error:
            self.view.show_error(error)
    
    # calculates the working-time based on break-time, start-time and leave-time
    def calculateWorkingTime(self):
        # get all present minutes
        presentMinutes = (self.model.intLeaveHours - self.model.intStartHours)*60
        presentMinutes += self.model.intLeaveMinutes - self.model.intStartMinutes

        # remove minutes for break-time (default: 50min)
        presentMinutes -= (self.model.intBreakMinutes + self.model.intBreakHours*60)

        # store working-time in model
        self.model.intWorkingHours = int(presentMinutes / 60.0)
        self.model.intWorkingMinutes = presentMinutes-(self.model.intWorkingHours*60)

    # calculates the leave-time based on break-time, start-time and working-time
    def calculateLeaveTime(self):
        # get all present minutes
        presentMinutes = (self.model.intStartHours + self.model.intWorkingHours)*60
        presentMinutes += self.model.intStartMinutes + self.model.intWorkingMinutes

        # add minutes for break-time (default: 50min)
        presentMinutes += (self.model.intBreakMinutes + self.model.intBreakHours*60)

        # store leave-time in model
        self.model.intLeaveHours = int(presentMinutes / 60.0)
        self.model.intLeaveMinutes = presentMinutes-(self.model.intLeaveHours*60)

    # calculates the start-time based on break-time, working-time and leave-time
    def calculateStartTime(self):
        # get all present minutes
        presentMinutes = (self.model.intLeaveHours - self.model.intWorkingHours)*60
        presentMinutes += self.model.intLeaveMinutes - self.model.intWorkingMinutes

        # remove minutes for break-time (default: 50min)
        presentMinutes -= (self.model.intBreakMinutes + self.model.intBreakHours*60)

        # store start-time in model
        self.model.intStartHours = int(presentMinutes / 60.0)
        self.model.intStartMinutes = presentMinutes-(self.model.intStartHours*60)

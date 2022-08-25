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
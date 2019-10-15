import datetime
import pprint

def getTimelessDate(dateObject):
    
    return datetime.datetime(dateObject.year, dateObject.month, dateObject.day)


class basicTask():
    def __init__(self, nameDesc, startDate, xDelay):
        self.description = nameDesc # A concise description of what you do in the task.
        self.startDate = startDate #The date to first do the task on. The date on which all calculations are based.
        self.xDelay = xDelay
        self.foresight = 10
        self.dueDates = self.getDueDates()
        

    # Calculate next occurence, xDays after initialDate
    def getDueDates(self):
        foresightCount = self.foresight
        dueDateList = []
        interval = datetime.timedelta(self.xDelay)
        dueDate = self.startDate
        if self.startDate == getTimelessDate(datetime.datetime.now()):
            dueDateList.append(getTimelessDate(datetime.datetime.now()))

        for _ in range(foresightCount):
            dueDate += interval
            dueDateList.append(dueDate)

        return dueDateList

    def renewDueDates(self):
        today = getTimelessDate(datetime.datetime.now())
        lastDate = self.dueDates[-1] # Use this date for calculations if all dates have gone by.
        listOfRemainingDates = [date for date in self.dueDates if date > today]

        newDates = []

        if len(listOfRemainingDates) > 0:
            dueDatesToGet = self.foresight - len(listOfRemainingDates)       
            calculateFrom = listOfRemainingDates[-1]

            interval = datetime.timedelta(self.xDelay)
            for _ in range(dueDatesToGet):
                calculateFrom += interval
                newDates.append(calculateFrom)


        



        self.dueDates = listOfRemainingDates + newDates



lastMonth = getTimelessDate(datetime.datetime(2019, 8, 14))
todayDate = getTimelessDate(datetime.datetime.now())
task1 = basicTask('Study', lastMonth, 7)
print(task1.description)
print('Initial due dates')
pprint.pprint(task1.dueDates)
task1.renewDueDates()
print('Remaining due dates')
pprint.pprint(task1.dueDates)
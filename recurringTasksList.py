import datetime
import pprint

def getTimelessDate(dateObject):
    
    return datetime.datetime(dateObject.year, dateObject.month, dateObject.day)


class basicTask():
    def __init__(self, nameDesc, startDate, xDelay):
        self.description = nameDesc # A concise description of what you do in the task.
        self.startDate = startDate #The date to first do the task on. The date on which all calculations are based.
        self.xDelay = xDelay
        self.foresight = 5
        self.dueDates = self.getDueDates()


    def __str__(self):
        formattedDate = self.getNextDue().strftime('%a, %d of %B')
        return (f'{self.description}: next due on {formattedDate}')
    
    def getNextDue(self):
        
        if self.dueDates[0] > self.startDate:
            return self.dueDates[0]
        else:
            return self.startDate

        

    # Calculate next occurence, xDays after initialDate
    def getDueDates(self):
        foresightCount = self.foresight
        dueDateList = []
        interval = datetime.timedelta(self.xDelay)
        dueDate = self.startDate
        
        if self.startDate >= getTimelessDate(datetime.datetime.now()):
            dueDateList.append(getTimelessDate(datetime.datetime.now()))
            

        for _ in range(foresightCount):
            dueDate += interval
            dueDateList.append(dueDate)

        return dueDateList

    def renewDueDates(self):
        today = getTimelessDate(datetime.datetime.now())
        lastDate = self.dueDates[-1] # Use this date for calculations if all dates have gone by.
        listOfRemainingDates = [date for date in self.dueDates if date > today]
        interval = datetime.timedelta(self.xDelay)

        newDates = []

        if len(listOfRemainingDates) > 0: # If some valid dates are still present in the list:
            dueDatesToGet = self.foresight - len(listOfRemainingDates)       
            calculateFrom = listOfRemainingDates[-1]

            
            for _ in range(dueDatesToGet):
                calculateFrom += interval
                newDates.append(calculateFrom)

        else: # If all dates have passed
            elapsedTime = getTimelessDate(datetime.datetime.now()) - lastDate
            howManyMissed = elapsedTime.days // interval.days # .days for a day-based task
            nextDueDate = lastDate + (datetime.timedelta(interval.days) * (howManyMissed + 1))

            newDates.append(nextDueDate)
            for _ in range(self.foresight):
                nextDueDate += interval
                newDates.append(nextDueDate)
      
        self.dueDates = listOfRemainingDates + newDates

    


aLongTimeAgo = getTimelessDate(datetime.datetime(2019, 2, 2))
lastMonth = getTimelessDate(datetime.datetime(2019, 8, 14))
todayDate = getTimelessDate(datetime.datetime.now())
task1 = basicTask('Study', aLongTimeAgo, 7)
print(task1.description)
print('Initial due dates')
pprint.pprint(task1.dueDates)
task1.renewDueDates()
print('Remaining due dates')
pprint.pprint(task1.dueDates)
print(task1)



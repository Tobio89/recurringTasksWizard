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
        if self.getNextDue() == getTimelessDate(datetime.datetime.now()):
            dueMessage = 'due TODAY'
        elif self.getNextDue() == getTimelessDate(datetime.datetime.now() + datetime.timedelta(days=1)):
            dueMessage = 'due tomorrow'
        else:
            dueMessage = f"next due on {self.getNextDue().strftime('%A, %d of %B,')}"
        return (f'{self.description}: {dueMessage}')
    
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
        
        if self.startDate == getTimelessDate(datetime.datetime.now()):
            dueDateList.append(getTimelessDate(datetime.datetime.now()))
        
        elif self.startDate > getTimelessDate(datetime.datetime.now()):
            dueDateList.append(self.startDate)
            

        for _ in range(foresightCount):
            dueDate += interval
            dueDateList.append(dueDate)

        return dueDateList

    def renewDueDates(self):
        today = getTimelessDate(datetime.datetime.now())
        lastDate = self.dueDates[-1] # Use this date for calculations if all dates have gone by.
        listOfRemainingDates = [date for date in self.dueDates if date >= today]
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
            moduloDays = elapsedTime.days % interval.days # To see if the task is on a valid day, according to its pattern
            if moduloDays:
                nextDueDate = lastDate + (datetime.timedelta(interval.days) * (howManyMissed + 1))
            else:
                nextDueDate = lastDate + (datetime.timedelta(interval.days) * (howManyMissed))

            newDates.append(nextDueDate)
            for _ in range(self.foresight):
                nextDueDate += interval
                newDates.append(nextDueDate)
      
        self.dueDates = listOfRemainingDates + newDates

    def isDueToday(self):
        self.renewDueDates()
        today = getTimelessDate(datetime.datetime.now())
        if today in self.dueDates:
            return True
        else:
            return False


    def delay(self, delayamt):
        '''
        delayamt = how long to delay the due date, in days
        '''
        delayDate = self.dueDates[0] + datetime.timedelta(delayamt)

        slicePoint = len(self.dueDates) # How many dates to cut off
        for date in range(len(self.dueDates)):
            if delayDate <= self.dueDates[date]:
                slicePoint = date
                break

        if slicePoint < len(self.dueDates): # Meaning you're not delaying past all of the due dates
            self.dueDates = self.dueDates[slicePoint:]
            self.dueDates.insert(0, delayDate)
        else: # If you're delaying it beyond all the due dates
            self.dueDates.clear()
            self.dueDates.append(delayDate)
                

    def printDueDates(self):
        for date in self.dueDates:
            formattedDate = date.strftime('%Y/%m/%d, a %A')
            print(formattedDate)            
        

class monthTask(basicTask):
    # def __init__(self, nameDesc, initialDate, xMonths):
    #     super().__init__(nameDesc, initialDate, xMonths)


    # Override: Calculate next occurence, xMonths after initialDate
    def getDueDates(self):
        foresightCount = self.foresight
        inDateYear = self.startDate.year
        inDateMonth = self.startDate.month
        inDateDay = self.startDate.day

        dueDateList = []
        nextMonth = inDateMonth
        nextDateYear = inDateYear

        if self.startDate == getTimelessDate(datetime.datetime.now()):
            dueDateList.append(getTimelessDate(datetime.datetime.now()))
            foresightCount -= 1
            
        elif self.startDate > getTimelessDate(datetime.datetime.now()):
            dueDateList.append(self.startDate)
            foresightCount -= 1

        for _ in range(foresightCount):

            
            
            nextMonth += self.xDelay
            while nextMonth > 12:
                nextMonth -= 12
                nextDateYear += 1
            dueDateList.append(datetime.datetime(nextDateYear, nextMonth, inDateDay))
        
        return dueDateList


    def renewDueDates(self):
        today = getTimelessDate(datetime.datetime.now())
        lastDate = self.dueDates[-1] # Use this date for calculations if all dates have gone by.
        listOfRemainingDates = [date for date in self.dueDates if date >= today]
        

        newDates = []

        if len(listOfRemainingDates) > 0: # If some valid dates are still present in the list:
            dueDatesToGet = self.foresight - len(listOfRemainingDates)       
            calculateFrom = listOfRemainingDates[-1]

            inDateYear = calculateFrom.year
            inDateMonth = calculateFrom.month
            inDateDay = calculateFrom.day

            nextMonth = inDateMonth
            nextDateYear = inDateYear
            
            for _ in range(dueDatesToGet):

                nextMonth += self.xDelay
                while nextMonth > 12:
                    nextMonth -= 12
                    nextDateYear += 1
                newDates.append(datetime.datetime(nextDateYear, nextMonth, inDateDay))


            self.dueDates = listOfRemainingDates + newDates

        else: # If all dates have passed
            elapsedYear = lastDate.year
            elapsedMonth = lastDate.month   
            elapsedDay = lastDate.day

            calculateFrom = lastDate
            calculateYear = elapsedYear
            calculateMonth = elapsedMonth
            calculateDay = elapsedDay

            while calculateFrom < today: # Cycle through date creation until a date not elapsed is reached
                calculateMonth += self.xDelay
                while calculateMonth > 12:
                    calculateMonth -= 12
                    calculateYear += 1
                calculateFrom = datetime.datetime(calculateYear, calculateMonth, calculateDay) # If this date is valid, it will continue to the next part of the program

            foresight = self.foresight
            if calculateFrom == today:
                newDates.append(calculateFrom)
                foresight -= 1
                
            for _ in range(foresight): # Creating a whole new set of dates

                calculateMonth += self.xDelay 
                while calculateMonth > 12:
                    calculateMonth -= 12
                    calculateYear += 1
                newDates.append(datetime.datetime(calculateYear, calculateMonth, calculateDay))
            


                

            
      
            self.dueDates = newDates









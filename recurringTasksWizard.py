import datetime
import shelve

class basicTask():
    def __init__(self, nameDesc, initialDate, xDelay):
        self.name = nameDesc # A concise description of what you do in the task.
        self.initialDate = initialDate#The date to first do the task on. The date on which all calculations are based.
        self.xDelay = xDelay
        self.dueDate = self.getDueDate()
        self.nextDueDate = self.dueDate

    # Calculate next occurence, xDays after initialDate
    def getDueDate(self):
        dayDelta = datetime.timedelta(self.xDelay)
        nextDate = self.initialDate + dayDelta
        return nextDate
    
    def isDueToday(self):
        rawDueDate = self.dueDate
        rawTodayDate = datetime.datetime.now()
        today = (rawTodayDate.year, rawTodayDate.month, rawTodayDate.day)
        dueDate = (rawDueDate.year, rawDueDate.month, rawDueDate.day)

        if today == dueDate:
            self.initialDate = datetime.datetime.now()
            self.nextDueDate = self.getDueDate()
            return True
        
        elif today > dueDate:
            print('Due date has passed.')
            difference = datetime.datetime(today) - datetime.datetime(dueDate)
            self.initialDate = datetime.datetime(today) - difference
            self.dueDate = self.getDueDate()
            self.nextDueDate = self.dueDate
            return False
        else:
            return False


    
    def updateDueDate(self):
        if self.isDueToday():
            self.initialDate = datetime.datetime.now()
            self.nextDueDate = self.getDueDate()
            
        elif self.dueDate < datetime.datetime.now():
            self.dueDate = self.getDueDate()
            self.nextDueDate = self.dueDate



    

    



class dayNameBasedTask(basicTask):
    def __init__(self, nameDesc, initialDate, dayList):
        super().__init__(nameDesc, initialDate, dayList)

    def getDueDate(self):
        days  = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        dayNumbers = [days.index(day) for day in self.xDelay]
        todayDayNumber = int(datetime.datetime.now().strftime('%w'))

        
        nextDay = False
        for day in dayNumbers:
            if day >= todayDayNumber:
                print(f'The next day is {days[day]}')
                nextDay = day
                break
        if nextDay == False:
            nextDay = dayNumbers[0]
        
        if nextDay == todayDayNumber:
            return datetime.datetime.now()
        else:
                    
            dayDifference = nextDay - todayDayNumber
            if dayDifference < 0:
                dayDifference += 7
            
            deltaDifference = datetime.timedelta(days=dayDifference)

            nextDate = datetime.datetime.now() + deltaDifference

            return nextDate


        

    def isDueToday(self):

        todayDayName = datetime.datetime.now().strftime('%a')
        if todayDayName in self.xDelay:
            return True
        else:
            return False
    



class dayReccuringTask(basicTask):
    def __init__(self, nameDesc, initialDate, xDays):
        super().__init__(nameDesc, initialDate, xDays)


    # Calculate next occurence, xDays after initialDate
    def getDueDate(self):
        dayDelta = datetime.timedelta(self.xDelay)
        nextDate = self.initialDate + dayDelta
        return nextDate

class weekRecurringTask(basicTask):
    def __init__(self, nameDesc, initialDate, xWeeks):
        super().__init__(nameDesc, initialDate, xWeeks)


    # Override: Calculate next occurence, xWeeks after initialDate
    def getDueDate(self):
        weekDelta = datetime.timedelta(weeks=self.xDelay)
        nextDate = self.initialDate + weekDelta
        return nextDate

class monthRecurringTask(basicTask):
    def __init__(self, nameDesc, initialDate, xMonths):
        super().__init__(nameDesc, initialDate, xMonths)


    # Override: Calculate next occurence, xMonths after initialDate
    def getDueDate(self):
        inDateYear = self.initialDate.year
        inDateMonth = self.initialDate.month
        inDateDay = self.initialDate.day

        nextDateYear = inDateYear
        nextMonth = inDateMonth + self.xDelay
        while nextMonth > 12:
            nextMonth -= 12
            nextDateYear += 1
        return datetime.datetime(nextDateYear, nextMonth, inDateDay)


# NextByDays - Given a date, calculates the next occurence for x days later, e.g '10 days later'. Used for 'Every X days'
def calculateNextByDays(inDate, _days):
    dayDelta = datetime.timedelta(_days)
    nextDate = inDate + dayDelta
    return nextDate

# Next ByWeeks - Given a date, calculates the next occurence for x weeks later, used for 'Every X weeks'
def calculateNextByWeeks(inDate, _weeks):
    weekDelta = datetime.timedelta(weeks=_weeks)
    nextDate = inDate + weekDelta
    return nextDate

# NextByMonths - Given a date, calculates the next occurence for x months later, used for 'Every X months'
def calculateNextByMonths(inDate, _months):
    inDateYear = inDate.year
    inDateMonth = inDate.month
    inDateDay = inDate.day

    nextDateYear = inDateYear
    nextMonth = inDate.month + _months
    while nextMonth > 12:
        nextMonth -= 12
        nextDateYear += 1
    return datetime.datetime(nextDateYear, nextMonth, inDateDay)


# getDayName - Given a date, returns the day's name: Monday, Saturday, etc. Part of 'Every mon-, wed-, friday'
def getDayName(indate):
    return indate.strftime('%a')

def checkDueOnXDay(indate, listOfDueDays):
    todayDayName = getDayName(indate)
    if todayDayName in listOfDueDays:
        return True
    else:
        return False



       
        

    





# waterPlants = task()




todayDate = datetime.datetime.now()
# todayDate = datetime.datetime(2020,4,10)

print(getDayName(todayDate))



### Testing Day Recurring Task

tenDaysAgo = datetime.datetime.now() - datetime.timedelta(12)

plants = dayReccuringTask('Water the plants', tenDaysAgo, 10)

print(plants.name)
print(plants.nextDueDate)
print(plants.isDueToday())


### Testing Week Recurring Task

# reportsTask = weekRecurringTask('Write Reports', todayDate, 12)

# print(reportsTask.name)
# print(reportsTask.nextDueDate)
# print(reportsTask.isDueToday())


### Testing Month Recurring Task

# KBcertificateTask = monthRecurringTask('Renew KB Injung Cert', todayDate, 6)
# print(KBcertificateTask.name)
# print(KBcertificateTask.nextDueDate)
# print(KBcertificateTask.isDueToday())

### Testing Dayname Recurring Task

# study = dayNameBasedTask('Study Polish', todayDate, ['Thu'])
# print(study.isDueToday())
# print(study.nextDueDate)

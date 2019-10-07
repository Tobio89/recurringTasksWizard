import datetime
import shelve

class task():
    def __init__(self, nameDesc, initialDate):
        self.name = nameDesc # A concise description of what you do in the task.
        self.initialDate = initialDate #The date to first do the task on. The date on which all calculations are based.

class dayReccuring(task):
    def __init__(self, nameDesc, initialDate, xDays):
        super().__init__(nameDesc, initialDate)
        self.xDays = xDays
        self.nextDueDate = self.getDueDate()

    # Calculate next occurence, xDays after initialDate
    def getDueDate(self):
        dayDelta = datetime.timedelta(self.xDays)
        nextDate = self.initialDate + dayDelta
        return nextDate
    
    def isDueToday(self):
        rawDueDate = self.nextDueDate
        rawTodayDate = datetime.datetime.now()
        today = (rawTodayDate.year, rawTodayDate.month, rawTodayDate.day)
        dueDate = (rawDueDate.year, rawDueDate.month, rawDueDate.day)

        return today == dueDate

    


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
    return indate.strftime('%A') 


       
        

    





# waterPlants = task()




todayDate = datetime.datetime.now()

plants = dayReccuring('Water the plants', todayDate, 10)

print(plants.name)
print(plants.nextDueDate)
print(plants.isDueToday())








# It's tough to write this here where people are talking.

# Include: a task that repeats on every ___day in a given week (every mon and fri , every thursday).
# Include: a task that repeats on the __th of each month.
# Include: a task that repeats every n days.
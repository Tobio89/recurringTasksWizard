import datetime, os, pprint, shelve

import recurringTasksDataInterface as tasksData
from recurringTasksList import getTimelessDate, basicTask, monthTask

os.chdir(r'C:\Users\User\.spyder-py3\Ultraccountability\recurringTasksWizard\dict')


def saveToShelf(saveWhat):
    with shelve.open('MyTaskData') as shelveFile:
        print('Saving Task Objects...')
        shelveFile['taskObjects'] = saveWhat


def openShelf():
    with shelve.open('MyTaskData') as shelveFile:
        openWhat = shelveFile['taskObjects']
    return openWhat

def selectTaskByIndex(list_):
    for number, item in enumerate(list_):
        print(f'[{number}] - {item}')
    try:
        selection = int(input('\nEnter the number of the chosen item: '))
        return selection
    except:
        print('Invalid selection. Aborting...')
        
def getNewTaskDate():
    print('Enter the date you want the task to start, separated by /')
    date = input("Or enter 'today': ")
    if date in ('today', 'TODAY', 'Today'):
        dateDetails = getTimelessDate(datetime.datetime.now())
    else:
        try:
            separatedDate = date.split('/')
            dateDetails = datetime.datetime(int(separatedDate[0]), int(separatedDate[1]), int(separatedDate[2]))
        except:
            print('Error: Invalid date entered. Try entering the date as YYYY/MM/DD.')
    
    return dateDetails


def listDueTomorrow(listOfTasks):
    tomorrowDate = getTimelessDate(datetime.datetime.now() + datetime.timedelta(days=1))
    
    tasksDueTomorrow = [task for task in listOfTasks if task.getNextDue() == tomorrowDate]

    return tasksDueTomorrow
    
def findSoonestTask(listOfTasks):
    for task in listOfTasks:
        task.renewDueDates()

    soonestTaskIndex = 0
    soonestDate = listOfTasks[0].dueDates[0]

    for index, task in enumerate(listOfTasks):
        task.renewDueDates
        if task.dueDates[0] <= soonestDate:
            soonestTaskIndex = index
            soonestDate = task.dueDates[0]
    return soonestTaskIndex

def sortTasksByDueDate(listOfTasks):
    sortedList = []
    for item in range(len(listOfTasks)):
        soonest = findSoonestTask(listOfTasks)
        sortedList.append(listOfTasks.pop(soonest))
    
    return sortedList

print('RECURRING TASK WIZARD')
tasksLoadedFromShelf = sortTasksByDueDate(openShelf()) #Selection sort tasks by due date


displayTasks = True
RUNNING = True
changeToSave = False

while RUNNING:
    if displayTasks:
        print('\nTasks due today:\n\n')
        tasksDueToday = [task for task in tasksLoadedFromShelf if task.isDueToday()]
        if tasksDueToday:
            for task in tasksDueToday:
                print(f'     - {task.description}')
            print('\n')
        else:
            print('None')
        displayTasks = False
    print('Commands include add, remove, delay, tomorrow, and list')
    userCom = input('Enter a command, or enter nothing to exit: ').lower()

    if userCom.lower() not in ('add', 'remove', 'delay', 'list', 'tomorrow'):
        
        print('See you tomorrow!')
        RUNNING = False
    
    elif userCom.lower() == 'add':
        typeOfTaskToCreate = input("Enter 'day' or 'month' to add\na day- or month- based task: ")
        newTaskDescription = input('Enter a description for the task: ')
        newTaskDate = getNewTaskDate()
        newTaskInterval = int(input(f'How many {typeOfTaskToCreate.lower()}s later will the task repeat?: '))

        if typeOfTaskToCreate.lower() == 'day':
            newTask = basicTask(newTaskDescription, newTaskDate, newTaskInterval)
        elif typeOfTaskToCreate.lower() == 'month':
            newTask = monthTask(newTaskDescription, newTaskDate, newTaskInterval)

        
        print(f'\nNew task:\n\t{newTask}\n...has been added.')
        tasksLoadedFromShelf.append(newTask)

        displayTasks = True
        changeToSave = True
    
    elif userCom.lower() == 'remove':
        print('What task do you want to remove?')
        indexOfTaskToRemove = selectTaskByIndex(tasksLoadedFromShelf)
        print(f"\nTask '{tasksLoadedFromShelf[indexOfTaskToRemove].description}' has been removed.\n")
        tasksLoadedFromShelf.pop(indexOfTaskToRemove)
        displayTasks = True
        changeToSave = True

    elif userCom.lower() == 'delay':
        print('Which task do you want to delay?')
        indexOfTaskToDelay = selectTaskByIndex(tasksLoadedFromShelf)
        try:
            howLongToDelayBy = int(input('Enter the time in days for\nhow long you want to delay the task: '))
        except:
            print('Error: days to delay must be a number.')
        print(f"\nTask '{tasksLoadedFromShelf[indexOfTaskToDelay].description}' has been delayed by {howLongToDelayBy} day(s):")
        tasksLoadedFromShelf[indexOfTaskToDelay].delay(howLongToDelayBy)

        print(f'\n\t{tasksLoadedFromShelf[indexOfTaskToDelay]}\n')

        displayTasks = True
        changeToSave = True

    elif userCom.lower() == 'list':
        print('\n')
        print('Listing all tasks in database:')
        for task in tasksLoadedFromShelf:
            print(f'    - {task}')
        print('\n')

    elif userCom.lower() == 'tomorrow':
        tasksDueTomorrow = listDueTomorrow(tasksLoadedFromShelf)
        print('\n')
        for task in tasksDueTomorrow:
            print(f'    - {task}')
        print('\n')
        



if changeToSave:
    print('Saving changes...')
    saveToShelf(tasksLoadedFromShelf)
    print('Saving done. Bye!')





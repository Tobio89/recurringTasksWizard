import datetime, os, pprint, shelve

import recurringTasksDataInterface as tasksData
from recurringTasksList import getTimelessDate, basicTask


os.chdir(r'C:\Users\User\.spyder-py3\Ultraccountability\recurringTasksWizard\dict')

taskDict = tasksData.tasksDict

def saveToShelf(saveWhat):
    with shelve.open('MyTaskData') as shelveFile:
        print('Saving Task Objects...')
        shelveFile['taskObjects'] = saveWhat


def openShelf():
    with shelve.open('MyTaskData') as shelveFile:
        openWhat = shelveFile['taskObjects']
    return openWhat

def checkNewTasks(taskObjectList):
    incomingTasks = [task for task in taskDict.keys()]

    taskDescriptions = [task.description for task in taskObjectList]

    newTasks = {desc : data for desc, data in taskDict.items()  if desc not in taskDescriptions}
   

    if newTasks:
        print('Found new tasks:')
        for item in newTasks.keys():
            print(item)
        return newTasks
    else:
        return None
    


def deleteTasks(taskObjectList):
    incomingTasks = [task for task in taskDict.keys()]

    taskDescriptions = [task.description for task in taskObjectList]

    updatedTaskList = []

    for index, task in enumerate(taskDescriptions):
        if task in incomingTasks:
            updatedTaskList.append(taskObjectList[index])
        
    if len(updatedTaskList) < len(taskObjectList):
        print('Some tasks were removed from the database.')
    
    return updatedTaskList
    
   
    


def addNewTasks(taskObjectList):
    print('Checking for new tasks...')
    newTasks = checkNewTasks(taskObjectList)

    if newTasks:
        
        for taskItem in newTasks.items():
            taskDesc = taskItem[0]
            taskInitDate = taskItem[1]['initTime']
            taskInterval = taskItem[1]['interval']

            basicTaskObject = basicTask(taskDesc, taskInitDate, taskInterval)

            taskObjectList.append(basicTaskObject)
    else:
        print('No new tasks imported; nothing to add.')

    
# basicTasks = []

# for taskItem in taskDict.items():
#     taskDesc = taskItem[0]
#     taskInitDate = taskItem[1]['initTime']
#     taskInterval = taskItem[1]['interval']

#     basicTaskObject = basicTask(taskDesc, taskInitDate, taskInterval)
#     basicTasks.append(basicTaskObject)

# saveToShelf(basicTasks)


# basicTasks = openShelf()

# print(basicTasks[5].dueDates)



if __name__ == '__main__':
    basicTasks = openShelf()

    addNewTasks(basicTasks)
    basicTasks = deleteTasks(basicTasks)

    
    tasksDueToday = []

    for task in basicTasks:
        if task.isDueToday() == True:
            tasksDueToday.append(task)



    print('\nRECURRING TASKS WIZARD: What do you have to do today?\n')
    if not tasksDueToday:
        print('No scheduled tasks today\n')
        input('Enter any key to exit')
    else:
        for task in tasksDueToday:
            print(task.description)
            

    print('\n')
    
    print('Type "delay" to enter delay mode,')
    print('Type "list" to see all possible tasks,')
    usercom = input('Or enter any key to exit: ')
    if usercom.lower() == 'delay':
        delayMode = True
        while delayMode:
    
            for index, item in enumerate(tasksDueToday):
                print(f'{index}: {item.description}')
            print('\n')
            delayIndex = int(input('Enter the index of the task you want to delay: '))
            delayLength = int(input('Enter the number of days to delay the task by: '))
            tasksDueToday[delayIndex].delay(delayLength)
            print(f"Task '{tasksDueToday[delayIndex].description}' was delayed by {delayLength} day/s" )

            print("Enter 'continue' to continue delaying tasks,")
            exitCom = input("Or enter any key to exit: ")

            if exitCom.lower() not in ('continue', 'c'):
                delayMode = False
    
    elif usercom.lower() == 'list':
        print('\nHere are all tasks, and their next due dates:\n')
        for task in basicTasks:
            print(task)
        print('\n')
        input('Enter any key to exit: ')



    saveToShelf(basicTasks)
    print('See you tomorrow!')


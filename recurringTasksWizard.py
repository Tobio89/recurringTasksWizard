import shelve, pprint
import datetime

from recurringTasksList import getTimelessDate, basicTask

initTime = 'initTime'
interval = 'interval'

# tasksDict = {
#     'Study Polish': {
#         initTime : datetime.datetime(2019,10,21),
#         interval : 7
#     },
#     'Study Korean': {
#         initTime : datetime.datetime(2019,10,23),
#         interval : 7
#     },
#     'Vacuum the house': {
#         initTime : datetime.datetime(2019,10,18),
#         interval : 3
#     },
# }

# with shelve.open('MyTaskData') as shelfFile:
#     shelfFile['taskData'] = tasksDict



def getTaskData():
    with shelve.open('MyTaskData') as shelfFile:
        dic = shelfFile['taskData']
    return dic

def saveTaskData(updatedDic):
    with shelve.open('MyTaskData') as shelfFile:
        shelfFile['taskData'] = updatedDic
        print('Task Data Dictionary has been saved')


if __name__ == '__main__':

    print('RECURRING TASK WIZARD')
    tasksDict = getTaskData()
    pprint.pprint(tasksDict)

    while True:
        usercom = input('Enter a command:')

        if usercom.lower() == 'exit':
            break
        
        elif usercom.lower() == 'save':
            print('Saving...')
            saveTaskData(tasksDict)

        elif usercom.lower() == 'add':
            
            try:
                taskDescription = input('Enter the description for the task: ')
                dateDetails = input('Enter the date the task will begin: ')

                if dateDetails.lower() == 'today':
                    dateDetails = getTimelessDate(datetime.datetime.now())
                else:
                    try:
                        separatedDate = dateDetails.split('/')
                        dateDetails = datetime.datetime(separatedDate[0], separatedDate[1], separatedDate[2])
                    except:
                        print('Invalid date entered. Use "/" characters to separate the date, as YEAR/MONTH/DAY')
                        continue
                
                specifiedInterval = int(input('Enter the interval in days: '))

                tasksDict[taskDescription] = {
                    initTime : dateDetails,
                    interval : specifiedInterval
                }
            except:
                print('Error adding task. Was the date in the correct format? YEAR/MONTH/DATE')
                continue
        
        elif usercom.lower() == 'delete':
            keys = list(tasksDict.keys())
            for number, key in enumerate(keys):
                print(f'[{number}]: {key}')
            delNum = int(input('Enter the number of the task you want to delete: '))

            delTask = keys[delNum]

            removedTask = tasksDict.pop(delTask)

            print(f'Removed task: {delTask}.')

        elif usercom.lower() == 'print':
            pprint.pprint(tasksDict)



            
    


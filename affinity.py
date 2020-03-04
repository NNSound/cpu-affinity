import psutil
import json
import logging

with open('./config.json') as f:
    setting = json.load(f)

logging.basicConfig(level=logging.INFO,format='[%(asctime)s][%(levelname)-4s] %(message)s',
                    datefmt='%m-%d %H:%M:%S', handlers = [logging.FileHandler('affinity.log', 'a+', 'utf-8'),])

if (not setting.__contains__('ProcessName') or not setting.__contains__('cpu')):
    input("設定檔錯誤，按任意鍵退出")
    logging.warning("設定檔錯誤")
    exit()

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects

listOfProcessIds = findProcessIdByName(setting['ProcessName'])

cpuCount = psutil.cpu_count()
logging.info("Cpu Count: %d"%(cpuCount))

if (setting['cpu'] < 0):
    msg = "請設定 0 以上的數字，謝謝"
    logging.warning(msg)
    print(msg)
    input("按任意鍵離開...")
    exit()

if (setting['cpu'] > cpuCount):
    msg = "您的CPU核心數只有 %d 個, 請買好一點的CPU或是調低CPU 設定值"%(cpuCount)
    logging.warning(msg)
    print(msg)
    input("按任意鍵離開...")
    exit()

arr = []
for i in range(0, setting['cpu']):
    arr.append(i)

for pid in listOfProcessIds:
    p = psutil.Process(pid['pid'])
    p.cpu_affinity(arr)

print("成功設定CPU親合")
logging.info("成功設定CPU親合")
input("按任意鍵離開...")
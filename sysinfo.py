import psutil as p
import platform


def sysinfo():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}") 

def size(byte):
  #this the function to convert bytes into more suitable reading format.

  #Suffixes for the size
  for x in ["B","KB","MB","GB","TB"]:
    if byte<1024:
      return f"{byte:.2f}{x}"
    byte=byte/1024

#Function to get info about Disk Usage.
def disk():
  print("-"*50, "Disk Information", "-"*50)
  print("Partitions on Drive:")

  par = p.disk_partitions()
  print (par)
  # getting all of the disk partitions
  sum = 0
  for x in par:
      if x.device == 'D:\\':
          continue
      print("Drive: ", x.device)
      print("  File system type: ", x.fstype)

      dsk = p.disk_usage(x.mountpoint)
      print("  Total Size: ", size(dsk.total))
      print("  Used:       ", size(dsk.used))
      print("  Free:       ", size(dsk.free))
      print("  Percentage: ", dsk.percent, "%\n")

      intermediate = size(dsk.free)[:-2]
      sum1 = float(intermediate)
      sum = sum + sum1

  print ("Total free memory is:", sum,"GB")
   
      
  main()

#Function to Get memory/Ram usage.
def memory():
  print("-"*50, "Memory Information", "-"*50)

  #Getting the Memory/Ram Data.
  mem = p.virtual_memory()
  print("Total Memory:    ",size(mem.total))
  print("Available Memory:", size(mem.available))
  print("Used Memory:     ", size(mem.used))
  print("Percentage:      ",mem.percent,"% \n")

  #Getting the Swap Memory Data.
  #It is the Hard disk/ SSD space Which is used up as main memory when the main memory is not sufficient. 
  print("-"*48, "Swap Memory Information", "-"*47)
  swmem = p.swap_memory()
  print("Total Memory:    ", size(swmem.total))
  print("Available Memory:", size(swmem.free))
  print("Used Memory:     ", size(swmem.used))
  print("Percentage:      ", swmem.percent, "%\n")

  main()

#Function to get CPU information.
def cpu():
  print("-"*50, "CPU Information", "-"*50)

  #Getting the logical and physical core count.
  print("Logical/Total Core Count: ", p.cpu_count(logical=True) )
  print("Physical Core Count: ", p.cpu_count(logical=False))

  #Getting the CPU Frequencies.
  fre=p.cpu_freq()
  print("Maximum Frequency:" ,fre.max, "Mhz")
  print("Minimum Frequency:", fre.min,"Mhz")
  print("Current Frequency: ",fre.current ,"Mhz")

  #Getting the CPU Usage.
  for x, percentage_usage in enumerate(p.cpu_percent(percpu=True)):
      print("Core ",x, ":",percentage_usage,"%")
  print("Total CPU Usage:", p.cpu_percent(),"%\n")
  main()
def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in p.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (p.NoSuchProcess, p.AccessDenied, p.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects
def processtop5():
    print("*** Iterate over all running process and print process ID & Name ***")
    # Iterate over all running process
    for proc in p.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            print(processName , ' ::: ', processID)
        except (p.NoSuchProcess, p.AccessDenied, p.ZombieProcess):
            pass
    print('*** Create a list of all running processes ***')
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in p.process_iter():
       # Get process detail as dictionary
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       # Append dict of process detail in list
       listOfProcessNames.append(pInfoDict)
    # Iterate over the list of dictionary and print each elem
    for elem in listOfProcessNames:
        print(elem)
    print('*** Top 5 process with highest memory usage ***')
    listOfRunningProcess = getListOfProcessSortedByMemory()
    for elem in listOfRunningProcess[:5] :
        print(elem)
    main()
#Main Function
def main():
  print("\nPress 1 for Disk Info. \nPress 2 for Memory/Ram Info. \nPress 3 for CPU Info. \nPress 4 for SYS Info. \nPress 5 for Process Info.\nPress 0 to exit.")
  choice=int(input(">>> "))
  
  if choice==1: 
    disk()
  elif choice==2:
    memory()
  elif choice==3:
    cpu()
  elif choice ==4:
    sysinfo()
  elif choice==5:
      processtop5()
  elif choice==0:
    pass
  else:
    print("Please provide a valid input")

#Driver Function
if __name__ == "__main__":
  main()
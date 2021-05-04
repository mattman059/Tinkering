#!/usr/bin/python

#WRITTEN IN PYTHON3 (3.8.5) on Windows 10 2004 x86_64
#Threading Class Structure scraped from: https://www.tutorialspoint.com/python/python_multithreading.htm

#Make sure this script runs from the same directory where exported bookmarks exist

import queue
import threading
import time
import requests
import sys
import math

exitFlag = 0
URL_SCAN_LIST = "URLs.txt"
INITIAL_BOOKMARKS = "bookmarks.html"

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      #print("Starting " + self.name + "\n")
      process_data(self.name, self.q)
      
def process_data(threadName, q):
   while not exitFlag:
      queueLock.acquire()
      
      if not workQueue.empty():
            data = q.get()
            queueLock.release()
            process_URL(threadName,data)
      else:
         queueLock.release()
         time.sleep(1)

def process_URL(threadName,url):
    try:
        r = requests.get(url.strip())
        if r.status_code != 200:
            print(threadName + " - " + str(r.status_code) + ": " + url + "\n")
    except:
        print(threadName + " - [*]: " + url.strip())
        pass

def process_bookmarks():
    count = 0
    fh = open(INITIAL_BOOKMARKS, encoding='utf-8')
    fh_out = open(URL_SCAN_LIST,'w')
    for line in fh.readlines():
        if "HREF" in line:
            try:
                href = line.split(" ")[9]
                if (len(href) > 0) and ("HREF" in href):
                    href2 = href.split("=\"")[1].strip("\"")
                    fh_out.write(href2 + "\n")
                    count += 1
            except IndexError:
                pass

    print("Processed " + str(count) + " URLs")
    doProcess()
    fh_out.close()



######################################
#### Build nameList from URL file ####
nameList = []
    
def doProcess():
    fh = open(URL_SCAN_LIST)
    for line in fh.readlines():
        nameList.append(line.strip())

try:
    doProcess()
except:
    try:
        process_bookmarks()
    except:
        print("Something bad happened")
        sys.exit(0)

threadNumber = math.floor(len(nameList) * .05)
print("NUMBER OF THREADS: " + str(threadNumber))
threadList = []
for i in range(threadNumber):
    threadList.append("Thread-" + str(i))

######################################
    
queueLock = threading.Lock()
workQueue = queue.Queue(len(nameList))
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
   workQueue.put(word)
queueLock.release()
# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print("Exiting Main Thread")

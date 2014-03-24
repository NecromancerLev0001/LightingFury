'''
Created on 2014. 3. 21.

@author: Su-Jin Lee
'''

from time import time

INTERVAL = 60

class LazySweeper(object):
    workList = []
    
    def __init__(self, interval=INTERVAL):
        self.interval = interval
        self.doTime = time() + self.interval
        
    def sweep(self):
        if self.doTime > time():
            return False            
        for work in self.workList:
            work()
        self.doTime = time() + self.interval
        
    def addWork(self, work):
        self.workList.append(work)        
            
if __name__ == '__main__':
    sweeper = LazySweeper()
    while True:
        sweeper.sweep()

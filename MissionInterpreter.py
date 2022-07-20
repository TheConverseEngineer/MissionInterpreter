import time
import matplotlib.pyplot as plt
import numpy as np

class MissionInterpreter:
        
    def __init__(self, logs: dict, times: dict, startTime: float, endTime: float):
        """ NOTE: It is not reccomended to directly create this class. Instead, use one of the provided static methods
            
            SEE ALSO: createFromFile(filename: str) -> MissionInterpreter
        """
        self.logs = logs
        self.times = times
        self.startTime = startTime
        self.endTime = endTime
      
    def getLogs(self, name: str, returnType=str) -> list:
        """ Get the logs corresponding to the given name, with the option to specify how these logs should be returned """
        if (returnType == str): return self.logs[name]
        elif (returnType == bool): return [i=="true" for i in self.logs[name]]
        else:
            try:
                return [returnType(i) for i in self.logs[name]]
            except Exception: raise Exception(f"ERR: The logs under {name} could not be converted to {returnType}")
    
    def getTimes(self, name: str) -> list:
        return self.times[name]
    
    def getTimedLogs(self, name: str, returnType: str) -> list:
        """ Does the same thing as getLogs, but returns a list of pairs consisting of (time, value) """
        var = self.getLogs(name, returnType)
        return list(zip(self.times[name], var))
    
    def getTimedPlotValues(self, name: str, modifier=None) -> (list, list):
        """ Returns all the data needed to plot a graph showing the given value over time
    
            A modifier in the form of a method from the modifiers subclass can be passed here
        """
        if modifier is None: data = self.getLogs(name, returnType=float)
        else: data = modifier(self.getLogs(name, returnType=float)) 
        return (self.getTimes(name), data);
        
    def get2DPlotValued(self, name1: str, name2: str, mod1=None, mod2=None) -> (list, list):
        """ Returns all the data needed to plot a graph showing the two given values

            A modifier in the form of a method from the modifiers subclass can be passed here
        """
        if mod1 is None: data1 = self.getLogs(name, returnType=float)
        else: data1 = modifier(self.getLogs(name, returnType=float))
        if mod2 is None: data2 = self.getLogs(name, returnType=float)
        else: data2 = modifier(self.getLogs(name, returnType=float))
        return (data1, data2)
    
    def getLambdaPlotValues(self, names: list, func) -> (list, list):
        """ Returns all the data needed to plot a graph showing the lambda value of the name list """
        reps = min([(len(self.logs[i]), i) for i in names])
        data = [func(*[float(self.logs[i][j]) for i in names]) for j in range(reps[0])]
        return (self.getTimes(reps[1]), data);
    
    @staticmethod
    def createFromFile(filename: str, include=None, exclude=None, filterRepeats=False, ignoreBlanks=True):
        """ Creates a Mission Interpreter from an alog file.

        filename: str
            The name of the alog file (including the path if the file is not in the same directory)
        """
        start = time.perf_counter()
        logs = {}
        times = {}
        startTime, endTime = (0, 0)
        with open(filename, 'rt') as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == '%':
                    if line[:3] == '%%%': continue # go to next line
                    if 'LOGSTART' in line:
                        data = [i for i in line.split(' ') if i]
                        startTime = float(data[2])
                else: # these are the data lines
                    x = line.split()
                    if (len(x)<3): continue
                    elif (len(x)==3):
                        if (ignoreBlanks): continue
                        else:
                            if (include is not None and x[1] in include) or (exclude is not None and x[1] not in exclude) or (include is None and exclude is None):
                                if (not filterRepeats) or (x[1] not in logs) or (not logs[x[1]][-1] == ""):
                                    MissionInterpreter.Utils.appendDict(logs, x[1], "")
                                    MissionInterpreter.Utils.appendDict(times, x[1], float(x[0]))
                    else:
                        if (include is not None and x[1] in include) or (exclude is not None and x[1] not in exclude) or (include is None and exclude is None):
                            if (not filterRepeats) or (x[1] not in logs) or (not logs[x[1]][-1] == " ".join(x[3:])):
                                MissionInterpreter.Utils.appendDict(logs, x[1], " ".join(x[3:]))
                                MissionInterpreter.Utils.appendDict(times, x[1], float(x[0]))
                    endTime = float(x[0])
            return MissionInterpreter(logs, times, startTime, endTime + startTime)

    class Modifiers:
        """ A simple static sub-class filled with some common data modifiers (can also be used for plotting) """
        @staticmethod
        def derivate(items: list) -> list:
            """ Derivates a list (position -> velocity, velocity -> acceleration, etc.). Secant approx. used """
            if (len(items) < 2): return [0] * len(items)
            newList = [0] * len(items)
            newList[0] = abs(items[0]-items[1])
            for i in range(1, len(items)):
                newList[i] = abs(items[i]-items[i-1])
            return newList
                
        @staticmethod
        def integrate(items: list) -> list:
            """ Integrate a list (velocity -> position, acceleration -> velocity, etc.). Rieman sum used (no +C)"""
            newList = [0] * len(items)
            newList[0] = items[0]
            for i in range(1, len(items)):
                newList[i] = newList[i-1] + items[i]
            return newList
            
    class Utils:
        """ A simple static sub-class filled with some common utility functions """
        @staticmethod
        def appendDict(dictionary, key, value):
            """ A simple function that appends a value to a dictionary, or adds it if the key is not present """
            if (key in dictionary): dictionary[key].append(value)
            else: dictionary[key] = [value]
           

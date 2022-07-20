# Mission Interpreter
Conveniance Wrapper for reading alog files


## Usage examples:

### Creating a new interpreter:
    itp = MissionInterpreter.createFromFile(filename)
  
This function comes with a number of optional optimizations:
   - filterRepeats: when true, ignore logs if the variable stays the same
   - include:       If you only want to look at certain variables, pass the names of those variables in a list
   - exclude:       If you want to ignore certain variables, add them to this list.
   - ignoreBlanks   Setting this to true will cause the reader to skip over lines where no variables are set
       
       
### Reading data:
If you want all datapoints for SOME_VARIABLE, run `itp.getLogs("SOME_VARIABLE")`
    
If you want to access the data in a specific form, you can use the returnType argument. For example, setting `returnType=float` will cause the function to return a list of floats.
WARNING: trying to return an invalid type will cause an error (example, trying to get integers as floats)
    
### Reading times:
If you want a list of every time SOME_VARIABLE was changed, run `itp.getTimes("SOME_VARIABLE")`
This function will always return a list of floats
    
### Mission start/end time:
The mission start and end times can easily be accessed with `itp.startTime` and `itp.endTime`, respectively
NOTE: unlike the alog_parser, this class does NOT create a LOGTIME key in the times dictionary.
    
### Getting times and data:
If you want a combined list that has both timestamps and variable values, use `itp.getTimedLogs("SOME_VARIABLE")`
This will return a list in the following format: [(timestamp, new value), (timestamp, new value), (timestamp, new value), (timestamp, new value), ...]
Once again, you can use the returnType argument to specify which kind of variable you want (this will only affect values, not timestamps)

PLOTTING:
    NOTE: all plotting functions can be run in the same way:
        import matplotlib.pyplot as plt
        plt.scatter(*ipt.THE_FUNCTION_YOU_WANT_TO_USE)
        plt.show()
        
    NOTE: Only data that can be represented as floats can be plotted with these functions
        
    Plotting one variable over time: Use getTimedPlotValues("SOME_VARIABLE")
    
    Plotting two variables against each other: Use get2DPlotValues("SOME_VARIABLE", "SOME_OTHER_VARIABLE")
    
    Plotting some function over time:
        Use getLambdaPlotValues([LIST_OF_NEEDED_VARIABLES], FUNCTION_YOU_WANT_TO_RUN)
        
        For example, say that you want to graph the distance to (0, 0) over time.
            Note that the formula for finding the distance from origin is simply SQRT(x^2 + y^2)
            
            Start by defining this as a function:
            def distToZero(x, y):
                return numpy.sqrt(x**2 + y**2)
            
            Then run as follows: getLambdaPlotValues(["NAV_X", "NAV_Y"], distToZero)
            Note that the order of the variables in the list must be the same as the order of parameter in the function
            
            
MODIFIERS:
    Modifiers are an easy way to edit a list.
    There are currently two modifiers, derivate (with derivates a list) and integrate (with integrates a list, ignoring constants)
    NOTE: Data used with modifiers must be floats
    
    They can be used as such:
    x = itp.getLogs("Nav_X", returnType = float)
    velocityOfX = MissionInterpreter.Modifiers.derivate(x)
    otherX = MissionInterpreter.Modifiers.integrate(x)
    
    Modifiers can also be used when plotting as such:
        plt.scatter(*ipt.getTimedPlotValues("NAV_X", modifier=derivate))
        plt.show()
        
        This code will plot a graph of dx/dt over time
    

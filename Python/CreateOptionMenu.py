from TkOptionMenu import OptionsMenu
from tkinter import Tk
from time import sleep

#* Include any files from which you want to get globals from here



def getOptions(obj=None, namespace=globals()):
    ''' Gets all the Option members in the passed in class. The passed in class must have a default constructor. '''

    if obj is None:
        options = [namespace[attr] for attr in namespace if not callable(namespace[attr]) and not attr.startswith("__") and type(namespace[attr]) == Option]
    else:
        options = [getattr(obj, attr) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__") and type(getattr(obj, attr)) == Option]
    return options


def createOptionMenu(*instances, getGlobal=True, windowName='Options', sort=True, styleOptionTab='General', namespace=globals()):
    options = []

    #* Go through the classes passed in, get all the options from them, and add them to members under their key (and sort them)
    for i in instances:
        options += getOptions(i)

    #* Do the same with global variables
    if getGlobal:
        options += getOptions(namespace=namespace)

    if sort:
        options.sort()

    OptionsMenu(Tk(className=windowName), *options, styleOptionTab=styleOptionTab).mainloop()

    # Escape debouncing
    sleep(.15)

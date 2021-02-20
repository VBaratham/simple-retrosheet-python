"""
This file defines the object which reads in the actual retrosheet,
hands the data off to each of the handlers registered to it, and
produces the final output
"""
import sys
import csv
import itertools
import logging as log
from collections import OrderedDict
from fileinput import FileInput

from retrosheet.event import pythonify_line

class FatalHandlerException(Exception):
    """
    Class of exceptions that should stop the analysis immediately
    """
    pass

class NonfatalHandlerException(Exception):
    """
    Class of exceptions that cause a handler to enter the error state
    but not terminate the analysis
    """
    pass

class StopAnalysis(FatalHandlerException):
    """
    A handler or trigger should raise this exception to stop the
    analysis before all games/events have been read
    """
    pass

    

class Analysis(object):
    def __init__(self, filename=None, filenames=None):
        """
        Creates an Analysis object for parsing the MLB retrosheet.
        @param filename - name of the retrosheet Event file 
        @param filenames - if running on multiple Event files (you usually will),
                           pass them as a list here.
        If neither @filename nor @filenames is specified, we will expect the retrosheet on STDIN
        If either is passed, STDIN will be ignored
        """
        # TODO: allow passing year(s) to fetch the sheet from the internet on the fly
        if filename and filenames:
            raise ValueError("Use either @filename or @filenames, not both." + \
                             " Or send all data through STDIN and use neither.")
        
        if filenames:
            self.filenames = filenames
        elif filename:
            self.filenames = [filename]
        else:
            self.filenames = ['-'] # FileInput treats this as stdin

        self.handlers = OrderedDict()
        self.triggers = OrderedDict()

    def _retrosheet_as_filelike(self):
        """ Return the entire retrosheet as a single (lazily-loaded) file-like """
        return FileInput(files=self.filenames)
            
    def _get_python_stream(self):
        """ Yield all lines in the retrosheet as Python objects """
        reader = csv.reader(self._retrosheet_as_filelike())
        for line in reader:
            log.debug(line)
            pyline = pythonify_line(line)
            if pyline:
                yield pyline

    def register_handler(self, name, handler):
        """
        Register a handler for this analysis
        @param name - the name of this handler, for later reference when we go
                      to fetch its' data
        @param handler - the handler object
        """
        self.handlers[name] = handler

    def register_trigger(self, name, trigger):
        self.triggers[name] = trigger

    def fire_trigger(self, trigger_name):
        # A trigger is a function that receives the dictionary of
        # handlers and does something with their data
        self.triggers[trigger_name](self.handlers)

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    
    def run(self):
        self.preprocess()
        
        try:
            for pyline in self._get_python_stream():
                for handler in self.handlers.values():
                    try:
                        # run the handler
                        trigger_name = handler.handle(pyline)
                    except NonfatalHandlerException as e:
                        log.error(e)
                        handler.mark_error()

                    # if the handler returned a trigger, fire it
                    if trigger_name:
                        self.fire_trigger(trigger_name)
                        
        except FatalHandlerException as e:
            log.error(e)

        self.postprocess()
                

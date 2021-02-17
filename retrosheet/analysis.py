"""
This file defines the object which reads in the actual retrosheet,
hands the data off to each of the handlers registered to it, and
produces the final output
"""
import sys
from collections import OrderedDict

from retrosheet.event import pythonify_line

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
            raise ValueError("Use either @filename or @filenames, not both. Alternatively, send all data through STDIN")
        
        if filenames:
            self.filenames = filenames
        elif filenames:
            self.filenames = [filename]
        else:
            self.filenames = None

        self.handlers = OrderedDict()

    def _get_raw_stream(self):
        """
        Check whether files or STDIN is being used;
        return an iterator over all lines of the retrosheet
        """
        if self.filenames is not None:
            for fn in self.filenames:
                with open(fn) as retrosheet:
                    for line in retrosheet:
                        yield line
        else:
            for line in SYS.STDIN:
                yield line

    def _get_python_stream(self):
        """ Yield all lines in the retrosheet as Python objects """
        for line in self._get_raw_stream():
            yield pythonify_line(line)

    def register_handler(self, name, handler):
        """
        Register a handler for this analysis
        @param name - the name of this handler, for later reference when we go to fetch its' data
        @param handler - the handler object
        """
        self.handlers[name] = handler

    def fire_trigger(self, trigger):
        """
        When a handler returns a trigger, look for a method of this
        object with that name, and call it
        """
        getattr(self, trigger)()

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    
    def run(self):
        self.preprocess()
        
        for pyline in self._get_python_stream():
            for handler in self.handlers.values():
                trigger = handler.handle(pyline)
                if trigger:
                    self.fire_trigger(trigger)

        self.postprocess()
                

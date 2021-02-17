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
            raise ValueError("Use either @filename or @filenames, not both." + \
                             " Or send all data through STDIN and use neither.")
        
        if filenames:
            self.filenames = filenames
        elif filenames:
            self.filenames = [filename]
        else:
            self.filenames = None

        self.handlers = OrderedDict()
        self.stream = io.StringIO()

    def _retrosheet_as_filelike(self):
        """ Return the entire retrosheet as a single (lazily-loaded) file-like """
        def _yield_files(self):
            if self.filenames is not None:
                for fn in self.filenames:
                    with open(fn) as infile:
                        yield infile
            else:
                yield sys.stdin

        return itertools.chain(self._yield_files())
            
    def _get_python_stream(self):
        """ Yield all lines in the retrosheet as Python objects """
        reader = csv.reader(self._retrosheet_as_filelike())
        for line in reader:
            yield pythonify_line(line)
            
    # def _get_raw_stream(self):
    #     """
    #     Check whether files or STDIN is being used;
    #     return an iterator over all lines of the retrosheet
    #     """
    #     if self.filenames is not None:
    #         for fn in self.filenames:
    #             with open(fn) as retrosheet:
    #                 for line in retrosheet:
    #                     yield line
    #     else:
    #         for line in sys.stdin:
    #             yield line

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

    def fire_triggers(self, trigger_names):
        """
        When a handler returns a trigger, look for a trigger registered under
        the given names and call them
        """
        for trigger_name in trigger_names:
            self.triggers[trigger_name]()

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    
    def run(self):
        self.preprocess()
        
        for pyline in self._get_python_stream():
            triggers_to_fire = []
            for handler in self.handlers.values():
                new_trigger = handler.handle(pyline)
                if new_trigger:
                    triggers_to_fire.append(new_trigger)
            self.fire_triggers(trigger_to_fire)

        self.postprocess()
                

from retrosheet import event

class Handler(object):
    """
    Base class for handlers
    """
    @property
    def fcn_for(self):
        return {
            event.ID: self.handle_id,
            event.Start: self.handle_start,
            event.Sub: self.handle_sub,
            event.Play: self.handle_play,
            event.Info: self.handle_info,
            event.Com: self.handle_com,
            event.Version: self.handle_version,
        }

    def handle_id(self, _id):
        pass

    def handle_version(self, version):
        pass

    def handle_start(self, start):
        pass

    def handle_sub(self, sub):
        pass

    def handle_play(self, play):
        pass

    def handle_info(self, info):
        pass

    def handle_com(self, com):
        pass

    def handle(self, pyline):
        """ Pass the line off to the appropriate handling function """
        typ = type(pyline)
        return self.fcn_for[typ](pyline)

    def reset(self):
        """
        Resets the handler. Usually this means re-initializing all member
        data structures. Most handlers can do this by simply rerunning
        their constructor.

        This function mnust be called by the Analysis object after firing
        triggers for each game
        """
        self.__init__()

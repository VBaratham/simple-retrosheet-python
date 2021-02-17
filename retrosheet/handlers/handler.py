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
        }
    
    def handle_id(self, _id):
        pass

    def handle_start(self):
        pass

    def handle_sub(self):
        pass

    def handle_play(self):
        pass

    def handle_info(self):
        pass

    def handle_com(self):
        pass

    def handle(self, pyline):
        """ Pass the line off to the appropriate handling function """
        typ = type(pyline)
        return self.fcn_for[typ](pyline)

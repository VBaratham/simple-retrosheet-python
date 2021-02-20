from retrosheet import event
import logging as log

class Handler(object):
    """
    Base class for handlers
    """

    def __init__(self, *args, **kwargs):
        # True when we are in an error state:
        self.error = False
    
    @property
    def fcn_for(self):
        return {
            event.ID: self.handle_id,
            event.Version: self.handle_version,
            event.Start: self.handle_start,
            event.Sub: self.handle_sub,
            event.Play: self.handle_play,
            event.Info: self.handle_info,
            event.Data: self.handle_data,
            event.Com: self.handle_com,
            event.Padj: self.handle_padj,
            event.Badj: self.handle_badj,
            event.Radj: self.handle_radj,
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

    def handle_data(self, data):
        pass

    def handle_com(self, com):
        pass
    
    def handle_padj(self, badj):
        pass

    def handle_badj(self, badj):
        pass

    def handle_radj(self, radj):
        pass

    def handle(self, pyline):
        """ Pass the line off to the appropriate handling function """
        if not self.error:
            typ = type(pyline)
            return self.fcn_for[typ](pyline)
        else:
            log.debug("Not running b/c in error state: {}".format(pyline))

    def _enter_error(*args, **kwargs):
        """
        Base classes override this function with code to run when
        the handler errors.
        """
        pass

    def _exit_error(*args, **kwargs):
        """
        Base classes override this function with code to run when
        the handler's error is resolved.
        """
        pass

    def mark_error(self, *args, **kwargs):
        """
        When a handler errors, we continue running the analysis after
        calling this function to mark the handler as errored. Errored
        handlers do not run until the user script intervenes to resolve the
        error and calls handler.resolve_error() to confirm the resolution.
        """
        self.error = True
        self._enter_error(*args, **kwargs)

    def resolve_error(self, *args, **kwargs):
        self.error = False
        self._exit_error(*args, **kwargs)

    def reset(self):
        """
        Resets the handler. Usually this means re-initializing all member
        data structures. Most handlers can do this by simply rerunning
        their constructor. Note that any handler that takes arguments (e.g.
        GameTrigger) will need to overwrite this method

        This function mnust be called by the Analysis object after firing
        triggers for each game
        """
        self.__init__()

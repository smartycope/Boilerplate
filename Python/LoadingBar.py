from GuiScene import *
from pygame import freetype
from Animation import *

class LoadingBar:
    def __init__(self, surface, loc, finsihedFunc, *params, tasks=None, **kwparams):
        self.animation = Animation('other/loadingAnimation/', secondsPerLoop=5, scale=[240, 240])
        if tasks is None:
            self.length = self.animation.numFrames
        else:
            self.length = tasks

        self.surface = surface
        self.loc = loc

        self._progress = self.length
        self.finished = False

        self.func = finsihedFunc
        self.params = params
        self.kwparams = kwparams

    def progress(self, amount=None):
        if amount is None:
            amount = self.length / self.animation.numFrames

        self._progress -= amount

        if self._progress <= 0:
            self.finished = True
            self.func(*self.params, **self.kwparams)
            return True
        else:
            self.surface.blit(self.animation.animate(), [self.loc[0], self.loc[1]])
            pygame.display.flip()
            pygame.display.update()
            return False
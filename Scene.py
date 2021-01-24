from os import environ; environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"; import pygame
from Point import Pointf, Pointi
from pickle import dumps, loads
# from cPickle import dumps, loads
from time import localtime
from Cope import DIR, createFile
from os.path import join

class Scene:
    """ An Abstact Scene class.
        To initalize, override init().
        The only method that truely 'needs' to be overriden, is run(), which must return self._menu
        Events are handled by
    """

    defaultBackground = [20, 20, 20]
    savesPath = DIR + '/saves/'
    saveExtension = '.pkl'

    def __init__(self, surface, **params):
        self.mainSurface = surface
        self.updateMouse()
        self.fullscreen = False
        self.background = self.defaultBackground
        self.backgroundBlitOffset = [0, 0]

        # This is the directory in which the assets are loaded from
        self.dir = ''

        self.center = Pointf(self.mainSurface.get_rect().center)

        # This determines what menu to switch to.
        # Fill it with the name of the class
        self._menu = ''
        self.menuParams = params

        self.init(**params)

    def loadAsset(self, name, scale=None, extension='png'):
        if scale is None:
            return loadAsset(self.dir, name, extension)
        else:
            return pygame.transform.scale(loadAsset(self.dir, name, extension), scale)

    def init(self, **params):
        pass

    def run(self):
        """ The function that runs every frame. Must return self._menu!
        """
        raise NotImplementedError
        return self._menu

    def exit(self):
        pygame.quit()
        exit(0)

    def switchMenu(self, menu: str, **passParams):
        """ Switch to the menu specified with the *additional* keyword arguements specified
            at the end of the next frame
        """

        self._menu = menu
        self.menuParams.update(passParams)

    def save(self, dirpath=None, name=None):
        if dirpath is None:
            dirpath = self.savesPath

        if name is None:
            t = localtime()
            name = f'{t.tm_mon}-{t.tm_day}-{t.tm_year}@{t.tm_hour % 12}:{t.tm_min} ' \
                    + 'pm' if t.tm_hour / 12 else 'am' \
                    + self.saveExtension

        createFile(join(dirpath, name))
        tmp = self.serialize()
        f = open(join(dirpath, name), 'wb')
        f.write(tmp)
        print('Saved!')
        f.close()

    def load(self, name, dirpath=None):
        if dirpath is None:
            dirpath = self.savesPath

        with open(join(dirpath, name), 'rb') as f:
            self.deserialize(f)

    def serialize(self) -> bytes:
        return dumps(self.__dict__)

    def deserialize(self, string: bytes):
        self = self.__dict__.update(loads(string))




#* Some short 'ease of access' functions
    def showMouse(self, show: bool):
        pygame.mouse.set_visible(show)

    def setKeyRepeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def getSize(self):
        """ Returns (width, height) of self.mainSurface, which is ostenibly the size of the window
        """
        return self.mainSurface.get_size()

    def updateMouse(self):
        """ Update the mouse position in to self.mouseLoc
        """
        self.mouseLoc = Pointf(pygame.mouse.get_pos())

    def isHeld(self, key: str):
        """ To get mouse buttons, pass in 'mouse<num>'.
        """

        if 'mouse' in key:
            return pygame.mouse.get_pressed(5)[int(key[-1])-1]
        else:
            return pygame.key.get_pressed()[pygame.key.key_code(key)]


#* The various event handlers
    def handleEvent(self, event):
        pygame.event.pump()

        #* Exit the window
        if   event.type == pygame.QUIT:
            self.exit()

        #* Mouse moves
        elif event.type == pygame.MOUSEMOTION:
            self.updateMouse()
            self.mouseMotion()

        #* If the left mouse button is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouseLeftButtonDown()

        #* If the left mouse button is released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouseLeftButtonUp()

        #* Middle button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.mouseMiddleButtonDown()

        #* Middle button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.mouseMiddleButtonUp()

        #* Right mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.mouseRightButtonDown()

        #* Right mouse button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.mouseRightButtonUp()

        #* If a file is dropped into the window
        elif event.type == pygame.DROPFILE: #and event.file[-4:0] == '':
            self.fileDropped()

        # TODO: I don't belive these will work on windows.
        #* If you scroll up
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.scrollUp()

        #* If you scroll down
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.scrollDown()


        elif event.type == pygame.KEYDOWN:
            self.keyDown(event)


        elif event.type == pygame.KEYUP:
            self.keyUp(event)


        else:
            self.handleOtherEvent(event)

    def mouseLeftButtonDown(self):
        pass

    def mouseLeftButtonUp(self):
        pass

    def mouseRightButtonDown(self):
        pass

    def mouseRightButtonUp(self):
        pass

    def mouseMiddleButtonDown(self):
        self.updateMouse()
        print(self.mouseLoc)

    def mouseMiddleButtonUp(self):
        pass

    def mouseMotion(self):
        pass

    def fileDropped(self):
        pass

    def scrollUp(self):
        pass

    def scrollDown(self):
        pass

    def keyDown(self, event):
        # if event.key == pygame.K_f:
        #     self.fullscreen = not self.fullscreen
        return pygame.key.name(event.key)

    def keyUp(self, event):
        return pygame.key.name(event.key)

    def handleOtherEvent(self, event):
        pass

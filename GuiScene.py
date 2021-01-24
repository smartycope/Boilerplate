from Scene import *
from Elements import *
from Text import Text
import pygame_gui

class GuiScene(Scene):
    guiThemePath = DIR + 'data/other/myTheme.json'

    def __init__(self, surface, **params):
        self.uiManager = pygame_gui.UIManager(surface.get_size(), self.guiThemePath)
        self.elements = ()
        self.showMouse(True)
        self.setKeyRepeat(200, 20)
        self.background = self.uiManager.get_theme().get_colour('dark_bg')

        super().__init__(surface, **params)

        self.uiManager.set_window_resolution(self.getSize())
        self.uiManager.clear_and_reset()
        self.renderUI()


    def renderUI(self):
        raise NotImplementedError


    def handleEvent(self, event):
        for i in self.elements:
            i.handleEvent(event)

        super().handleEvent(event)

        self.uiManager.process_events(event)


    def run(self, deltaTime):
        self.uiManager.update(deltaTime)
        self.uiManager.draw_ui(self.mainSurface)
        return self._menu

from GuiScene import *
import pygame

class LandingMenu(GuiScene):
    def renderUI(self):
        self.background = None

        textSize = 50
        textLoc  = Pointi(self.center.x, self.center.y - 200)

        startButtonSize = [300, 100]
        startButtonLoc  = Pointi(self.center.x - startButtonSize[0] / 2, self.center.y + 200)

        aboutButtonSize = [150, 50]
        aboutButtonLoc  = Pointi(self.center.x - aboutButtonSize[0] / 2, self.center.y + 305)

        # toUpgradeButtonLoc  = Pointi(, 550)
        # toUpgradeButtonSize = respawnButtonSize

        self.text = Text('Welcome!', textLoc, size=textSize)

        self.elements += (
            Button(startButtonLoc, self.uiManager, 'Start', self.save, name='save.pkl', size=startButtonSize),
            Button(aboutButtonLoc, self.uiManager, 'About', self.load, name='save.pkl', size=aboutButtonSize),
        )

    def keyDown(self, event):
        key = super().keyDown(event)

        # if key == 'escape':
            # self.exit()
        # if key == 'enter' or key == 'return':
            # self.switchMenu('')


    def mouseMotion(self):
        if self.isHeld('mouse1'):
            # pygame.glfxdraw.pixel(self.mainSurface, *self.mouseLoc.data(), (255, 0, 0))
            # pygame.draw.circle(self.mainSurface, (255, 0, 0),  self.mouseLoc.data(), 1)
            self.mainSurface.set_at(self.mouseLoc.datai(), (255, 0, 0))



    def run(self, deltaTime):
        self.text.draw(self.mainSurface)
        return super().run(deltaTime)
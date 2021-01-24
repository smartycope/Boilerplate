from os import environ; environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"; import pygame

#* Scenes
from LandingMenu import LandingMenu


SCENES = (LandingMenu,)
STARTING_SCENE = LandingMenu

class Game:
    args = None
    fps  = 30
    startFullscreen = False
    startingScreen = 0

    def __init__(self, size=(None, None), title='Hello World!', args=None):
        self.args = args

        self.initPygame(size, title)

        #* Make a dict of "className": classType
        self.scenes = dict(zip([i.__name__ for i in SCENES], SCENES))

        startScene = STARTING_SCENE.__name__

        self.currentScene = self.scenes[startScene](self.mainSurface)
        self.sceneStack = [startScene]


    def run(self):
        while True:
            deltaTime = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                self.currentScene.handleEvent(event)


            sceneCommand = self.currentScene.run(deltaTime)

            if sceneCommand == '':
                pass
            elif sceneCommand == 'prev':
                # Because the last in the list is the current Scene
                self.sceneStack.pop()
                switchToScene = self.sceneStack.pop()

                self.currentScene = self.scenes[switchToScene](self.mainSurface, **self.currentScene.menuParams)
                self.sceneStack.append(switchToScene)
            else:
                self.sceneStack.append(sceneCommand)
                self.currentScene = self.scenes[sceneCommand](self.mainSurface, **self.currentScene.menuParams)

            pygame.display.flip()
            pygame.display.update()

            if type(self.currentScene.background) in [list, tuple, pygame.Color]:
                self.mainSurface.fill(self.currentScene.background)
            elif type(self.currentScene.background) == pygame.Surface:
                self.mainSurface.blit(self.currentScene.background, self.currentScene.backgroundBlitOffset, special_flags=pygame.BLEND_RGBA_SUB)
            elif self.currentScene.background is None:
                pass
            else:
                assert(False)


    def initPygame(self, size, title):
        #* Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        # pygame.mouse.set_visible(False)
        tmp = pygame.display.Info(); self.screenSize = (tmp.current_w, tmp.current_h)
        # pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(title)

        self.fullscreenWindowFlags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN | pygame.NOFRAME
        self.windowedWindowFlags   = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE

        if pygame.__version__ >= '2.0.0':
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.set_allow_screensaver(True)
            self.windowedWindowFlags = self.windowedWindowFlags | pygame.SCALED

        #* Set the icon
        # with open(DIR + 'data/' + self.settings['iconFile'], 'r') as icon:
        #     pygame.display.set_icon(pygame.image.load(icon))

        self.windowedSize = size
        if size[0] is None:
            self.windowedSize[0] = round(self.screenSize[0] / 1.5)
        if size[1] is None:
            self.windowedSize[1] = round(self.screenSize[1] / 1.5)

        if self.startFullscreen:
            self.mainSurface = pygame.display.set_mode(self.screenSize, self.fullscreenWindowFlags, display=self.startingScreen)
        else:
            self.mainSurface = pygame.display.set_mode(self.windowedSize, self.windowedWindowFlags, display=self.startingScreen)

        #* Get info about the graphics
        vidInfo = pygame.display.Info()
        if self.args.verbose:
            print('Backend video driver being used:', pygame.display.get_driver())
            print('The display is', 'not' if not vidInfo.hw else '', 'hardware accelerated')
            print('The display has', vidInfo.video_mem, 'MB of video memory')
            print('The current width and height of the window are:', (vidInfo.current_w, vidInfo.current_h))
            print('The width and height of the display is:', self.screenSize)

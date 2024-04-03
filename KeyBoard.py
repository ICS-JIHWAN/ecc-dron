import pygame

def init():
    pygame.init()
    screen = pygame.display.set_mode((360, 240))
    pygame.display.set_caption('Drone Control')

def getKey(keyName):
    result = False

    for events in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        result = True
    pygame.display.update()

    return result

def main():
    print(getKey('a'))

if __name__ == '__main__':
    init()
    while True:
        main()
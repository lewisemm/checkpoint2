import os
from people import fellow

# definitions for functionalities across the app


def clearScreen():
    ans = os.system('cls')

    if (ans != 0):
        os.system('clear')


def currentPath():
    path = os.path.dirname(os.path.dirname(__file__))

    return path


def mainMenu():
    print '-' * 80
    print '-' * 40, ' MAIN MENU ', '-' * 28
    print '-' * 80
    print ' ' * 80
    print '1. Allocate people to rooms.'
    print '2. Get list of allocations.'
    print '3. Print allocation list.'
    print '4. List unallocated people.'
    print '5. List people in a room.'
    print ' ' * 80
    print '0. Quit application.'
    print ' ' * 80
    print '-' * 80


def choosePersonMenu():
    print '-' * 80
    print '-' * 80
    print ' ' * 80
    print '1. Allocate Staff.'
    print '2. Allocate Fellow.'
    print ' ' * 80
    print '0. Exit sub-menu'
    print ' ' * 80
    print '-' * 80


def appOrTextFileMenu():
    print '-' * 80
    print '-' * 80
    print ' ' * 80
    print '1. Allocate through the app'
    print '2. Allocate through text file'
    print ' ' * 80
    print '0. Exit sub-menu'
    print ' ' * 80
    print '-' * 80


def chooseOfficeOrLivingMenu():
    print '-' * 80
    print '-' * 80
    print ' ' * 80
    print '1. Allocate Office.'
    print '2. Allocate Living space.'
    print ' ' * 80
    print '0. Exit sub-menu'
    print ' ' * 80
    print '-' * 80


def listRooms():
    print '-' * 80
    print '-' * 80
    print ' ' * 80
    print '1. Choose an Office.'
    print '2. Choose a Living space.'
    print ' ' * 80
    print '0. Exit sub-menu'
    print ' ' * 80
    print '-' * 80

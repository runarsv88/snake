from curses import wrapper
import curses
from enum import Enum
import time
from random import randint

class Direction(Enum):
    UP = 'k'
    DOWN = 'j' 
    LEFT = 'h'
    RIGHT = 'l'
    
    @classmethod
    def opposite(cls, key):
        if key == cls.UP.value:
            return cls.DOWN.value
        elif key == cls.DOWN.value:
            return cls.UP.value
        elif key == cls.LEFT.value:
            return cls.RIGHT.value
        elif key == cls.RIGHT.value:
            return cls.LEFT.value

    @classmethod
    def hasValue(cls, value):
        return (any(value == item.value for item in cls))

class Element:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move(self, key):
        if key == Direction.UP.value:
           self.y = self.y - 1
        elif key == Direction.DOWN.value:
           self.y = self. y + 1
        elif key == Direction.LEFT.value:
            self.x = self.x - 1
        elif key == Direction.RIGHT.value:
            self.x = self.x + 1
        return

class Snake:
    symbol = 'X'
    foodSymbol = 'O'
    rows = 30
    cols = 60

    def __init__(self):
        head = Element(3,6)
        self.head = head
        self.body = [Direction.LEFT.value, Direction.LEFT.value] 
        self.food = Element(3,10)
    
    def refresh(self, innerScreen):
        innerScreen.clear()
        innerScreen.insstr(self.head.y, self.head.x, self.symbol)
        body = Element(self.head.y, self.head.x) 
        counter = 0
        for char in reversed(self.body):
            body.move(char)
            innerScreen.addstr(body.y, body.x, self.symbol)
        innerScreen.addstr(self.food.y, self.food.x, self.foodSymbol)
        innerScreen.refresh()
        return

    def moveHead(self, key):
        if Direction.hasValue(key):
             if self.body[-1] != key:
                self.head.move(key)
                self.body.append(Direction.opposite(key))
                if self.head.y == self.food.y and self.head.x == self.food.x:
                    self.updateFood() 
                else:
                    self.body = self.body[1:]
        return

    def updateFood(self):
        randy = randint(1,self.rows-2)
        randx = randint(1,self.cols-1)
        self.food.y = randy
        self.food.x = randx
        
def main(stdscr):
    snake = Snake()
    rows = snake.rows
    cols = snake.cols
    stdscr.clear()
    curses.curs_set(0)

    for i in range(0, rows):
        stdscr.insstr(i, 0,'#')
        stdscr.insstr(i,cols,'#')
    for i in range(1, cols+1):
        stdscr.insstr(0,i,'#')
        stdscr.insstr(rows-1,i,'#')
    stdscr.refresh()
    innerScreen = curses.newwin(rows-2, cols-1,1,1)
    snake.refresh(innerScreen)
    h,w = innerScreen.getmaxyx()
    limit = 60
    counter = 0
    while True:
        counter = counter + 1
        key = innerScreen.getkey()
        snake.moveHead(key)
        snake.refresh(innerScreen)

    innerScreen.getkey()

wrapper(main)

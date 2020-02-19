#!/usr/bin/python2.7


'''
list all the commands in tmux and allow for them to be constructed
'''

from Tkinter import *  #Python 2
#from tkinter import *   #Python 3
from subprocess import call
import time
#import _thread
import functools
import math
import random

DOWN=u'\u2193'  # down arrow
DIVIDE=u'\u00f7'    #divide symbol
POW10="10"+u'\u02E3'
POW="y"+u'\u02E3'
E="e"+u'\u02E3'
SQUARE='x'+u'\u00B2'
ROOT=u'\u221A'+'x'
MOD='MOD'
PI=u'\u03C0'

DISPLAY_MODE_NORMAL=0
DISPLAY_MODE_FUNC=1
DISPLAY_MODE_ALT=2

def b3(txt):
    return [txt,txt,txt]

keys= [
    [['', '', ''],      [ROOT,'A', SQUARE], [E,'B',''],     [POW10,'C',''], [POW,'D',''],   ['1/x','E',''], ['7','',''], ['8','',''], ['9','',''], [DIVIDE, '','']],
    [['', '', ''],      ['avg','a','sdev'], ['MOD','b',PI], ['sin','c',''], ['cos','d',''], ['tan','e',''],  ['4','',''], ['5','',''], ['6','',''], ['*', '','']],
    [['', '', ''],      ['','',''],         ['','',''],     ['>>','','<<'], ['<>','','Rnd#'],   [DOWN,'',''],   ['1','',''], ['2','',''], ['3','',''], ['-', '','']],
    [b3('Quit'),        b3('Clear'),        b3('Func'),     b3('Alt'),      ['','',''],     ['Exe','',''],  ['0','',''], ['.','',''], ['-','',''], ['+', '','']],
]

class UserInterface(Frame):
    # 480 x 272
    def __init__(self, parent, logic):
        Frame.__init__(self, parent)
        parent.geometry("480x272")
        self.parent = parent
        self.app = logic
        self.limit = None
        self.input = None
        self.actions = {}
        self.buttons_by_row = [[], [], [], []]
        self.display_mode = DISPLAY_MODE_NORMAL
        self.init()
    def mkNumButton(self, obj, r, c):
        txt = keys[r][c][0]
        but = Button(obj, text=txt, width=1, command=lambda arg=txt, row=r, column=c : self.app.numButton(arg, row, column) )
        self.buttons_by_row[r].append(but)
        but.pack(side=LEFT)
        return but
    def mkCmdButton(self, obj, r, c, size=1):
        txt = keys[r][c][0]
        but = Button(obj, text=txt, width=size, command=lambda arg=txt, row=r, column=c : self.app.opButton(arg, row, column) )
        self.buttons_by_row[r].append(but)
        but.pack(side=LEFT)
        return but

    def showFunc(self):
        if self.display_mode == DISPLAY_MODE_NORMAL:
            for y in range(0,4):
                for x in range(0,10):
                    self.buttons_by_row[y][x]['text'] = keys[y][x][DISPLAY_MODE_FUNC]
                    if self.buttons_by_row[y][x]['text']=='Func':
                        self.buttons_by_row[y][x].configure(background='blue')
                        self.buttons_by_row[y][x].config(bg='blue')
                        self.buttons_by_row[y][x]['bg']='blue'
                        #self.buttons_by_row[y][x].update()
                        #self.buttons_by_row[y][x].flash()
                        self.buttons_by_row[y][x].pack()
                        print (self.buttons_by_row[y][x]['text'])
            self.display_mode=DISPLAY_MODE_FUNC
        elif self.display_mode==DISPLAY_MODE_FUNC:
            for y in range(0,4):
                for x in range(0,10):
                    self.buttons_by_row[y][x]['text'] = keys[y][x][DISPLAY_MODE_NORMAL]
            self.display_mode = DISPLAY_MODE_NORMAL

    def showAlt(self):
        if self.display_mode == DISPLAY_MODE_NORMAL:
            for y in range(0,4):
                for x in range(0,10):
                    self.buttons_by_row[y][x]['text'] = keys[y][x][DISPLAY_MODE_ALT]
            self.display_mode=DISPLAY_MODE_ALT
        elif self.display_mode==DISPLAY_MODE_ALT:
            for y in range(0,4):
                for x in range(0,10):
                    self.buttons_by_row[y][x]['text'] = keys[y][x][DISPLAY_MODE_NORMAL]
            self.display_mode = DISPLAY_MODE_NORMAL
    def clearInput(self):
        self.input.delete(0,END)   #clear out input field
    def appendInput(self, num):
        self.input.insert(INSERT, num)
    def turnInputNegative(self):
        raw = self.input.get() #get the input line for processing
        print(raw)
        try:
            num = float(raw)
            num = num * -1.0
            self.input.delete(0,END)   #clear out input field
            self.input.insert(0, num)
        except ValueError:
            pass
    def init(self):
        self.SQRT = "sqrt"
        self.parent.title("Pocket Calculator")
        self.parent.configure(bg='gray')
        
        head = Frame(self.parent)
        head.pack(fill=Y)
        sizeLabel = Label(head, text="Stack Calculator")
        sizeLabel.pack()
        self.input = Entry(head, width=52, borderwidth=1, relief="groove")
        self.input.pack()
        self.stackView = Text(head, height=7, width=67, borderwidth=1, relief="groove")
        self.stackView.pack()
        head.update()

        row3 = Frame(self.parent)
        row3.pack(fill=X)
        for x in range(0,10):
            if 0<=x and x<6:
                self.mkCmdButton(row3, 0, x, 3)
            elif x<=x and x<9:
                self.mkNumButton(row3, 0, x)
            elif x==9:
                self.mkCmdButton(row3, 0, 9)
#         self.mkCmdButton(row3, 0, 0, "", 3)
#         self.mkCmdButton(row3, 0, 1, ROOT, 3)
#         self.mkCmdButton(row3, 0, 2, E, 3)
#         self.mkCmdButton(row3, 0, 3, POW10, 3)
#         self.mkCmdButton(row3, 0, 4, POW, 3)
#         self.mkCmdButton(row3, 0, 5, "1/x", 3)
#         self.mkNumButton(row3, 0, 6, "7")
#         self.mkNumButton(row3, 0, 7, "8")
#         self.mkNumButton(row3, 0, 8, "9")
#         self.mkCmdButton(row3, 0, 9, DIVIDE)
        row3.update()
        
        row2 = Frame(self.parent)
        row2.pack(fill=X)
        for x in range(0,10):
            if 0<=x and x<6:
                self.mkCmdButton(row2, 1, x, 3)
            elif x<=x and x<9:
                self.mkNumButton(row2, 1, x)
            elif x==9:
                self.mkCmdButton(row2, 1, 9)
#         self.mkCmdButton(row2, 1, 0, "sdev", 3)
#         self.mkCmdButton(row2, 1, 1, "avg", 3)
#         self.mkCmdButton(row2, 1, 2, MOD, 3)
#         self.mkCmdButton(row2, 1, 3, "sin", 3)
#         self.mkCmdButton(row2, 1, 4, "cos", 3)
#         self.mkCmdButton(row2, 1, 5, "tan", 3)
#         self.mkNumButton(row2, 1, 6, "4")
#         self.mkNumButton(row2, 1, 7, "5")
#         self.mkNumButton(row2, 1, 8, "6")
#         self.mkCmdButton(row2, 1, 9, "*")
        row2.update()

        row1 = Frame(self.parent)
        row1.pack(fill=X)
        for x in range(0,10):
            if 0<=x and x<6:
                self.mkCmdButton(row1, 2, x, 3)
            elif x<=x and x<9:
                self.mkNumButton(row1, 2, x)
            elif x==9:
                self.mkCmdButton(row1, 2, 9)
#         self.mkCmdButton(row1, 2, 0, "", 3)
#         self.mkCmdButton(row1, 2, 1, "", 3)
#         self.mkCmdButton(row1, 2, 2, "<<", 3)
#         self.mkCmdButton(row1, 2, 3, ">>", 3)
#         self.mkCmdButton(row1, 2, 4, "<>", 3)
#         self.mkCmdButton(row1, 2, 5, DOWN, 3)
#         self.mkNumButton(row1, 2, 6, "1")
#         self.mkNumButton(row1, 2, 7, "2")
#         self.mkNumButton(row1, 2, 8, "3")
#         self.mkCmdButton(row1, 2, 9, "-")
        row1.update()
        
        row0 = Frame(self.parent)
        row0.pack(fill=X)
        for x in range(0,10):
            if 0<=x and x<6:
                self.mkCmdButton(row0, 3, x, 3)
            elif x<=x and x<9:
                self.mkNumButton(row0, 3, x)
            elif x==9:
                self.mkCmdButton(row0, 3, 9)
#         self.mkCmdButton(row0, 3, 0, "Quit", 3)
#         self.mkCmdButton(row0, 3, 1, "Clear", 3)
#         self.mkCmdButton(row0, 3, 2, "Func", 3)
#         self.mkCmdButton(row0, 3, 3, "Alt", 3)
#         self.mkCmdButton(row0, 3, 4, "", 3)
#         self.mkCmdButton(row0, 3, 5, "Exe", 3)
#         self.mkNumButton(row0, 3, 6, "0")
#         self.mkNumButton(row0, 3, 7, ".")
#         self.mkNumButton(row0, 3, 8, "-")
#         self.mkCmdButton(row0, 3, 9, "+")
        row0.update()
   
        self.parent.geometry("480x271")
        self.parent.update()
        self.parent.geometry("480x272")
        
        for y in self.buttons_by_row:
            for x in y:
                pass
                #print(x['text'])
        #for y in range(0,len(self.buttons_by_row)):
        #    for x in range(0,len(self.buttons_by_row[y])):
        #        print (self.buttons_by_row[y][x][text])
    def fillList(self, list):
        pass

class AppLogic():
    def __init__(self, ui, verbose=False):
        self.view = ui
        self.stack = []
        self.memory = {}
        self.verbose = verbose
        self.mode = DISPLAY_MODE_NORMAL
        self.button_labels = {ROOT:[SQUARE,'']}

        
    #def enterButton(self):
    #    print(self.view.input.text)
    def cmdMakeNegative(self):
        self.view.turnInputNegative()
    def cmdAlt(self):
        if self.mode==DISPLAY_MODE_NORMAL:
            self.mode=DISPLAY_MODE_ALT
            self.view.showAlt()
        elif self.mode==DISPLAY_MODE_ALT:
            self.mode=DISPLAY_MODE_NORMAL
            self.view.showAlt()
    def cmdFunc(self):
        if self.mode==DISPLAY_MODE_NORMAL:
            self.mode=DISPLAY_MODE_FUNC
            self.view.showFunc()
        elif self.mode==DISPLAY_MODE_FUNC:
            self.mode=DISPLAY_MODE_NORMAL
            self.view.showFunc()
    def opButton(self, op, row, column):
        #TODO: if number is on input, processes it here
        op = keys[row][column][self.mode]
        if op in ['Rnd#', PI]:
            self.cmdAdditiveMath(op)
        if op in [E, "log", ROOT, SQUARE, "log2", "log10", POW10, "1/x", "sin", "cos", "tan"]:
            self.cmdUnaryMath(op)
        elif op in [POW, MOD]:
            self.cmdBinaryMath(op)
        elif len(op)==1 and (("a" <= op and op <= 'z') or ("A" <= op and op <= 'Z')):
            key = op.upper()
            if "a" <= op and op <= 'z':
                self.stack.append(self.memory[key])
                self.displayStack()
                #print("stack: {}".format(self.stack))
            if "A" <= op and op <= 'Z':
                self.memory[key] = self.stack[len(self.stack)-1]
                self.displayStack()
        else:
            switcher = {
                "Quit": self.cmdQuit,
                "Clear": self.clearInput,
                "Func": self.cmdFunc,
                "Alt": self.cmdAlt,
                "avg": self.cmdAvg,
                "sdev": self.cmdStandardDeviation,
                DOWN: self.cmdDropTop,
                "<>": self.cmdSwapTop2,
                ">>": self.cmdRotateRight,
                "<<": self.cmdRotateLeft,
                DIVIDE: self.cmdDiv,
                "*": self.cmdTimes,
                "-": self.cmdMinus,
                "+": self.cmdPlus,
                "Exe": self.cmdExec,
            }
            func = switcher.get(op, lambda: "unknown command")
            func() 

    def numButton(self, num, row, column):
        if num=="-":
            self.view.turnInputNegative()
        else:
            self.view.input.insert(INSERT, num)
    
    def displayStack(self):
        out = str(self.stack) + "\n"
        if self.view != None and self.view.stackView != None:
            if len(self.memory)>0:
                self.view.stackView.insert("1.0", str(self.memory) + "\n")
            self.view.stackView.insert("1.0", out)
        if self.verbose == True:
            if len(self.stack)>0:
                print("stack: {}".format(self.stack))
            if len(self.memory)>0:
                print("mem: {}".format(self.memory))
    def clearInput(self):
        self.view.clearInput()

    #commands on different lines, process each math line
    #45:4 +:3 => 45 45 45 45 + + +
    def processLine(self, raw):
        lines = raw.split("\n")
        oneline = lines[0]
        words = oneline.split(" ")
        for word in words:
            self.processWord(word)
    #one math 'word' from the math line, could have multipliers = 2:3 or *:2
    #45:4 => 45 45 45 45
    def processWord(self, word):
        line = None
        parts = word.split(":")
        value = parts[0]
        count = 1           #assume at least once
        if len(parts)>=2:
            try:
                count = int(parts[1])
            except ValueError:
                print(part[1] + " is not a valid multiplyer")
        for x in range(0, count):
            self.processTheChunk(value)
    #could be a numer or a command
    def processTheChunk(self, raw):
        try:
            #try to process as number
            line = float(raw)
            self.stack.append(line)
            self.displayStack()
            self.clearInput()
        except ValueError:
            #process as command
            self.opButton(raw)
        #print("stack: {}".format(self.stack))
    
    #mark - Calculation Actions
    def cmdExec(self):
        raw = self.view.input.get() #get the input line for processing
        if len(raw)>0:
            self.processLine(raw)
            self.clearInput()
    def cmdQuit(self):
        quit()
    #mark - stack operations
    def cmdDropTop(self):
        if len(self.stack)>=1:
            x = self.stack.pop()
            self.displayStack()
            #print("stack: {}".format(self.stack))
    def cmdSwapTop2(self):
        if len(self.stack)>=2:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(right)
            self.stack.append(left)
            self.displayStack()
            #print("stack: {}".format(self.stack))
    def cmdRotateRight(self):
        if len(self.stack)>=2:
            last = self.stack.pop()
            self.stack.insert(0, last)
            self.displayStack()
            #print("stack: {}".format(self.stack))
    
    def cmdRotateLeft(self):
        if len(self.stack)>=2:
            last = self.stack.pop(0)
            self.stack.append(last)
            self.displayStack()
            #print("stack: {}".format(self.stack))
    #mark - basic math operations
    def cmdDiv(self):
        if len(self.stack)>=2:
            right = self.stack.pop()
            left = self.stack.pop()
            ans = float(left) / float(right)
            self.stack.append(ans)
            self.displayStack()
            #print("stack: {}".format(self.stack))
    def cmdTimes(self):
        if len(self.stack)>=2:
            right = self.stack.pop()
            left = self.stack.pop()
            ans = left * right
            self.stack.append(ans)
            self.displayStack()
    def cmdMinus(self):
        if len(self.stack)>=2:
            right = self.stack.pop()
            left = self.stack.pop()
            ans = left - right
            self.stack.append(ans)
            self.displayStack()
    def cmdPlus(self):
        if len(self.stack)>=2:
            right = self.stack.pop()
            left = self.stack.pop()
            ans = left + right
            self.stack.append(ans)
            self.displayStack()
    #mark - complex math operations
    def cmdAvg(self):
        if len(self.stack)>=2:
            sum = 0
            count = 0
            while len(self.stack)>0:
                sum = sum + self.stack.pop()
                count = count + 1
            avg = sum/count
            self.stack.append(avg)
            self.displayStack()
    def cmdStandardDeviation(self):
        if len(self.stack)>=2:
            sum = 0.0
            sd = 0.0
            count = float(len(self.stack))
            
            #find average
            for x in self.stack:
                sum += x
            mean = sum / count
            
            while len(self.stack):
                sd += math.pow( self.stack.pop()-mean, 2)
            sd = math.sqrt( sd / count)
            self.stack.append(sd)
            self.displayStack()

    def cmdBinaryMath(self, cmd):
        if len(self.stack)>=2:
            x = self.stack.pop()
            y = self.stack.pop()
            if cmd==None:
                pass
            elif cmd==POW:
                ans = math.pow(y, x)
            elif cmd==MOD:
                #ans = y % x
                ans = fmod(x, y)
            elif cmd=="foo":
                pass
            self.stack.append(ans)
            self.displayStack()
    def cmdUnaryMath(self, cmd):
        if len(self.stack)>=1:
            x = self.stack.pop()
            ans = None
            if cmd==E:
                ans = math.exp(x)
            elif cmd=="log":
                ans = math.log(x)
            elif cmd==ROOT:
                print ('in root')
                ans = math.sqrt(x)
            elif cmd=="log2":
                ans = math.log(x, 2.0)
            elif cmd=="log10":
                ans = math.log10(x)
            elif cmd==POW10:
                ans = math.pow(10.0, x)
            elif cmd==SQUARE:
                print ('in square')
                ans = math.pow(x, 2.0) 
            elif cmd=="1/x":
                ans = 1.0 / x
            elif cmd=="sin":
                ans = math.sin(math.radians(x))
            elif cmd=="cos":
                ans = math.cos(math.radians(x))
            elif cmd=="tan":
                ans = math.tan(math.radians(x))
            
            self.stack.append(ans)
            self.displayStack()
    def cmdAdditiveMath(self, cmd):
        if cmd=='Rnd#':
            self.stack.append(random.random())
            self.displayStack()
        elif cmd==PI:
            self.stack.append(math.pi)
            self.displayStack()
def main():
    master = Tk()
    app=AppLogic(None)
    ui=UserInterface(master, app)
    app.view = ui

    for arg in sys.argv:
        parts = arg.split("=")
        if len(parts)>1:
            if parts[0]=="-e" or parts[0]=="--equation":
                app.view.input.insert(INSERT, parts[1])
        elif len(parts)==1:
            if arg=="-v" or arg=="--verbose":
                app.verbose = True

    master.update()
    master.mainloop()

if __name__ == "__main__":
    main()

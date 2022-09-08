import curses,sys

CENTER = 'center'
LEFT = 'left'
RIGHT = 'right'
BOTTOM = 'bottom'
TOP = 'top'

class TerminalButtons:
    
    def assignList(self,aa,ab,h,c):
        #list with all objs coords (first char,last,height)
        self.Buttons[str(self.countObj)] = [aa,ab,h,c]

    def CreateButton(self,positionx='left',positiony='top',fg=curses.COLOR_WHITE,bg=curses.COLOR_BLACK,commmand=None,text='test',row=0,col=0,typeText=curses.A_CHARTEXT):
        curses.init_pair(self.countObj, fg, bg)

        hm, wm = self.std.getmaxyx()
        
        if positionx == 'center':
            w = wm//2
            w = w - len(text)//2 + col
        if positiony == 'center':
            h = hm//2 + row
        if positionx == 'left':
            w = 0 + col
        if positiony == 'top':
            h = 0 + row
        if positionx == 'right':
            w = wm - len(text) + col
        if positiony == 'bottom':
            h = hm - 1 + row

            
        self.std.attron(curses.color_pair(self.countObj) | typeText)
        self.std.addstr(h, w, text)
        self.std.attroff(curses.color_pair(self.countObj) | typeText)

        finalt = w + len(text)
        self.assignList(w,finalt,h,commmand)
        self.countObj = self.countObj + 1

    def ReqInput(self, x, y):
        curses.echo()
        curses.nocbreak() 
        self.std.refresh()
        input = self.std.getstr(x, y)

        #self.CreateButton(color=curses.COLOR_CYAN,text=input)
        curses.noecho()
        curses.cbreak()
        return input.decode('utf-8')

    def AddKeyEvent(self,key,func):
        self.events[str(self.countObj)] = [key,func]
        self.countObj = self.countObj + 1

    def ConfigureBg(self,bg=curses.COLOR_BLUE,fg=curses.COLOR_WHITE):
        curses.init_pair(self.countObj, fg, bg)
        self.std.bkgd(' ', curses.color_pair(self.countObj) )
        self.countObj = self.countObj + 1

    def mainLoop(self):
        while self.running:
            self.std.refresh()
            key = self.std.getch()

            for j in self.events:
                event = self.events[j]
                if event[0] == key:
                    event[1]()

            if key == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()
                
                buttons = self.Buttons
                try:
                    for i in buttons:
                        obj = self.Buttons[i]
                        aa,ab,h,c = obj

                        if y == h and x in range(aa,ab):
                            if c != None:
                                c()
                except:pass
        
            elif key == 27:
                sys.exit()
                
    def ClearScreen(self):
        self.std.clear()
        self.Buttons = {}

    def GetMaxYX(self):
        return self.std.getmaxyx()

    def Exit(self):
        self.running = False

    def __init__(self,std,cursor=0):
        self.Buttons = {}
        self.countObj = 1
        self.events = {}
        self.std = std
        self.running = True
        curses.curs_set(cursor)
        curses.mousemask(1)



if __name__ == '__main__':
    def testInput(Tb:TerminalButtons):
        inputs = Tb.ReqInput(1,1)
        Tb.ConfigureBg()
        Tb.CreateButton(positionx=CENTER,positiony=CENTER,bg=curses.COLOR_GREEN,text='You writed: %s' % inputs,row=2,commmand=lambda:[testInput(Tb)])

    def EventTest(Tb:TerminalButtons):
        Tb.CreateButton(text='You pressed KeyUp',fg=curses.COLOR_GREEN)

    def main(stdscr):

        Tb = TerminalButtons(stdscr)
        Tb.AddKeyEvent(curses.KEY_UP,lambda:EventTest(Tb))
        
        y = Tb.GetMaxYX()[1]
        a = ' ' + '=' * (y-2)
        Tb.CreateButton(text=a,fg=curses.COLOR_GREEN)
        Tb.CreateButton(text=a,fg=curses.COLOR_GREEN,positiony=BOTTOM)

        Tb.CreateButton(text='blink',fg=curses.COLOR_GREEN,positiony=BOTTOM,positionx=CENTER,typeText=curses.A_BLINK,row=-1)
        Tb.CreateButton(text='bold',fg=curses.COLOR_GREEN,positiony=TOP,positionx=CENTER,typeText=curses.A_BOLD,row=1)

        Tb.CreateButton(positiony=CENTER,positionx=CENTER,fg=curses.COLOR_BLUE,text='center')
        Tb.CreateButton(positiony=TOP,positionx=CENTER,fg=curses.COLOR_BLUE,text='top')
        Tb.CreateButton(positiony=BOTTOM,positionx=CENTER,fg=curses.COLOR_BLUE,text='bottom')
        Tb.CreateButton(positiony=CENTER,positionx=RIGHT,fg=curses.COLOR_BLUE,text='right')
        Tb.CreateButton(positiony=CENTER,positionx=LEFT,fg=curses.COLOR_BLUE,text='left')
        
        Tb.CreateButton(positionx=CENTER,positiony=CENTER,bg=curses.COLOR_GREEN,text='Click for Input',row=2,commmand=lambda:[testInput(Tb)])
        Tb.CreateButton(positionx=CENTER,positiony=CENTER,bg=curses.COLOR_RED,text='Clear',row=3,commmand=Tb.ClearScreen)

        Tb.mainLoop()

    curses.wrapper(main)
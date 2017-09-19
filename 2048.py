# -*- coding: utf-8 -*-

#Importing libraries to be used
import wx 
import os
import random
import copy

# creating the user interface frame that the user will interact with and perform actions that will have an appropriate response
class Frame(wx.Frame):
    def __init__(self,title):
        #created a default toolbar of application with a resizeable option and minimize box 
        super(Frame,self).__init__(None,-1,title,
                style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER)
        #Setting different colours for each tile in the game
        self.colors = {0:(204,192,179),2:(238, 228, 218),4:(237, 224, 200),
                8:(242, 177, 121),16:(245, 149, 99),32:(246, 124, 95),
                64:(246, 94, 59),128:(237, 207, 114),256:(237, 207, 114),
                512:(237, 207, 114),1024:(237, 207, 114),2048:(237, 207, 114),
                4096:(237, 207, 114),8192:(237, 207, 114),16384:(237, 207, 114),
                32768:(237, 207, 114),65536:(237, 207, 114),131072:(237, 207, 114),
                262144:(237, 207, 114),524288:(237, 207, 114),1048576:(237, 207, 114),
                2097152:(237, 207, 114),4194304:(237, 207, 114),
                8388608:(237, 207, 114),16777216:(237, 207, 114),
                33554432:(237, 207, 114),67108864:(237, 207, 114),
                134217728:(237, 207, 114),268435456:(237, 207, 114),
                536870912:(237, 207, 114),1073741824:(237, 207, 114),
                2147483648:(237, 207, 114),4294967296:(237, 207, 114),
                8589934592:(237, 207, 114),17179869184:(237, 207, 114),
                34359738368:(237, 207, 114),68719476736:(237, 207, 114),
                137438953472:(237, 207, 114),274877906944:(237, 207, 114),
                549755813888:(237, 207, 114),1099511627776:(237, 207, 114),
                2199023255552:(237, 207, 114),4398046511104:(237, 207, 114),
                8796093022208:(237, 207, 114),17592186044416:(237, 207, 114),
                35184372088832:(237, 207, 114),70368744177664:(237, 207, 114),
                140737488355328:(237, 207, 114),281474976710656:(237, 207, 114),
                562949953421312:(237, 207, 114),1125899906842624:(237, 207, 114),
                2251799813685248:(237, 207, 114),4503599627370496:(237, 207, 114),
                9007199254740992:(237, 207, 114),18014398509481984:(237, 207, 114),
                36028797018963968:(237, 207, 114),72057594037927936:(237, 207, 114)}
     #Initalize game           
        self.setIcon()
        self.initGame()
    #Displays game and provides settings to move the tiles
        panel = wx.Panel(self)
        panel.Bind(wx.EVT_KEY_DOWN,self.onKeyDown)
        panel.SetFocus()
        self.initBuffer()
        self.Bind(wx.EVT_SIZE,self.onSize) 
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_CLOSE,self.onClose)
        self.SetClientSize((505,720))
        self.Center()
        self.Show()
    #Puts on board so user can see
    def onPaint(self,event):
        dc = wx.BufferedPaintDC(self,self.buffer)
    # Saves score and terminates when closed
    def onClose(self,event):
        self.saveScore()
        self.Destroy()
    #   putting icon on toolbar
    def setIcon(self):
        icon = wx.Icon("icon.ico",wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
     #Opens previous game and loads and updates score
    def loadScore(self):
        if os.path.exists("bestscore.ini"):
            ff = open("bestscore.ini")
            self.bstScore = ff.read()
            ff.close()
     #Saves score and writes to file so it may be opened later
    def saveScore(self):
        ff = open("bestscore.ini","w")
        ff.write(str(self.bstScore))
        ff.close()
     #Initalize game so when it opens it displays text, score and all data needed for the game
    def initGame(self):
        self.bgFont = wx.Font(50,wx.SWISS,wx.NORMAL,wx.BOLD,face=u"Roboto")
        self.scFont = wx.Font(36,wx.SWISS,wx.NORMAL,wx.BOLD,face=u"Roboto")
        self.smFont = wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,face=u"Roboto")
        self.curScore = 0
        self.bstScore = 0
        self.loadScore()
        # 4 rows and 4 coloums for tiles ( using arrays because it easily represents system used )
        self.data = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        # First 2 tile inialized if 1 tile it must be 2 but if 2 tiles connected then its 4
        while count<2: 
            row = random.randint(0,len(self.data)-1) 
            col = random.randint(0,len(self.data[0])-1)
            if self.data[row][col]!=0: continue           
            self.data[row][col] = 2 if random.randint(0,1) else 4
            count += 1
         # empty bitmap to put pixels in for game   
    def initBuffer(self):
        w,h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w,h)
        #Displays all drawings to the screen
    def onSize(self,event):
        self.initBuffer()
        self.drawAll()
        #Placing tiles on screen and multiplying by 2 if 2 tiles interact with one another(game logic) 
    def putTile(self):
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col]==0: available.append((row,col)) # add tile if empty square
        if available:
            row,col = available[random.randint(0,len(available)-1)]
            self.data[row][col] = 2 if random.randint(0,1) else 4 
            return True
        return False
    def update(self,vlist,direct): # updates score and game tiles 
        score = 0
        if direct: #up or left
            i = 1
            while i<len(vlist): 
                # if 2 tiles of equal value mesh upward it multiples the values and deletes the ith number (2 squares = 1 square)
                if vlist[i-1]==vlist[i]:
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1] # Adds multiplied value to score 
                    i += 1
                i += 1
        else:
            #direction moved downward same thing as above but different direction
            i = len(vlist)-1
            while i>0:
                if vlist[i-1]==vlist[i]:
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1]
                    i -= 1
                i -= 1      
        return score
        # The calucation and keeping logs of data for score (upward and downward movements)
    def slideUpDown(self,up):
        score = 0
        numCols = len(self.data[0])
        numRows = len(self.data)
        oldData = copy.deepcopy(self.data)
        
        for col in range(numCols):
            cvl = [self.data[row][col] for row in range(numRows) if self.data[row][col]!=0]
            if len(cvl)>=2:
                score += self.update(cvl,up)
            for i in range(numRows-len(cvl)):
                if up: cvl.append(0)
                else: cvl.insert(0,0)
            for row in range(numRows): self.data[row][col] = cvl[row]
        return oldData!=self.data,score
    
    # The calucation and keeping logs of data for score (right and left movements)
    def slideLeftRight(self,left):
        score = 0
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)
        
        for row in range(numRows):
            rvl = [self.data[row][col] for col in range(numCols) if self.data[row][col]!=0]
            if len(rvl)>=2:           
                score += self.update(rvl,left)
            for i in range(numCols-len(rvl)):
                if left: rvl.append(0)
                else: rvl.insert(0,0)
            for col in range(numCols): self.data[row][col] = rvl[col]
        return oldData!=self.data,score
    def isGameOver(self):
        copyData = copy.deepcopy(self.data)
        
        flag = False # Tile is not moveable or you have lost if all tiles cant move any pieces up,down, left or right 
        if not self.slideUpDown(True)[0] and not self.slideUpDown(False)[0] and \
                not self.slideLeftRight(True)[0] and not self.slideLeftRight(False)[0]:
            flag = True #continue playing and copydata 
        if not flag: self.data = copyData
        return flag
  # Game logic to see if you can make a move or end the game
    def doMove(self,move,score):
        # if you can move put a tile and update change
        if move:
            self.putTile()
            self.drawChange(score)
            # if game is over put a message box and update best score if its the new best score
            if self.isGameOver():
                if wx.MessageBox(u"游戏结束，是否重新开始？",u"哈哈",
                        wx.YES_NO|wx.ICON_INFORMATION)==wx.YES:
                    bstScore = self.bstScore
                    self.initGame()
                    self.bstScore = bstScore
                    self.drawAll()
                    
    # when you click a directon for the tile to move, it moves in the appropriate direction
    def onKeyDown(self,event):
        keyCode = event.GetKeyCode()
                
        if keyCode==wx.WXK_UP:
            self.doMove(*self.slideUpDown(True))
        elif keyCode==wx.WXK_DOWN:
            self.doMove(*self.slideUpDown(False))
        elif keyCode==wx.WXK_LEFT:
            self.doMove(*self.slideLeftRight(True))
        elif keyCode==wx.WXK_RIGHT:
            self.doMove(*self.slideLeftRight(False))        
                
     # Creates background for the game board
    def drawBg(self,dc):
        dc.SetBackground(wx.Brush((250,248,239)))
        dc.Clear()
        dc.SetBrush(wx.Brush((187,173,160)))
        dc.SetPen(wx.Pen((187,173,160)))
        dc.DrawRoundedRectangle(15,150,475,475,5)
        #Creates a 2048 logo
    def drawLogo(self,dc):
        dc.SetFont(self.bgFont)
        dc.SetTextForeground((119,110,101))
        dc.DrawText(u"2048",15,26)
        # provides text to screen (Chinese text)
    def drawLabel(self,dc):
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119,110,101))
        dc.DrawText(u"合并相同数字，得到2048吧!",15,114)
        dc.DrawText(u"怎么玩: \n用-> <- 上下左右箭头按键来移动方块. \
                \n当两个相同数字的方块碰到一起时，会合成一个!",15,639)
        # Displays score to screen 
    def drawScore(self,dc):            
        dc.SetFont(self.smFont)
        scoreLabelSize = dc.GetTextExtent(u"SCORE")
        bestLabelSize = dc.GetTextExtent(u"BEST")
        curScoreBoardMinW = 15*2+scoreLabelSize[0]
        bstScoreBoardMinW = 15*2+bestLabelSize[0]
        curScoreSize = dc.GetTextExtent(str(self.curScore))
        bstScoreSize = dc.GetTextExtent(str(self.bstScore))
        curScoreBoardNedW = 10+curScoreSize[0]
        bstScoreBoardNedW = 10+bstScoreSize[0]
        curScoreBoardW = max(curScoreBoardMinW,curScoreBoardNedW)
        bstScoreBoardW = max(bstScoreBoardMinW,bstScoreBoardNedW)
        dc.SetBrush(wx.Brush((187,173,160)))
        dc.SetPen(wx.Pen((187,173,160)))
        dc.DrawRoundedRectangle(505-15-bstScoreBoardW,40,bstScoreBoardW,50,3)
        dc.DrawRoundedRectangle(505-15-bstScoreBoardW-5-curScoreBoardW,40,curScoreBoardW,50,3)
        dc.SetTextForeground((238,228,218))
        dc.DrawText(u"BEST",505-15-bstScoreBoardW+(bstScoreBoardW-bestLabelSize[0])/2,48)
        dc.DrawText(u"SCORE",505-15-bstScoreBoardW-5-curScoreBoardW+(curScoreBoardW-scoreLabelSize[0])/2,48)
        dc.SetTextForeground((255,255,255))
        dc.DrawText(str(self.bstScore),505-15-bstScoreBoardW+(bstScoreBoardW-bstScoreSize[0])/2,68)
        dc.DrawText(str(self.curScore),505-15-bstScoreBoardW-5-curScoreBoardW+(curScoreBoardW-curScoreSize[0])/2,68)
    # Put rounded rectangular tiles on screen
    def drawTiles(self,dc):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]
                if value==2 or value==4:
                    dc.SetTextForeground((119,110,101))
                else:
                    dc.SetTextForeground((255,255,255))
                dc.SetBrush(wx.Brush(color))
                dc.SetPen(wx.Pen(color))
                dc.DrawRoundedRectangle(30+col*115,165+row*115,100,100,2)
                size = dc.GetTextExtent(str(value))
                while size[0]>100-15*2: # changes font size based on number within tile
                    self.scFont = wx.Font(self.scFont.GetPointSize()*4/5,wx.SWISS,wx.NORMAL,wx.BOLD,face=u"Roboto")
                    dc.SetFont(self.scFont)
                    size = dc.GetTextExtent(str(value))
                if value!=0: dc.DrawText(str(value),30+col*115+(100-size[0])/2,165+row*115+(100-size[1])/2)
    # Draws everything to the screen
    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
        self.drawBg(dc)
        self.drawLogo(dc)
        self.drawLabel(dc)
        self.drawScore(dc)
        self.drawTiles(dc)
    # Calculates current score and checks if it is the best score and if so updates    
    def drawChange(self,score):
        dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
        if score:
            self.curScore += score
            if self.curScore > self.bstScore:
                self.bstScore = self.curScore
            self.drawScore(dc)
        self.drawTiles(dc)
     # Shows creator info
if __name__ == "__main__":
    app = wx.App()
    Frame(u"2048 v1.0.1 by Guolz")
    app.MainLoop()

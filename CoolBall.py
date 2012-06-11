""" 
CoolBall.py
Created on 2012-6-9

@author: YangGuozheng
"""
import sys 
import random 
import time
from PyQt4 import QtCore, QtGui 


class position(object):
    def __init__(self, x,y, color,have_ball, left, right, up, down):
        self.x = x
        self.y = y
        self.color = color
        self.have_ball = have_ball #(None,0 -6)
        self.left = left
        self.right = right
        self.up = up
        self.down =  down
        self.searched = 0
        
    def clear_data(self): 
        self.color = None
        self.have_ball = None
        self.searched = 0
        
    def __iaddr__(self, other):
        self.color = other.color
        self.have_ball = other.have_ball
        
class CoolBall(QtGui.QMainWindow):
    def __init__(self): 
        QtGui.QMainWindow.__init__(self) 
        self.setGeometry(300, 300, 490, 390) 
        self.setWindowTitle('Francy') 
        self.statusbar = self.statusBar() 
        self.center() 
        self.setFixedSize(490, 390)
        self.setWindowFlags(self.windowFlags()  & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.color_list = [0xFFB6C1,0xDC143C,0xFFD700, 0x00008B, 0x87CEEB, 0x008000,0x808080]
                              #LightPink, Crimson,  Yellow, DarkBlue,  SkyBlue , green,DimGray
        self.board_margin = 15
        self.row_column = 9
        self.position_list = []
        self.have_ball_list = []
        self.no_ball_list = range(81)
        self.chose_ball = None
        self.score = 0
        self.clear_up_list = []
        self.init_position_list()
        
    def center(self): 
        screen = QtGui.QDesktopWidget().screenGeometry() 
        size =  self.geometry() 
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2) 

    def init_position_list(self):
        self.gap = (self.contentsRect().height() - self.board_margin*2)/self.row_column
        for i in range(self.row_column):
            for j in range(self.row_column):
                if i == 0:
                    up = None
                else:
                    up = (i-1)*self.row_column + j
                if i == (self.row_column-1):
                    down = None
                else:
                    down = (i+1)*self.row_column + j
                if j == 0:
                    left = None
                else:
                    left = i*self.row_column + j -1
                if j == (self.row_column-1):
                    right = None
                else:
                    right = i*self.row_column + j +1
                pos = position(self.board_margin + 2 + j*self.gap, self.board_margin + 2 + i*self.gap, None, None,left,right,up,down)
                self.position_list.append(pos)
    
    def draw_board(self, painter):
        length = self.contentsRect().height()
        gap = (length - self.board_margin*2)/self.row_column
        pen = QtGui.QPen(QtGui.QColor(0xCCCC66).dark())
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.board_margin, self.board_margin, self.board_margin, self.board_margin+gap*self.row_column)
        painter.drawLine(self.board_margin, self.board_margin, self.board_margin+gap*self.row_column, self.board_margin)
        painter.drawLine(self.board_margin, self.board_margin+gap*self.row_column, self.board_margin+gap*self.row_column, self.board_margin+gap*self.row_column)
        painter.drawLine(self.board_margin+gap*self.row_column, self.board_margin, self.board_margin+gap*self.row_column, self.board_margin+gap*self.row_column)

        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(1,self.row_column):
            painter.drawLine(self.board_margin+i*gap, self.board_margin, self.board_margin+i*gap, self.board_margin+gap*self.row_column)
            painter.drawLine(self.board_margin, self.board_margin+i*gap, self.board_margin+gap*self.row_column, self.board_margin+i*gap)
            
    def draw_ball(self, x, y, color, painter): 
        painter.setPen(QtGui.QColor(color))
        Gradient = QtGui.QRadialGradient()
        Gradient.setCenter(x+27,y+27)
        Gradient.setColorAt(0,QtGui.QColor(0xFFFFFF))
        Gradient.setColorAt(0.6,QtGui.QColor(color))
        Gradient.setColorAt(1,QtGui.QColor(color).light())
        painter.setBrush(Gradient)
        painter.drawEllipse(x,y,36,36)

    def draw_chose_ball(self, x, y, color, painter):
        pen = QtGui.QPen(QtGui.QColor(color).light())
        pen.setWidth(3)
        pen.setStyle(3)
        painter.setPen(pen)
        Gradient = QtGui.QRadialGradient()
        Gradient.setCenter(x+28,y+28)
        Gradient.setColorAt(0,QtGui.QColor(0xFFFFFF))
        Gradient.setColorAt(0.6,QtGui.QColor(color))
        Gradient.setColorAt(0.1,QtGui.QColor(color).light())
        painter.setBrush(Gradient)
        painter.drawEllipse(x,y,36,36)
        
    def mousePressEvent(self, event):
        #print event.x(), event.y()
        x = event.x()
        y = event.y()
        if x < 15 or x > 375 or y > 375 or y <  15:
            self.chose_ball = None
        else:
            index = (x-self.board_margin)/self.gap+(y-self.board_margin)/self.gap*self.row_column
            if self.chose_ball == None:
                if index in self.have_ball_list:
                    self.chose_ball = index
                else:
                    pass
            else:
                if index in self.have_ball_list:
                    self.chose_ball = index
                else:
                    path = []
                    rtn = self.get_path(self.chose_ball, index, path)
                    #print rtn,path
                    if rtn:
                        chose_ball = self.chose_ball
                        path.pop(0)
                        for item in path :
                            self.position_list[item].color = self.position_list[chose_ball].color
                            self.position_list[item].have_ball = self.position_list[chose_ball].have_ball
                            self.position_list[chose_ball].clear_data() 
                            self.no_ball_list.append(chose_ball)
                            self.no_ball_list.remove(item)
                            self.have_ball_list.append(item)
                            self.have_ball_list.remove(chose_ball)
                            chose_ball = item
                            #self.update()
                        self.chose_ball=None
                        rtn_score = self.get_score()
                        if rtn_score:
                            for ipos in self.clear_up_list:
                                self.no_ball_list.append(ipos)
                                self.have_ball_list.remove(ipos)
                                self.position_list[ipos].clear_data()
                            self.clear_up_list = []
                        else:
                            self.random_next_setp()
                            rtn_score = self.get_score()
                            if rtn_score:
                                for ipos in self.clear_up_list:
                                    self.no_ball_list.append(ipos)
                                    self.have_ball_list.remove(ipos)
                                    self.position_list[ipos].clear_data()
                    else:
                        pass
        self.update()

    def draw_score(self, painter):
        pen = QtGui.QPen(QtGui.QColor(0x000080).light())
        pen.setWidth(3)
        painter.setPen(pen)
        text_score = QtCore.QString("Score:"+str(self.score))
        painter.drawText(400,30,text_score)
        #painter.drawText(400,30,60,60,QtCore.Qt.AlignLeft,text_score)
        
    def paintEvent(self, event): 
        painter = QtGui.QPainter(self)
        self.draw_board(painter)
        for index in self.have_ball_list:
            item = self.position_list[index]
            self.draw_ball(item.x, item.y, item.color, painter)

        if self.chose_ball:
            item = self.position_list[self.chose_ball]
            self.draw_chose_ball(item.x, item.y, item.color, painter)

        self.draw_score(painter)

    def get_path(self, source, target, path):
        for pos in self.position_list:
            pos.searched = 0
        self.count = 0
        
        return self.have_path(source, target, path)

    def have_path(self, source, target, path_list):
        self.position_list[source].searched = 1
        if source == target:
            path_list.insert(0,source)
            return True

        if self.position_list[source].left != None and self.position_list[self.position_list[source].left].searched == 0 and \
            self.position_list[self.position_list[source].left].have_ball == None:
                rtn = self.have_path(self.position_list[source].left, target, path_list)
                if rtn:
                    path_list.insert(0,source)
                    return True

        if self.position_list[source].right != None and self.position_list[self.position_list[source].right].searched == 0 and \
            self.position_list[self.position_list[source].right].have_ball == None:
                rtn = self.have_path(self.position_list[source].right, target, path_list)
                if rtn:
                    path_list.insert(0,source)
                    return True

        if self.position_list[source].up != None and self.position_list[self.position_list[source].up].searched == 0 and \
            self.position_list[self.position_list[source].up].have_ball == None:
                rtn = self.have_path(self.position_list[source].up, target, path_list)
                if rtn:
                    path_list.insert(0,source)
                    return True
                
        if self.position_list[source].down != None and self.position_list[self.position_list[source].down].searched == 0 and \
            self.position_list[self.position_list[source].down].have_ball == None:
                rtn = self.have_path(self.position_list[source].down, target, path_list)
                if rtn:
                    path_list.insert(0,source)
                    return True

        return False

    def get_row_score(self, position_list):
        pre_node = position_list[0]
        clear_up_list = [position_list[0]]
        for i in range(1, len(position_list)):
            if self.position_list[pre_node].have_ball == self.position_list[position_list[i]].have_ball and \
                self.position_list[position_list[i]].have_ball != None:
                pass
            else:
                if len(clear_up_list) >= 5:
                    self.clear_up_list += clear_up_list
                while clear_up_list:
                    clear_up_list.pop()
                    
            pre_node = position_list[i]
            clear_up_list.append(position_list[i])

        if len(clear_up_list) >= 5:
            self.clear_up_list += clear_up_list
        
    def get_score(self):
        self.clear_up_list = []
        for i in range(self.row_column):
            self.get_row_score([i*self.row_column+j  for j in range(self.row_column)])
            self.get_row_score([i+j*self.row_column  for j in range(self.row_column)])

        pos_list = [[4,12,20,28,36],
        [5,13,21,29,37,45],
        [6,14,22,30,38,46,54],
        [7,15,23,31,39,47,55,63],
        [8,16,24,32,40,48,56,64,72],
        [17,25,33,41,49,57,65,73],
        [26,34,42,50,58,66,74],
        [35,43,51,59,67,75],
        [44,52,60,68,76],
        [4,14,24,34,44],
        [3,13,23,33,43,53],
        [2,12,22,32,42,52,62],
        [1,11,21,31,41,51,61,71],
        [0,10,20,30,40,50,60,70,80],
        [9,19,29,39,49,59,69,79],
        [18,28,38,48,58,68,78],
        [27,37,47,57,67,77],
        [37,46,56,66,76]]
        for sub_list  in pos_list:
            self.get_row_score(sub_list)

        self.score += len(self.clear_up_list)
        self.clear_up_list = list(set(self.clear_up_list))
        if len(self.clear_up_list) > 0:
            return True
        else:
            return False

        
    def start(self):
        self.random_next_setp()
        self.update()

    def random_next_setp(self):
        if len(self.no_ball_list) < 3:
            print "Game over"
            return False
        else:
            for i in range(3):
                index = random.randint(0, len(self.no_ball_list)-1)
                value = self.no_ball_list.pop(index)
                self.have_ball_list.append(value)
                self.position_list[value].have_ball = random.randint(0, 6)
                self.position_list[value].color = self.color_list[self.position_list[value].have_ball]
            return True

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    cool_ball = CoolBall()
    cool_ball.show()
    cool_ball.start()
    sys.exit(app.exec_())



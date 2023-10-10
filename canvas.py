from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *

import jsonschema
from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.he.heview import HeView
from hetool.geometry.segments.line import Line
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation
from collector import CurveCollector


class Canvas(QtOpenGL.QGLWidget):
    
    def __init__(self):
        super(Canvas, self).__init__()
        self._hmodel = HeModel()
        self._controller = HeController(self._hmodel)
        self._view = HeView(self._hmodel)
        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.moved = False
        self.m_pt0 = QPointF(0.0, 0.0)
        self.m_pt1 = QPointF(0.0, 0.0)
        self.tools = []
        self.tool = None
        self.state = "None"
    
    def setState(self, _state):
        self.state = _state
        self.tool = self.tools[_state]

    def initializeGL(self): #glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)
            
    def resizeGL(self, _width, _height):
        # store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        
        if self._hmodel.isEmpty(): 
            self.scaleWorldWindow(1.0)
        else:
            self.m_L,self.m_R,self.m_B,self.m_T = self._view.getBoundBox()
            self.scaleWorldWindow(1.1)
        # setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        # reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # establish the clipping volume by setting up an
        # orthographic projection
        glOrtho(self.m_L,self.m_R,self.m_B,self.m_T,-1.0,1.0)
        # glOrtho(0.0, self.m_w, 0.0, self.m_h, -1.0, 1.0)

        # setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def paintGL(self):
        # clear the buffer with the current clear color
        glClear(GL_COLOR_BUFFER_BIT)
        
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_LINES)
        
        glVertex2f(pt0_U.x(), pt0_U.y())
        glVertex2f(pt1_U.x(), pt1_U.y())
        
        glEnd()
        if not(self._hmodel.isEmpty()):
            patches = self._hmodel.getPatches()
            for pat in patches:
                pts = pat.getPoints()
                triangs = Tesselation.tessellate(pts)
                glColor3f(1.0,0.0,1.0)
                for j in range(len(triangs)):
                    glBegin(GL_TRIANGLES)
                    glVertex2d(triangs[j][0].getX(), triangs[j][0].getY())
                    glVertex2d(triangs[j][1].getX(), triangs[j][1].getY())
                    glVertex2d(triangs[j][2].getX(), triangs[j][2].getY())
                    glEnd()
            segments = self._hmodel.getSegments()
            glColor3f(0.0, 0.0, 1.0) # blue
            for curves in segments:
                ptc = curves.getPointsToDraw()
                glBegin(GL_LINES)
                glVertex2f(ptc[0].getX(), ptc[0].getY())
                glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()
        
        glEndList()

    def fitWorldToViewport(self):
        if self._hmodel.isEmpty():
            return
        self.m_L,self.m_R,self.m_B,self.m_T = self._view.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()

    def scaleWorldWindow(self, _scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.m_h / self.m_w
        # Get current window center.
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        # Set new window sizes based on scaling factor.
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        # Adjust window to keep the same aspect ratio of the viewport.
        if sizey > (vpr*sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):
        # Compute pan distances in horizontal and vertical directions.
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        # Shift current window.
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        
    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QPointF(x,y)  

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            print(event.x())
            self.scaleWorldWindow(0.9)
        else:
            self.scaleWorldWindow(1.1)
        self.update()

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.pos()
        
    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.moved = True
            self.m_pt1 = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if not self.moved:
            self.m_pt0.setX(0)
            self.m_pt0.setY(0)
            return
            
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        # self._model.setCurve(pt0_U.x(),pt0_U.y(),pt1_U.x(), pt1_U.y())

        p0 = Point(pt0_U.x(), pt0_U.y())
        p1 = Point(pt1_U.x(), pt1_U.y())
        segment = Line(p0,p1)
        self._controller.insertSegment(segment,0.1)

        self.m_buttonPressed = False
        self.moved = False

        self.m_pt0.setX(0)
        self.m_pt0.setY(0)
        self.m_pt1.setX(0)
        self.m_pt1.setY(0)
        self.update()
        self.repaint()
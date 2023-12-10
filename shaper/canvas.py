from PyQt5 import QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *

from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.he.heview import HeView
from hetool.geometry.segments.line import Line
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation
from .elements.mesh_point import MeshPoint
from .collector import CurveCollector


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
        self.state = "None"
        self.curve_collector = CurveCollector()
        self.m_heTol = 20.0
        self.shift = False
        self.mesh = []
    
    def setState(self, _state):
        self.state = _state
        if _state == "curve":
            self.curve_collector.activateCollector("Bezier2")
            self.state = "line"
        else:
            self.curve_collector.deactivateCollector()

    def setAttrs(self, temp, is_fixed, force_value, force_direction):
        for point in self.getMeshSelected():
            point.setAttrs(temp,is_fixed,force_value,force_direction)

    def setMesh(self, distance):
        if distance == 0:
            return
        left, right, bottom, top = self._view.getBoundBox()
        self.mesh = []
        surfaces = self._hmodel.getPatches()
        aux_y = bottom
        while aux_y < top + self.m_heTol:
            aux_x = left
            while aux_x < right + self.m_heTol:
                pt = MeshPoint(aux_x, aux_y)
                for surface in surfaces:
                    if surface.isPointInside(pt):
                        self.mesh.append(pt)
                aux_x += distance
            aux_y += distance
        self.repaint()
        self.update()

    def getMeshSelected(self):
        selected = []
        for pt in self.mesh:
            if pt.isSelected():
                selected.append(pt)
        return selected

    def getEventUCoordinates(self, event):
        m_pt = event.pos()
        pt_u = self.convertPtCoordsToUniverse(m_pt)
        return pt_u.x(), pt_u.y()
    
    def initializeGL(self): #glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND);
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
        if not(self._hmodel.isEmpty()):
            patches = self._hmodel.getPatches()
            for pat in patches:
                pts = pat.getPoints()
                triangs = Tesselation.tessellate(pts)
                glColor3f(0.4,0.3,5.0)
                for j in range(len(triangs)):
                    glBegin(GL_TRIANGLES)
                    glVertex2d(triangs[j][0].getX(), triangs[j][0].getY())
                    glVertex2d(triangs[j][1].getX(), triangs[j][1].getY())
                    glVertex2d(triangs[j][2].getX(), triangs[j][2].getY())
                    glEnd()
            segments = self._hmodel.getSegments()
            for line in segments:
                if line.isSelected():
                    glColor3f(1.0, 0.0, 0.0)
                else:
                    glColor3f(0.0, 0.0, 1.0)
                ptc = line.getPointsToDraw()
                glLineWidth(3)
                glBegin(GL_LINES)
                glVertex2f(ptc[0].getX(), ptc[0].getY())
                glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()

            points = self._hmodel.getPoints()
            for point in points:
                if point.isSelected():
                    glColor3f(1.0, 0.0, 0.0)
                else:
                    glColor3f(1.0, 1.0, 1.0)
                glPointSize(5)
                glBegin(GL_POINTS)
                glVertex2f(point.getX(), point.getY())
                glEnd()

        pt0_U = self.m_pt0
        pt1_U = self.m_pt1
        if self.state == "line":   
            glColor3f(1.0, 1.0, 0.0)
            glBegin(GL_LINES)
            glVertex2f(pt0_U.x(), pt0_U.y())
            glVertex2f(pt1_U.x(), pt1_U.y())
            glEnd()
        elif self.state == "select" or self.state == "square":
            left = min(pt0_U.x(), pt1_U.x())
            right = max(pt0_U.x(), pt1_U.x())
            up = max(pt0_U.y(), pt1_U.y())
            down = min(pt0_U.y(), pt1_U.y())
            if self.state == "select":
                glColor4f(0.1, 0.0, 0.9, 0.5)
            else:
                glColor3f(0.0,1.0,0.0)
            glBegin(GL_QUADS)
            glVertex2f(left, up)
            glVertex2f(left, down)
            glVertex2f(right, down)
            glVertex2f(right, up)
            glEnd()

        temp_curve = self.curve_collector.getCurveToDraw()
        glColor3f(0.0,1.0,0.0)
        glBegin(GL_LINE_STRIP)
        for pt in temp_curve:
            glVertex2f(pt[0], pt[1])
        glEnd()

        glBegin(GL_POINTS)
        for pt in self.mesh:
            r,g,b = pt.color
            glColor3f(r,g,b)
            glVertex2f(pt.getX(), pt.getY())
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
            self.scaleWorldWindow(0.9)
        else:
            self.scaleWorldWindow(1.1)
        self.update()

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        x, y = self.getEventUCoordinates(event)
        if self.state == "line" or self.state == "select" or self.state == "square":
            self.m_pt0.setX(x)
            self.m_pt0.setY(y)
        elif self.state == "curve":
            self.curve_collector.update(x, y)   

    def mouseMoveEvent(self, event):
        if not self.m_buttonPressed:
            return
        self.moved = True
        x, y = self.getEventUCoordinates(event)
        if self.state == "line" or self.state == "select" or self.state == "square":
            self.m_pt1.setX(x)
            self.m_pt1.setY(y)
        elif self.state == "curve":
            self.curve_collector.update(x, y)
        self.update()

    def mouseReleaseEvent(self, event):
        if self.state == "line":
            if not self.moved:
                self.m_pt0.setX(0)
                self.m_pt0.setY(0)
                return

            p0 = Point(self.m_pt0.x(), self.m_pt0.y())
            p1 = Point(self.m_pt1.x(), self.m_pt1.y())
            segment = Line(p0,p1)
            if self.curve_collector.isActive():
                self.state = "curve"
                self.curve_collector.collectPoint(p0.x, p0.y)
                self.curve_collector.collectPoint(p1.x, p1.y)
            else:
                self._controller.insertSegment(segment,self.m_heTol)
        elif self.state == "curve":
            x,y = self.getEventUCoordinates(event)
            finish = self.curve_collector.collectPoint(x, y)
            if finish:
                curve = self.curve_collector.getCurve()
                init_pt = curve.pop(0)
                for pt in curve:
                    pt0 = init_pt
                    pt1 = pt
                    try:
                        self._controller.insertSegment(pt0+pt1, self.m_heTol)
                    except:
                        print("Falha ao inserir segmento")
                    init_pt = pt
                self.state = "line"
        elif self.state == "select":
            x,y = self.getEventUCoordinates(event)
            if not self.moved:
                for point in self.mesh:
                    point.setSelected(False)
            else:
                for point in self.mesh:
                    point.setSelected(point.isInside(self.m_pt0.x(), self.m_pt0.y(), self.m_pt1.x(), self.m_pt1.y()))
                self.update()
        elif self.state == "square":
            if not self.moved:
                self.m_pt0.setX(0)
                self.m_pt0.setY(0)
                return
            
            p00 = Point(self.m_pt0.x(), self.m_pt0.y())
            p10 = Point(self.m_pt1.x(), self.m_pt0.y())
            p11 = Point(self.m_pt1.x(), self.m_pt1.y())
            p01 = Point(self.m_pt0.x(), self.m_pt1.y())

            l1 = Line(p00,p10)
            l2 = Line(p10,p11)
            l3 = Line(p11,p01)
            l4 = Line(p01,p00)
            lines = [l1,l2,l3,l4]

            for line in lines:
                try:
                    self._controller.insertSegment(line, self.m_heTol)
                except:
                    print("Falha ao inserir segmento")
            
        self.m_pt0.setX(0)
        self.m_pt0.setY(0)
        self.m_pt1.setX(0)
        self.m_pt1.setY(0)
        self.m_buttonPressed = False
        self.moved = False
        self.repaint()
        self.update()
        

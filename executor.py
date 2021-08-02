#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtCore import Qt

from colors import colornames, isvalidcolor
import compiler


class Turtle(QWidget):
    def __init__(self, parent=None, sizes=None, bg=None, points=[]):
        super().__init__(parent)
        if sizes:
            self.resize(*sizes)
        self.bg = bg
        self.points = points

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.redraw(painter, e)
        painter.end()

    def redraw(self, painter, event):
        visible = False
        color = "#000000"
        cap = Qt.SquareCap
        width = 4
        x = 0
        y = 0
        painter.setBrush(Qt.NoBrush)
        buffer = ""
        if self.bg and isvalidcolor(self.bg):
            self.bg = self.bg.lower()
            self.setStyleSheet(f"background: {self.bg};")
        else:
            self.setStyleSheet(f"background: white;")
        for p in self.points:
            qc = QColor(color)
            pen = QPen(qc, width, Qt.SolidLine)
            pen.setCapStyle(cap)
            painter.setPen(pen)
            if p == "VISIBLE":
                visible = True
            elif p == "HIDDEN":
                visible = False
            elif p.split()[0] == "SETBG":
                newcolor = p.split()[1]
                if isvalidcolor(newcolor):
                    self.bg = newcolor
                    self.setStyleSheet(f"background: {self.bg};")
            elif p.split()[0] == "SETCOLOR":
                newcolor = p.split()[1]
                if isvalidcolor(newcolor):
                    color = newcolor
            elif p.split()[0] == "SETCAP":
                newcap = p.split()[1]
                cap = eval("Qt." + newcap + "Cap")
            elif p.split()[0] == "SETWIDTH":
                width = int(p.split()[1])
            elif p == "CLEAR":
                self.clear()
            elif p.split()[0] == "PYCODE":
                if p.strip() == "PYCODE END":
                    exec(buffer, globals())
                    buffer = ""
                else:
                    buffer += p.split(" ", 1)[1]
            elif p.split()[0] == "CIRCLE":
                coords = p.split(" ", 1)[1].replace(" ", ", ")
                painter.drawEllipse(*eval(coords))
            elif p.split()[0] == "TITLE":
                title = p.split(" ", 1)[1]
                self.setWindowTitle(title)
            else:
                path = QPainterPath()
                if (x != 0 or y != 0):
                    path.moveTo(x, y)
                xy = p.split("x")
                x = int(xy[0])
                y = int(xy[1])
                if visible:
                    draw = path.lineTo
                else:
                    draw = path.moveTo
                draw(x, y)
                painter.drawPath(path)
        qc = QColor(color)
        painter.setPen(pen)
        if visible:
            painter.setBrush(qc)
            painter.drawEllipse(x - 5, y - 5, 10, 10)

    def command(self, c):
        self.points.append(c)
        self.update()

    def clear(self):
        self.points = []
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    turtle = Turtle(sizes=(800, 600))
    for i in range(10):
        cmd = input(str(i) + ": ")
        turtle.command(cmd)
    turtle.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QGraphicsDropShadowEffect, QGraphicsEffect
from PyQt5.QtCore import QSize, QEvent, QPropertyAnimation, QAbstractAnimation, QEasingCurve, QVariantAnimation
from PyQt5.QtGui import QIcon

#-----------------------------------------------#
#Implement a mainButton class instance of       #
#QPushButton to easily tweak each property      #
#and to easily implement event filters          #
#for main and sidebar buttons                   #
#-----------------------------------------------#

class MainButton(QPushButton):
    def __init__(self, iconpath, xSize, ySize):
        super().__init__()

        #Text settings
        self.setText(None)

        #Size settings
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(xSize, ySize)
        self.setMaximumSize(xSize + 10, ySize + 10)

        #Icon settings
        self.setIcon(QIcon(iconpath))
        self.setIconSize(QSize(xSize + 10,ySize + 10))

        #Shadow settings
        self.shadow = QGraphicsDropShadowEffect(blurRadius = 8, xOffset = 0, yOffset= 0)
        self.setGraphicsEffect(self.shadow)

        #Filter settings
        self.installEventFilter(self)

        #Animation Settings
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setStartValue(QSize(xSize, ySize))
        self.anim.setEndValue(QSize(xSize + 10, ySize + 10))
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)

    def eventFilter(self, QObject, event):
        if event.type() == QEvent.Leave:
            self.anim.setDirection(QAbstractAnimation.Forward)
            self.anim.start()
            return True
        elif event.type() == QEvent.Enter:
            self.anim.setDirection(QAbstractAnimation.Backward)
            self.anim.start()
        return False

class SideButton(QPushButton):
    def __init__(self, iconpath, hovericon, xSize, ySize):
        super().__init__(iconpath)

        #Text settings
        self.setText(None)

        #Size settings
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(xSize, ySize)
        self.setMaximumSize(xSize + 10, ySize + 10)

        #Icon settings
        self.icon = QIcon(iconpath)
        self.hovericon = QIcon(hovericon)
        self.setIcon(self.icon)
        self.setIconSize(QSize(xSize + 10,ySize + 10))

        #Filter settings
        self.installEventFilter(self)

    def eventFilter(self, QObject, event):
        if event.type() == QEvent.Enter:
            self.setIcon(self.hovericon)
            return True
        elif event.type() == QEvent.Leave:
            self.setIcon(self.icon)
        return False
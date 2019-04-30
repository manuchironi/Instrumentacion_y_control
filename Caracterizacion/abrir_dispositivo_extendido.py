# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abrir_dispositivo_extendido.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 294)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 211, 16))
        self.label.setObjectName("label")
        self.TreeWidget = QtWidgets.QTreeWidget(Dialog)
        self.TreeWidget.setGeometry(QtCore.QRect(40, 50, 311, 181))
        self.TreeWidget.setObjectName("TreeWidget")
        font = QtGui.QFont()
        font.setUnderline(False)        
        self.TreeWidget.headerItem().setFont(0, font)
        self.TreeWidget.headerItem().setBackground(0, QtGui.QColor(206, 206, 206)) 
      
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Seleccione un dispositivo de la siguiente lista"))
        self.TreeWidget.headerItem().setText(0, _translate("Dialog", "Dispositivos disponibles")) 
        __sortingEnabled = self.TreeWidget.isSortingEnabled()
        self.TreeWidget.setSortingEnabled(False)
   #     self.TreeWidget.topLevelItem(0).setText(0, _translate("Dialog", "Primera fila"))
        self.TreeWidget.setSortingEnabled(__sortingEnabled)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


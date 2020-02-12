import os
import sys
import re

import CGAgnostics.GUI as comp
from PySide2 import QtWidgets, QtCore, QtGui

# Color definitions:
_WINDOW_STYLE = '''
    font: 10pt; background-color: rgb(40,40,45); color:white;
    '''

_DARK_TAB_STYLE = '''
                QTabBar::tab{
                background-color:rgb(60,70,100);
                font: bold;
                width:100px;
                color:white;
                }

                QTabBar::tab:selected, QTabBar::tab:hover {
                background: rgb(200,150,30);
                color:rgb(35,35,60)
                }

                QTabWidget::pane {border-top: 2px solid #C2C7CB;}
                QTabWidget::tab-bar {left: 20px;}
            '''

_BLUE_BTN_STYLE = '''
    QToolTip {color: white; border: 2px solid darkkhaki;
    padding: 5px; border - radius: 3 px; opacity: 200;}
    QPushButton:enabled {background-color: rgb(60,70,100)}
    QPushButton:disabled {background-color: rgb(40,40,45)}
    
    '''

_DARK_LNE_STYLE = '''
    QLineEdit:enabled{
        background:rgb(15,15,15);
        border: none;
        selection-background-color:rgb(250,100,30);
    }
    
    QLineEdit:disabled{
        background:rgb(40,40,45);
        border: none;
    }

    '''
_DARK_TBL_STYLE = '''
    QTableWidget {
    background-color: rgb(25,25,25);
    selection-background-color:rgb(45,45,60)}

    QHeaderView{
        color:rgb(150,100,50);
        background-color:rgb(20,20,20)}
    '''
_DARK_TED_STYLE = '''
    QTextEdit {
    font: italic;
    color: rgb(100,100,100);
    background-color: rgb(20,20,20);
    selection-background-color:rgb(30,30,50)}
    '''
_DARK_CBX_STYLE = '''
    background:rgb(20,20,20);
    selection-background-color:rgb(250,100,30);
    '''

_DARK_SBX_STYLE = '''
    color: white;
    background:rgb(20,20,20);
    selection-background-color:rgb(250,100,30);
    '''

_DARK_LBL_STYLE = '''
    QLabel:enabled{
        color: rgb(200,200,200);
    }
    QLabel:disabled{
        color:rgb(150,150,150);
    }
'''

# End color definitions.

class ToolkitQWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    @staticmethod
    def root_path():
        pattern = re.compile('CGAgnostics.*')
        if getattr(sys, 'frozen', False):
            result = os.path.dirname(sys.executable)
            result = re.sub(pattern, "", result)
        else:
            result = os.path.dirname(__file__)
            result = re.sub(pattern, "", result)
        return result


class ToolkitQDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ToolkitQDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(_WINDOW_STYLE)

    @staticmethod
    def execution_path():
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.dirname(__file__)
        return datadir


class ToolkitQTab(QtWidgets.QTabWidget):
    def __init__(self):
        super(ToolkitQTab, self).__init__()

        self.setStyleSheet(_DARK_TAB_STYLE)


class ToolkitQPushButton(QtWidgets.QPushButton):
    def __init__(self, label, tooltip='No tooltip set yet'):
        super(ToolkitQPushButton, self).__init__(label)
        self.setToolTip(tooltip)
        self.setStyleSheet(_BLUE_BTN_STYLE)


class ToolkitQLineEdit(QtWidgets.QLineEdit):
    def __init__(self, placeholder=''):
        super(ToolkitQLineEdit, self).__init__()
        self.setStyleSheet(_DARK_LNE_STYLE)
        self.setPlaceholderText(placeholder)

    s_key_pressed = QtCore.Signal()
    enter_key_pressed = QtCore.Signal()

    def keyPressEvent(self, e):
        super(ToolkitQLineEdit, self).keyPressEvent(e)
        if e.key() == QtCore.Qt.Key_S:
            self.s_key_pressed.emit()
        elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_key_pressed.emit()


class ToolkitQTableWidget(QtWidgets.QTableWidget):
    enter_pressed = QtCore.Signal()

    def __init__(self):
        super(ToolkitQTableWidget, self).__init__()
        self.setStyleSheet(_DARK_TBL_STYLE)

    def keyPressEvent(self, e):
        super(ToolkitQTableWidget, self).keyPressEvent(e)
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit()


class ToolkitQConsole():
    def __init__(self):
        self._colors = {
            "standar": QtGui.QColor(120, 120, 120),
            "success": QtGui.QColor(50, 150, 100),
            "warning": QtGui.QColor(170, 150, 40),
            "error": QtGui.QColor(180, 60, 60)
        }
        self._V_root_LYT = None
        self._set_console()

    @property
    def widget(self):
        _WGT = QtWidgets.QWidget()
        _WGT.setLayout(self._V_root_LYT)
        return _WGT

    @property
    def layout(self):
        return self._V_root_LYT
        # -------------------------------------------------------------
        # Public methods:

    def log(self, message, color="standar"):
        if color == "success":
            self.console_TED.setText('')
            self.console_TED.setTextColor(self._colors["success"])
            self.console_TED.setText('<Success> ' + message)
        elif color == "warning":
            self.console_TED.setText('')
            self.console_TED.setTextColor(self._colors["warning"])
            self.console_TED.setText('<Warning> ' + message)
        elif color == "error":
            self.console_TED.setText('')
            self.console_TED.setTextColor(self._colors["error"])
            self.console_TED.setText('<Error> ' + message)
        else:
            self.console_TED.setText('')
            self.console_TED.setTextColor(self._colors["standar"])
            self.console_TED.setText(message)

    # -------------------------------------------------------------
    # Private methods:

    def _set_console(self):
        self.H_root_console_LYT = None

        def _widgets():
            self.console_TED = QtWidgets.QTextEdit()
            self.console_TED.setPlainText("Logs...")
            self.console_TED.setStyleSheet(_DARK_TED_STYLE)
            self.console_TED.setMinimumHeight(40)
            self.console_TED.setMaximumHeight(800)
            self.console_TED.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
            self.console_TED.setReadOnly(True)

            self.clear_BTN = QtWidgets.QPushButton("Clear console")

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()
            _V_LYT.addWidget(self.console_TED)

            _H_clear_button_LYT = QtWidgets.QHBoxLayout()
            _H_clear_button_LYT.addStretch()
            _H_clear_button_LYT.addWidget(self.clear_BTN)

            _V_LYT.addLayout(_H_clear_button_LYT)

            self._V_root_LYT = _V_LYT

        def _methods():
            def clear_console():
                self.console_TED.setText('')
                self.console_TED.setTextColor(self._colors["standar"])

            self.clear_BTN.clicked.connect(clear_console)

        _widgets()
        _layouts()
        _methods()


class ToolkitQGroupBox(QtWidgets.QGroupBox):
    def __init__(self, label):
        super(ToolkitQGroupBox, self).__init__(label)
        self.setStyleSheet(
            'QGroupBox {border: 1px solid rgb(20,20,20); padding:10%}')


class ToolkitQComboBox(QtWidgets.QComboBox):
    def __init__(self, list_of_items=None):
        super(ToolkitQComboBox, self).__init__()
        self.setStyleSheet(_DARK_CBX_STYLE)

        if list_of_items is not None:
            for each in list_of_items:
                self.addItem(each)


class ToolkitQCredits(QtWidgets.QLabel):
    def __init__(self):
        super(ToolkitQCredits, self).__init__()
        self.setText("Created by Jair Anguiano," +
                     "for support mail me at " +
                     '<a style="color:rgb(95,95,95);"href="jairanpo@gmail.com">' +
                     'jairanpo@gmail.com</a>')

        self.setStyleSheet("color:rgb(90,90,90); font: Italic")


class ToolkitQCloseButton(QtWidgets.QPushButton):
    def __init__(self, text="close"):
        super(ToolkitQCloseButton, self).__init__()
        self.setText(text)
        self.setMinimumWidth(80)
        self.setMaximumWidth(150)


class ToolkitQFooter():
    def __init__(self, parent=""):
        self.parent = parent
        self.set_footer()

    @property
    def layout(self):
        _V_LYT = QtWidgets.QVBoxLayout()
        _WGT = QtWidgets.QWidget()
        _WGT.setLayout(self._V_root_layout)
        _V_LYT.addWidget(_WGT)
        return _V_LYT

    @property
    def widget(self):
        _WGT = QtWidgets.QWidget()
        _WGT.setLayout(self.layout)
        return _WGT

    @classmethod
    def close(cls, self):
        self.close_BTN.clicked.connect(self.parent.close)

    def set_footer(self):
        def _widgets():
            self.credits_LBL = ToolkitQCredits()
            self.close_BTN = ToolkitQCloseButton()

        def _layouts():
            _V_LYT = QtWidgets.QVBoxLayout()
            _H_LYT = QtWidgets.QHBoxLayout()
            _H_LYT.addWidget(self.credits_LBL)
            _H_LYT.addWidget(self.close_BTN)
            _V_LYT.addLayout(_H_LYT)
            self._V_root_layout = _V_LYT

        def _methods():
            self.close_BTN.clicked.connect(self.parent.close)

        _widgets()
        _layouts()
        _methods()


class ToolkitQSpinBox(QtWidgets.QSpinBox):
    def __init__(self, prefix):
        super().__init__()
        self.setPrefix(prefix)
        self.setStyleSheet(_DARK_SBX_STYLE)


class ToolkitQIconButton(QtWidgets.QPushButton):
    def __init__(self, icon, label=''):
        super().__init__(label)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(50, 50))
        self.setStyleSheet(_BLUE_BTN_STYLE)


class ToolkitQBrowseButton(QtWidgets.QPushButton, ToolkitQWidget):
    def __init__(self, parent, lineedit='', is_file=False, size=[50, 50], filter="*"):
        super().__init__()
        self._is_file = is_file
        self.path_LNE = lineedit
        self.parent = parent
        self.filter = filter
        self.setIconSize(QtCore.QSize(size[0], size[1]))
        self.setStyleSheet(_BLUE_BTN_STYLE)
        self._icons_path = os.path.join(
            self.root_path(), "CGAgnostics", "icons")
        self._folder_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "folder.ico"))

        self.setIcon(self._folder_icon)

        self._methods()

    def _methods(self):
        def set_savepath():
            file_path_FLD = QtWidgets.QFileDialog()
            path = False

            if self._is_file:
                path = file_path_FLD.getOpenFileName(
                    self.parent, "Select source file",
                    filter=self.filter
                )
                self.path_LNE.setText(path[0])

            else:
                path = file_path_FLD.getExistingDirectory(
                    self.parent, "Select folder")
                self.path_LNE.setText(path)

        self.clicked.connect(set_savepath)


class ToolkitQCreateButton(QtWidgets.QPushButton, ToolkitQWidget):
    def __init__(self, size=[120, 70]):
        super().__init__()
        self.setIconSize(QtCore.QSize(size[0], size[1]))
        self.setStyleSheet(_BLUE_BTN_STYLE)
        self._icons_path = os.path.join(
            self.root_path(), "CGAgnostics", "icons")
        self._create_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "export.ico"))

        self.setIcon(self._create_icon)


class ToolkitQLabel(QtWidgets.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(_DARK_LBL_STYLE)


class ToolkitQSplitter(QtWidgets.QSplitter):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
                QSplitter::handle {
                    image: url(images/splitter.png);
                    border: 1px dashed rgb(150,150,150);
            }
        ''')


class ToolkitQDirectory(ToolkitQWidget):
    def __init__(self, parent="", is_file=False):
        self.parent = parent
        self._is_file = is_file
        self._main_path = self.root_path()
        self._icons_path = os.path.join(self._main_path, 'icons')
        self._search_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "folder.ico"))
        self._create_icon = QtGui.QIcon(
            os.path.join(self._icons_path, "create.ico"))
        self.V_root_LYT = None
        self.V_savepath_LYT = None

        ToolkitQDirectory._widgets(self)
        ToolkitQDirectory._layouts(self)
        ToolkitQDirectory._methods(self)

    def _widgets(self):
        b_size = 40, 30
        self._instructions = comp.ToolkitQLabel('')

        self.savepath_LBL = comp.ToolkitQLabel('<h3>Path:</h3>')
        self.savepath_LNE = comp.ToolkitQLineEdit()
        self.savepath_BTN = comp.ToolkitQPushButton('')
        self.savepath_BTN.setIcon(self._search_icon)
        self.savepath_BTN.setIconSize(
            QtCore.QSize(b_size[0], b_size[1]))

        self.create_BTN = comp.ToolkitQIconButton(self._create_icon)
        self.create_BTN.setIconSize(QtCore.QSize(200, 120))
        self.create_BTN.setMaximumWidth(270)
        self.create_BTN.setMinimumWidth(200)
        self.create_BTN.setMinimumHeight(55)
        self.create_BTN.setMaximumHeight(55)

    def _layouts(self):
        _V_LYT = QtWidgets.QVBoxLayout()
        _H_savepath_LYT = QtWidgets.QHBoxLayout()
        _H_savepath_LYT.addWidget(self.savepath_LBL)
        _H_savepath_LYT.addWidget(self.savepath_LNE)
        _H_savepath_LYT.addWidget(self.savepath_BTN)
        _V_LYT.addLayout(_H_savepath_LYT)

        self.V_savepath_LYT = _V_LYT

    def _methods(self):
        def set_savepath():
            file_path_FLD = QtWidgets.QFileDialog()
            path = False

            if self._is_file:
                path = file_path_FLD.getOpenFileName(
                    self.parent, "Select source file",
                    filter="Videos (*.mp4 *.avi *.mov *.webmd)"
                )
                self.savepath_LNE.setText(path[0])

            else:
                path = file_path_FLD.getExistingDirectory(
                    self.parent, "Select folder")
                self.savepath_LNE.setText(path)

        self.savepath_BTN.clicked.connect(set_savepath)

    @property
    def savepath(self):
        return self.savepath_LNE.text().strip()

    @property
    def savepath_layout(self):
        return self.V_savepath_LYT

    @property
    def layout(self):
        return self.V_root_LYT

    @layout.setter
    def layout(self, value):
        self.V_root_LYT = value

    @property
    def console(self):
        return self._console

    @console.setter
    def console(self, ToolkitQConsole):
        self._console = ToolkitQConsole

    @property
    def create_button(self):
        return self.create_BTN

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, text):
        self._instructions.setText(text)


class ToolkitQCheckBox(QtWidgets.QCheckBox, ToolkitQWidget):
    def __init__(self, label):
        super().__init__(label)

        stylesheet = '''
            QCheckBox::indicator:unckeched { 
                width: 8px;
                height: 8px;
                border-radius:7px;
                border: 3px solid rgb(30,30,30);
               
            }

            QCheckBox:unchecked{
                    color:rgb(150,150,150)
            }

            QCheckBox::indicator:checked { 
                width: 8px;
                height: 8px;
                border-radius:7px;
                border: 3px solid rgb(30,30,30);
                background: rgb(200,90,30);
            }

            QCheckBox:checked{
                color:rgb(255,255,255)
            }
        '''

        self.setStyleSheet(stylesheet)

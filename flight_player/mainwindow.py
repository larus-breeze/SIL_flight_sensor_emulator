import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))   # Add parent folder to make imports of parallel directory possible
from larus_data.larus_to_df import raw_data_formats, processed_data_formats
from player import Player

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        """Main window of the Larus Flight Player"""
        super().__init__(parent=None)
        self.setWindowTitle('Larus Flight Player')
        QtCore.QCoreApplication.setOrganizationName("larus")
        QtCore.QCoreApplication.setOrganizationDomain("https://github.com/larus-breeze")
        QtCore.QCoreApplication.setApplicationName("flight_player")

        dir = os.path.dirname(__file__)

        self._player = Player(self, dir)
        self.setCentralWidget(self._player)

        self.setWindowIcon(QtGui.QIcon(dir + '/icons/larus_breeze.png'))
        
        # QActions
        self._openAction = QtWidgets.QAction(QtGui.QIcon(dir + '/icons/file_open.png'), 'Open', self)
        self._openAction.triggered.connect(self._open_file)
        self._openAction.setStatusTip("Open Larus Logfile")
        self._playAction = QtWidgets.QAction(QtGui.QIcon(dir + '/icons/play.png'), 'Play', self)
        self._playAction.triggered.connect(self._player.start_flight_player)
        self._playAction.setStatusTip("Play Larus Logfile")
        self._pauseAction = QtWidgets.QAction(QtGui.QIcon(dir + '/icons/pause.png'), 'Pause', self)
        self._pauseAction.triggered.connect(self._player.stop_flight_player)
        self._pauseAction.setStatusTip("Pause playing Logfile")
        self._exitAction = QtWidgets.QAction(QtGui.QIcon(dir + '/icons/exit.png'), 'Exit', self)
        self._exitAction.triggered.connect(self.close)
        self._exitAction.setStatusTip("Exit Larus Flight Player")

        # QMenu
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction(self._openAction)
        menu.addAction(self._playAction)
        menu.addAction(self._pauseAction)
        menu.addAction(self._exitAction)

        # QToolbar
        tools = QtWidgets.QToolBar()
        tools.addAction(self._openAction)
        tools.addAction(self._playAction)
        tools.addAction(self._pauseAction)
        tools.addAction(self._exitAction)
        self.addToolBar(tools)

        # QStatusbar
        status = QtWidgets.QStatusBar()
        self.setStatusBar(status)

        self.resize(800, 600)

    def _open_file(self):
        """Opens the selected Larus Data File"""

        larus_file_filter = "Larus files ("
        for element in raw_data_formats.keys():
            larus_file_filter += "*{} ".format(element)
        for element in processed_data_formats.keys():
            larus_file_filter += "*{} ".format(element)
        larus_file_filter += ")"

        settings = QtCore.QSettings()
        file_name, x = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", larus_file_filter)
        if file_name != "":
            settings.setValue("fileName", file_name)
            self._player.open_file()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

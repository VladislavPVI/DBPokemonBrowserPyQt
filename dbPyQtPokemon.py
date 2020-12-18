from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QTableWidget, QPushButton, QComboBox, \
    QTableWidgetItem
import sqlite3
from sqlite3 import Error
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.combo = QComboBox(self)
        self.tab5 = QTableWidget(self)
        self.tab4 = QTableWidget(self)
        self.tab3 = QTableWidget(self)
        self.tab2 = QTableWidget(self)
        self.tab1 = QTableWidget(self)
        self.tabs = QTabWidget(self)
        self.initUI()

    def setConnect(self):
        try:
            self.con = sqlite3.connect('veekun-pokedex.sqlite')
            print('connection established')

            self.cursorObj = self.con.cursor()
            self.cursorObj.execute('SELECT * FROM pokemon')

            col = list(map(lambda x: x[0], self.cursorObj.description))
            self.combo.addItems(col)

            self.set_data_to_table(self.tab1)
            self.tabs.setCurrentIndex(0)

        except Error:
            print(Error)

    def set_data_to_table(self, table):
        rows = self.cursorObj.fetchall()
        col = list(map(lambda x: x[0], self.cursorObj.description))

        table.setColumnCount(len(col))
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(col)

        for row_num, row in enumerate(rows):
            for col_num, col in enumerate(row):
                table.setItem(row_num, col_num, QTableWidgetItem(str(col)))

    def cleanTab(self, table):

        while table.rowCount() > 0:
            table.removeRow(0)
        table.setColumnCount(0)

    def closeConnect(self):
        try:
            self.con.close()

            self.cleanTab(self.tab1)
            self.cleanTab(self.tab2)
            self.cleanTab(self.tab3)
            self.cleanTab(self.tab4)
            self.cleanTab(self.tab5)

            print('connection closed')

        except Error:
            print(Error)

    def buttonClicked1(self):

        try:
            self.cursorObj.execute('SELECT identifier FROM pokemon')
            self.set_data_to_table(self.tab2)
            self.tabs.setCurrentIndex(1)

        except Error:
            print('check connection')

        except AttributeError:
            self.setConnect()

    def buttonClicked2(self):

        try:
            self.cursorObj.execute('SELECT * FROM pokemon where height > 50')
            self.set_data_to_table(self.tab3)
            self.tabs.setCurrentIndex(2)

        except Error:
            print('check connection')

        except AttributeError:
            self.setConnect()

    def buttonClicked3(self):
        try:
            self.cursorObj.execute('SELECT identifier, height, weight FROM pokemon ORDER BY weight')
            self.set_data_to_table(self.tab4)
            self.tabs.setCurrentIndex(3)

        except Error:
            print('check connection')

        except AttributeError:
            self.setConnect()

    def onActivated(self, text):

        try:
            self.cursorObj.execute('SELECT `' + text + '` FROM pokemon')
            self.set_data_to_table(self.tab5)
            self.tabs.setCurrentIndex(4)

        except Error:
            print('check connection')
        except AttributeError:
            self.setConnect()

    def initUI(self):
        self.setWindowTitle('DB Pokemon Browser')

        self.setFixedSize(600, 600)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Menu')

        newConnection = QAction('Set connection', self)
        closeConnection = QAction('Close connection', self)

        newConnection.triggered.connect(self.setConnect)
        closeConnection.triggered.connect(self.closeConnect)

        fileMenu.addAction(newConnection)
        fileMenu.addAction(closeConnection)

        btn1 = QPushButton("SELECT Column", self)
        btn1.setFixedSize(120, 50)
        btn1.move(24, 37)
        btn1.clicked.connect(self.buttonClicked1)

        btn2 = QPushButton("Query 2", self)
        btn2.setFixedSize(120, 50)
        btn2.move(168, 37)
        btn2.clicked.connect(self.buttonClicked2)

        btn3 = QPushButton("Query 3", self)
        btn3.setFixedSize(120, 50)
        btn3.move(312, 37)
        btn3.clicked.connect(self.buttonClicked3)

        self.combo.setFixedSize(120, 50)
        self.combo.move(456, 37)
        self.combo.activated[str].connect(self.onActivated)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")
        self.tabs.addTab(self.tab4, "Tab 4")
        self.tabs.addTab(self.tab5, "Tab 5")

        self.tabs.setFixedSize(600, 500)
        self.tabs.move(0, 100)
        self.setFixedSize(600, 600)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = MainWindow()
    sys.exit(app.exec_())
from PySide6.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem,
                               QHeaderView, QPushButton, QHBoxLayout,
                               QVBoxLayout, QAbstractItemView,
                               QLineEdit, QApplication)
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import QPointF, Qt

import numpy as np



# incremental row + keypress event

class MyTable(QTableWidget):
    def __init__(self, horizonatlHearderLabels, parent=None):
        super().__init__(parent)

        self.setColumnCount(len(horizonatlHearderLabels))
        self.setRowCount(1)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setHorizontalHeaderLabels(horizonatlHearderLabels)

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.setItem(i, j, item)

        copyShortcut = QShortcut(QKeySequence.Copy, self)
        pasteShortcut = QShortcut(QKeySequence.Paste, self)

        copyShortcut.activated.connect(self.copy)
        pasteShortcut.activated.connect(self.paste)

    def setData(self, data):
        self.setRowCount(0)  # erase data
        row, col = len(data), len(data[0])
        self.setColumnCount(col)
        self.setRowCount(row)
        # print(data)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.setItem(i, j, item)

    def data1(self):
        r = np.zeros(shape=(self.rowCount(), self.columnCount()), dtype=float)
        # r = [[0. for i in range(self.columnCount())] for i in range(self.rowCount())]
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                r[i, j] = float(self.item(i, j).text())
        return r

    def data2(self):
        r = [['' for i in range(self.columnCount())] for i in range(self.rowCount())]
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                r[i][j] = self.item(i, j).text()
        return r

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            i = self.currentRow() + 1
            j = self.currentColumn()
            if i == self.rowCount():
                self.setRowCount(i + 1)
                for kk in range(self.columnCount()):
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.setItem(i, kk, item)
            self.setCurrentCell(i, j)
            event.accept()

    def copy(self):
        selectedRangeList = self.selectedRanges()
        if selectedRangeList == []:
            return

        text = ""
        selectedRange = selectedRangeList[0]
        for i in range(selectedRange.rowCount()):
            if i > 0:
                text += "\n"
            for j in range(selectedRange.columnCount()):
                if j > 0:
                    text += "\t"
                itemA = self.item(selectedRange.topRow() + i, selectedRange.leftColumn() + j)
                if itemA:
                    text += itemA.text()
        text += '\n'

        QApplication.clipboard().setText(text)

    def paste(self):
        # 1\t2\n2\t3\n
        text = QApplication.clipboard().text()
        self._paste(text)

    def _paste(self, text):
        rows = text.split('\n')
        numRows = len(rows) - 1
        numColumns = rows[0].count('\t') + 1

        if self.currentRow() + numRows > self.rowCount():
            prevRowCount = self.rowCount()
            self.setRowCount(self.currentRow() + numRows)
            for i in range(prevRowCount, self.currentRow() + numRows):
                for kk in range(self.columnCount()):
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.setItem(i, kk, item)

        for i in range(numRows):
            columns = rows[i].split('\t')
            for j in range(numColumns):
                row = self.currentRow() + i
                column = self.currentColumn() + j
                if column < self.columnCount():
                    self.item(row, column).setText(columns[j] if isinstance(columns[j], str) else '')


class XYTableDialog(QDialog):
    def __init__(self, horizonatlHearderLabels, data, parent=None):
        super().__init__(parent)

        self.table = MyTable(horizonatlHearderLabels, parent)
        self.table.setData(data)

        # self.loadButton = QPushButton("&Load")
        self.saveButton = QPushButton("&Save")
        self.closeButton = QPushButton("&Close")
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()

        # bottomLayout.addWidget(self.loadButton)
        bottomLayout.addWidget(self.saveButton)
        bottomLayout.addWidget(self.closeButton)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(bottomLayout)

        self.setLayout(layout)

        # self.loadButton.clicked.connect(self.load)
        self.saveButton.clicked.connect(self.save)
        self.closeButton.clicked.connect(self.close)


    def load(self):
        pass
        # with open("members.csv") as fp:

    def save(self):
        data2D = self.data2()
        data1D = []
        for el in data2D:
            data1D.append(','.join(el))
        data = '\n'.join(data1D)
        with open("result.csv", 'w') as fp:
            fp.write(data)

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    data = np.array([[0.0, 0.9],
                     [0.2, 11.0],
                     [0.4, 15.4],
                     [0.6, 12.9],
                     [0.8, 8.5],
                     [1.0, 7.1],
                     [1.2, 4.0],
                     [1.4, 13.6],
                     [1.6, 22.2],
                     [1.8, 22.2]])

    dlg = XYTableDialog(["X", "Y"], data)
    # print(dlg.table.data1())
    dlg.show()
    #    table = MyTable(["X","Y","Z"])
    #    table.setData(data)
    #    table.show()

    app.exec_()

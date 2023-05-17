import sys , qtawesome , qdarkstyle
import colorama

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# TODO: Set icon colour and copy code with color kwarg

VIEW_COLUMNS = 5
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = 'All'

# A Python 
class Mainwindow(QMainWindow):
    """
    A small browser window that allows the user to search through all icons from
    the available version of QtAwesome.  You can also copy the name and python
    code for the currently selected icon.
    """


    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self) :
        self.setMinimumSize(400, 300)
        self.setWindowTitle('QtAwesome Icon Browser')

        qtawesome._instance()
        fontMaps = qtawesome._resource['iconic'].charmap

        iconNames = []
        for fontCollection, fontData in fontMaps.items():
            for iconName in fontData:
                iconNames.append('%s.%s' % (fontCollection, iconName))

        self._filterTimer = QTimer(self)
        self._filterTimer.setSingleShot(True)
        self._filterTimer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filterTimer.timeout.connect(self._updateFilter)

        model = IconModel(self.palette().color(QPalette.Light ))
        model.setStringList(sorted(iconNames))

        self._proxyModel = QSortFilterProxyModel()
        self._proxyModel.setSourceModel(model)
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._listView = IconListView(self)
        self._listView.setUniformItemSizes(True)
        self._listView.setViewMode(QListView.IconMode)
        self._listView.setModel(self._proxyModel)
        self._listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self._listView.doubleClicked.connect(self._copyIconText)

        self._lineEdit = QLineEdit(self)
        self._lineEdit.setMaximumSize(0,30)
        self._lineEdit.textChanged.connect(self._triggerDelayedUpdate)
        self._lineEdit.returnPressed.connect(self._triggerImmediateUpdate)

        self._comboBox = QComboBox(self)
        self._comboBox.setFixedSize(120 , 30)
        self._comboBox.currentIndexChanged.connect(self._triggerImmediateUpdate)
        self._comboBox.addItems([ALL_COLLECTIONS] + sorted(fontMaps.keys()))

        self.spacer = QSplitter(Qt.Horizontal)
        self.spacer.setStyleSheet("background-color : none ;")
        self.showSearchBtn_ = QToolButton(self  )
        self.showSearchBtn_.setFixedSize(30,30)
        self.showSearchBtn_.clicked.connect( lambda : self.showSearchBar() )
        self.showSearchBtn_.setIconSize(QSize(30,30))
        self.showSearchBtn_.setIcon( qtawesome.icon( "fa.search" , color = "White" ) ) 
        lyt = QHBoxLayout()
        lyt.setContentsMargins(2, 2, 2, 2)
        lyt.setSpacing(4)
        lyt.addWidget(self.spacer)
        lyt.addWidget(self._comboBox)
        self.statusBar_ = QStatusBar(self)
        self.statusBar_.setStyleSheet("background-color : none ; border : none ; ")
        lyt.addWidget(self._lineEdit)
        lyt.addWidget(self.showSearchBtn_ )
        searchBarFrame = QFrame(self)
        searchBarFrame.setFixedHeight(35)
        searchBarFrame.setLayout(lyt)

    

        lyt = QVBoxLayout()
        lyt.setContentsMargins(0,0,0,0)
        lyt.addWidget(searchBarFrame)
        lyt.addWidget(self._listView)
        lyt.addWidget(self.statusBar_)
        frame = QFrame(self)
        frame.setLayout(lyt)

        self.setCentralWidget(frame)

        QShortcut(
            QKeySequence(Qt.Key_Return),
            self,
            self._copyIconText,
        )

        self._lineEdit.setFocus()

        geo = self.geometry()
        desktop = QApplication.desktop()
        screen = desktop.screenNumber(desktop.cursor().pos())
        centerPoint = desktop.screenGeometry(screen).center()
        geo.moveCenter(centerPoint)
        self.setGeometry(geo)
    def showSearchBar(self) :
        width =  self._lineEdit.maximumWidth() 
        if width == 0 : self._lineEdit.setMaximumWidth(250)
        if width == 250 : self._lineEdit.setMaximumWidth(0)
    def _updateFilter(self):
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        reString = ""

        group = self._comboBox.currentText()
        if group != ALL_COLLECTIONS:
            reString += r"^%s\." % group

        searchTerm = self._lineEdit.text()
        if searchTerm:
            reString += ".*%s.*$" % searchTerm

        self._proxyModel.setFilterRegExp(reString)

    def _triggerDelayedUpdate(self):
        """
        Reset the timer used for committing the search term to the proxy model.
        """
        self._filterTimer.stop()
        self._filterTimer.start()

    def _triggerImmediateUpdate(self):
        """
        Stop the timer used for committing the search term and update the
        proxy model immediately.
        """
        self._filterTimer.stop()
        self._updateFilter()

    def _copyIconText(self):
        """
        Copy the name of the currently selected icon to the clipboard.
        """
        indexes = self._listView.selectedIndexes()
        if not indexes:
            return

        clipboard = QApplication.instance().clipboard()
        clipboard.setText( indexes[0].data())
        self.statusBar
        self.statusBar_.showMessage( f""" { indexes[0].data() } has been coppied to your clipboard""",2000)


class IconListView(QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def resizeEvent(self, event):
        """
        Re-implemented to re-calculate the grid size to provide scaling icons

        Parameters
        ----------
        event : QEvent
        """
        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tileWidth = width / VIEW_COLUMNS
        iconWidth = int(tileWidth * 0.8)

        self.setGridSize(QSize(int(tileWidth), int(tileWidth)))
        self.setIconSize(QSize(int(iconWidth), int(iconWidth)))

        return super().resizeEvent(event)


class IconModel(QStringListModel):

    def __init__(self, iconColor):
        super().__init__()
        self._iconColor = iconColor

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """
        Re-implemented to return the icon for the current index.

        Parameters
        ----------
        index : QModelIndex
        role : int

        Returns
        -------
        Any
        """
        if role == Qt.DecorationRole:
            iconString = self.data(index, role=Qt.DisplayRole)
            return qtawesome.icon(iconString, color=self._iconColor)
        return super().data(index, role)


if __name__ == "__main__" :
    iconBrowser = QApplication(sys.argv)
    iconBrowser.setFont(QFont("arial",12))
    iconBrowser.setWindowIcon(QIcon("folder.ico"))
    iconBrowser.setStyleSheet( qdarkstyle.load_stylesheet_pyqt5() )
    Mw = Mainwindow()
    Mw.show()
    sys.exit(iconBrowser.exec_())


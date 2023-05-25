import sys , qtawesome , os
from tkinter import ALL
from time import sleep

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from qtawesome import icon 

# TODO: Set icon colour and copy code with color kwarg

VIEW_COLUMNS = 5
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = 'All'

# A Python 
class Mainwindow(QWidget):
    
    """
    A small browser window that allows the user to search through all icons from
    the available version of QtAwesome.  You can also copy the name and python
    code for the currently selected icon.
    
    """
    icon_color = "white"
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self) :
        self.setMinimumSize(750, 500)
        self.setWindowTitle('QtAwesome Icon Browser')
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(QHBoxLayout())
        self.setTheme("dark")
        
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
        
        # Mainwindow
        container = QWidget()
        container.setObjectName("Mainwindow")
        container.setLayout(QHBoxLayout())
        container.layout().setContentsMargins(2,2,2,2)
        container.layout().setSpacing(0)
        # contentwidget 
        contentwidget = QFrame()
        contentwidget.setObjectName("contentwidget")
        contentwidget.setLayout(QVBoxLayout())
        contentwidget.layout().setContentsMargins(0,0,0,0)
        contentwidget.layout().setSpacing(0)
        # title bar
        titlebar = QFrame()
        titlebar.setObjectName("titlebar")
        titlebar.setFixedHeight(35)
        titlebar.setLayout(QHBoxLayout())
        titlebar.layout().setContentsMargins(2,2,2,2)
        #!
        extBtn = QToolButton(clicked = lambda : self.close() )
        extBtn.setObjectName("extBtn")
        extBtn.setFixedSize(30,30)
        extBtn.setIcon(icon("fa.close" , color="#D90368"))
        extBtn.setIconSize(QSize(30,30))
        #!
        appBtn = QToolButton(text = "All icons" , clicked = lambda : self._triggerImmediateUpdate(ALL_COLLECTIONS))
        appBtn.setObjectName(ALL_COLLECTIONS)
        appBtn.setFixedHeight(30)
        #!
        eiBtn = QToolButton(text="ei" , clicked = lambda : self._triggerImmediateUpdate("ei") )
        eiBtn.setObjectName("ei")
        eiBtn.setFixedHeight(30)
        #!
        faBtn = QToolButton(text="fa", clicked = lambda : self._triggerImmediateUpdate("fa") )
        faBtn.setObjectName("fa")
        faBtn.setFixedHeight(30)
        #!
        fa5Btn = QToolButton(text="fa5", clicked = lambda : self._triggerImmediateUpdate("fa5") )
        fa5Btn.setObjectName("fa5")
        fa5Btn.setFixedHeight(30)
        #!
        fa5bBtn = QToolButton(text="fa5b", clicked = lambda : self._triggerImmediateUpdate("fa5b") )
        fa5bBtn.setObjectName("fa5b")
        fa5bBtn.setFixedHeight(30)
        #!
        fa5sBtn = QToolButton(text="fa5s", clicked = lambda : self._triggerImmediateUpdate("fa5s") )
        
        fa5sBtn.setObjectName("fa5s")
        fa5sBtn.setFixedHeight(30)
        #!
        mdiBtn = QToolButton(text="mdi", clicked = lambda : self._triggerImmediateUpdate("mdi") )
        mdiBtn.setObjectName("mdi")
        mdiBtn.setFixedHeight(30)
        #!
        self.searchEdit = QLineEdit(self)
        self._triggerImmediateUpdate(ALL_COLLECTIONS)
        self.searchEdit.setObjectName("searchEdit")
        self.searchEdit.setMaximumWidth(0)        
        self.searchEdit.setPlaceholderText("Search for icon ...")
        self.searchBtn = QToolButton(clicked = lambda : self.showSearchBar())
        self.searchBtn.setFixedSize(28,28)
        self.searchBtn.setIcon(icon("fa.search" , color="#D90368"))
        self.searchBtn.setIconSize(QSize(28,28))
        self.searchEdit.textChanged.connect(self._triggerDelayedUpdate)
        self.searchEdit.returnPressed.connect(self._triggerImmediateUpdate)
        #!
        titlebar.layout().addWidget(appBtn)
        titlebar.layout().addWidget(eiBtn)
        titlebar.layout().addWidget(faBtn)
        titlebar.layout().addWidget(fa5Btn)
        titlebar.layout().addWidget(fa5bBtn)
        titlebar.layout().addWidget(fa5sBtn)
        titlebar.layout().addWidget(mdiBtn)
        titlebar.layout().addWidget( QSplitter(orientation=Qt.Horizontal) )
        titlebar.layout().addWidget(self.searchEdit)
        titlebar.layout().addWidget(self.searchBtn)
        titlebar.layout().addWidget(extBtn)
        # central widget 
        c_widget = QFrame()
        c_widget.setObjectName("CentralWidget")
        c_widget.setLayout(QHBoxLayout())
        c_widget.layout().setContentsMargins(0,0,0,0)
        self.icon_view = IconListView(self)
        self.icon_view.setUniformItemSizes(True)
        self.icon_view.setViewMode(QListView.IconMode)
        self.icon_view.setModel(self._proxyModel)
        self.icon_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.icon_view.doubleClicked.connect(self.updatStatusBarMessage)
        c_widget.layout().addWidget(self.icon_view)

        #! Status Bar
        self.statusBar = QFrame(self)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.setLayout(QHBoxLayout())
        self.statusBar.layout().setContentsMargins(0,0,0,0)
        self.statusBar.setFixedHeight(20)
        self.statusLabel = QLabel()
        self.statusBar.layout().addWidget(self.statusLabel)
        self.statusBar.layout().addWidget( QSizeGrip(self.statusBar) )
        #! layouts
        contentwidget.layout().addWidget(titlebar)
        # ! contentwidget layout
        contentwidget.layout().addWidget(c_widget)
        contentwidget.layout().addWidget(self.statusBar)
        # ! container layout 
        container.layout().addWidget(contentwidget)
        # App Layout
        self.layout().addWidget(container)
    def setTheme(self,theme : str ) :
        if theme == "light" :
            self.icon_color = "black" 
        self.theme = open(f"{os.curdir}/themes/{theme}.css","r")
        qApp.setStyleSheet( self.theme.read() )
        return self.theme , self.icon_color
    
    def showSearchBar(self) :
        width =  self.searchEdit.maximumWidth() 
        if width == 0 : self.searchEdit.setMaximumWidth(250)
        if width == 250 : self.searchEdit.setMaximumWidth(0)
    def _updateFilter(self):
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        reString = ""
        group = self.current_filter
        if group != ALL_COLLECTIONS:
            reString += r"^%s\." % group

        searchTerm = self.searchEdit.text()
        if searchTerm:
            reString += ".*%s.*$" % searchTerm

        self._proxyModel.setFilterRegExp(reString)

    def _triggerDelayedUpdate(self , filter):
        """
        Reset the timer used for committing the search term to the proxy model.
        """
        self._filterTimer.stop()
        self._filterTimer.start()

    def _triggerImmediateUpdate(self, group = ""):
        """
        Stop the timer used for committing the search term and update the
        proxy model immediately.
        """
        self.current_filter = group
        
        stylesheet = "#".__str__() + group.__str__() + "{color : #D90368}".__str__()
        self.setStyleSheet(stylesheet)
        self._updateFilter()
        
    def updatStatusBarMessage(self) :
        """
        Copy the name of the currently selected icon to the clipboard.
        then show a message that the selected icon has been coppied to clipboard
        """
        self.indexes = self.icon_view.selectedIndexes()
        if not self.indexes:
            return
        clipboard = QApplication.instance().clipboard()
        clipboard.setText( self.indexes[0].data())
        self.statusLabel.setText(f"""<span style='color : #D90368 ;'>{ self.indexes[0].data() }</span> has been coppied to your clipboard""")
        timer = QTimer(self)
        timer.timeout.connect( lambda : self.statusLabel.clear() )
        timer.start(2000)
class IconListView(QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        scrollBar = QScrollBar(self)
        scrollBar.setObjectName("scrollBar")
        self.setVerticalScrollBar(scrollBar)
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
    Mw = Mainwindow()
    Mw.show()
    sys.exit(iconBrowser.exec_())
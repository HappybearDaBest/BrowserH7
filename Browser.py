import sys
from PyQt5.QtCore import QUrl, Qt, QEventLoop
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QTabWidget, QAction, QMenu, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings, QWebEngineProfile

class WebBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 800, 600)  # Set the window size explicitly

        self.url_entry = QLineEdit()
        self.url_entry.returnPressed.connect(self.load_url)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("back.png"))

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("forward.png"))

        self.reload_button = QPushButton()
        self.reload_button.setIcon(QIcon("reload.png"))

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.homepage = "https://www.google.com"  # Set the homepage URL to google.com

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_tab)

        self.tab_bar_layout = QHBoxLayout()
        self.tab_bar_layout.addWidget(self.new_tab_button)
        self.tab_bar_layout.addStretch()

        self.tab_bar_widget = QWidget()
        self.tab_bar_widget.setLayout(self.tab_bar_layout)

        self.add_tab()

        self.back_button.clicked.connect(self.back)
        self.forward_button.clicked.connect(self.forward)
        self.reload_button.clicked.connect(self.reload)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.back_button)
        toolbar_layout.addWidget(self.forward_button)
        toolbar_layout.addWidget(self.reload_button)
        toolbar_layout.addWidget(self.url_entry)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)

        layout = QVBoxLayout()
        layout.addWidget(toolbar_widget)
        layout.addWidget(self.tab_bar_widget)
        layout.addWidget(self.tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        # Create bookmarks menu
        self.bookmarks_menu = QMenu(self)
        self.bookmarks_menu.aboutToShow.connect(self.update_bookmarks_menu)

        self.bookmarks_action = QAction("Bookmarks", self)
        self.bookmarks_action.setMenu(self.bookmarks_menu)

        # Create three dots menu
        self.more_menu = QMenu(self)
        self.more_menu.addAction(self.bookmarks_action)

        self.more_button = QPushButton("...")
        self.more_button.setMenu(self.more_menu)

        self.tab_bar_layout.addWidget(self.more_button)

        self.bookmarks = []

    def add_tab(self):
        browser = QWebEngineView()
        browser.page().settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        browser.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        browser.page().settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 Edg/100.0.0.0')

        self.tab_widget.addTab(browser, "New Tab")

        index = self.tab_widget.count() - 1
        self.tab_widget.setCurrentIndex(index)

        url = QUrl(self.homepage)
        browser.load(url)

        tab_button = QPushButton("x")
        tab_button.clicked.connect(lambda checked, index=index: self.close_tab(index))

        self.tab_widget.tabBar().setTabButton(index, QTabBar.RightSide, tab_button)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            browser_widget = self.tab_widget.widget(index)
            browser_widget.deleteLater()
            self.tab_widget.removeTab(index)

    def load_url(self):
        url = self.url_entry.text()
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            current_browser.load(QUrl.fromUserInput(url))

    def back(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            if current_browser.page().history().canGoBack():
                current_browser.page().history().back()

    def forward(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            if current_browser.page().history().canGoForward():
                current_browser.page().history().forward()

    def reload(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            current_browser.page().reload()

    def update_title(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            title = current_browser.page().title()
            self.setWindowTitle(f"{title} - Web Browser")

    def update_url(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            url = current_browser.url().toString()
            self.url_entry.setText(url)

    def update_icon(self):
        if self.tab_widget.count() > 0:
            current_browser = self.tab_widget.currentWidget()
            icon = current_browser.icon()
            self.setWindowIcon(icon)

    def update_bookmarks_menu(self):
        self.bookmarks_menu.clear()
        for bookmark in self.bookmarks:
            action = self.bookmarks_menu.addAction(bookmark)
            action.triggered.connect(lambda checked, url=bookmark: self.tab_widget.currentWidget().load(QUrl.fromUserInput(url)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser_window = WebBrowserApp()
    browser_window.show()
    sys.exit(app.exec_())

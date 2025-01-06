import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Python Browser Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a web engine view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("file://" + "index.html"))  # Load the HTML file

        # Set the central widget
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

        # Open developer tools (optional)
        self.browser.settings().setAttribute(
            self.browser.settings().DeveloperExtrasEnabled, True
        )


def main():
    app = QApplication(sys.argv)

    # Create and show the main browser window
    main_window = BrowserWindow()
    main_window.show()

    # Handle application lifecycle
    def handle_quit():
        print("Application is quitting...")

    app.aboutToQuit.connect(handle_quit)

    # Execute the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

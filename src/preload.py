import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a layout and central widget
        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Add labels for versions
        self.chrome_label = QLabel("Chrome Version: Not Available")
        self.node_label = QLabel("Node.js Version: Not Available")
        self.electron_label = QLabel("Electron Version: Not Available")

        self.layout.addWidget(self.chrome_label)
        self.layout.addWidget(self.node_label)
        self.layout.addWidget(self.electron_label)

        # Populate the labels with version information
        self.replace_text("chrome", "Not Available")
        self.replace_text("node", "Not Available")
        self.replace_text("electron", "Not Available")

    def replace_text(self, selector: str, text: str):
        """
        Update the text of the label corresponding to the given selector.
        """
        if selector == "chrome":
            self.chrome_label.setText(f"Chrome Version: {text}")
        elif selector == "node":
            self.node_label.setText(f"Node.js Version: {text}")
        elif selector == "electron":
            self.electron_label.setText(f"Electron Version: {text}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Version Information")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit,
    QLabel, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem, QProgressBar, QFileDialog, QTextEdit
)
from PyQt5.QtCore import Qt
import threading
from scraper import scrape_data  # Import scraping function

class ScraperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Input fields
        layout.addLayout(self.create_input_section())

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(['Page', 'Title', 'Price (€)', 'Link'])
        layout.addWidget(self.results_table)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Status log
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        layout.addWidget(self.status_log)

        # Start button
        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.start_button)

        self.central_widget.setLayout(layout)

    def create_input_section(self):
        input_layout = QHBoxLayout()

        # Keywords input
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Enter keywords (comma-separated)")
        input_layout.addWidget(QLabel("Keywords:"))
        input_layout.addWidget(self.keywords_input)

        # Price range
        self.price_low_input = QSpinBox()
        self.price_low_input.setRange(0, 10000)
        self.price_low_input.setValue(200)

        self.price_high_input = QSpinBox()
        self.price_high_input.setRange(0, 10000)
        self.price_high_input.setValue(2000)

        input_layout.addWidget(QLabel("Price Range (€):"))
        input_layout.addWidget(self.price_low_input)
        input_layout.addWidget(self.price_high_input)

        # Exclude keyword
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("Enter excluded keyword")
        input_layout.addWidget(QLabel("Exclude:"))
        input_layout.addWidget(self.exclude_input)

        # Output file path
        self.output_path_button = QPushButton("Set Output Path")
        self.output_path_button.clicked.connect(self.select_output_path)
        self.output_path_label = QLabel("output.xlsx")

        input_layout.addWidget(self.output_path_button)
        input_layout.addWidget(self.output_path_label)

        return input_layout

    def select_output_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            self.output_path_label.setText(file_path)

    def start_scraping(self):
        # Collect input values
        keywords = self.keywords_input.text().split(',')
        price_low = self.price_low_input.value()
        price_high = self.price_high_input.value()
        excluded_keyword = self.exclude_input.text()
        output_file = self.output_path_label.text()

        if not keywords or not output_file:
            self.status_log.append("Please provide all inputs.")
            return

        # Start scraping in a thread
        self.start_button.setEnabled(False)
        thread = threading.Thread(target=self.run_scraper, args=(keywords, price_low, price_high, excluded_keyword, output_file))
        thread.start()

    def run_scraper(self, keywords, price_low, price_high, excluded_keyword, output_file):
        def update_progress(page_number):
            self.progress_bar.setValue(page_number * 10)

        try:
            data = scrape_data(keywords, price_low, price_high, excluded_keyword, output_file, update_progress)
            self.display_results(data)
            self.status_log.append("Scraping completed successfully.")
        except Exception as e:
            self.status_log.append(f"Error: {e}")
        finally:
            self.start_button.setEnabled(True)

    def display_results(self, data):
        self.results_table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.results_table.setItem(row, 0, QTableWidgetItem(str(item['Page'])))
            self.results_table.setItem(row, 1, QTableWidgetItem(item['Title']))
            self.results_table.setItem(row, 2, QTableWidgetItem(str(item['Price (€)'])))
            self.results_table.setItem(row, 3, QTableWidgetItem(item['Link']))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ScraperGUI()
    gui.show()
    sys.exit(app.exec_())
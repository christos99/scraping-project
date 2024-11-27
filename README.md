
# **Scraping Project**

This project is a web scraper built using Python, Selenium, and PyQt5. It features a graphical user interface (GUI) that allows users to scrape data based on user-defined parameters such as keywords, price range, and exclusions, and save the results to an Excel file.

---

## **Features**
- **Scrape Listings**: Retrieve data such as page numbers, titles, prices, and links from a website.
- **GUI Interface**: Intuitive PyQt5-based GUI for inputting parameters and viewing results.
- **Customizable Search**:
  - Specify keywords to filter listings.
  - Define a price range.
  - Exclude unwanted keywords from results.
- **Progress Tracking**: A progress bar shows the scraping progress in real-time.
- **Save Results**: Save the scraped data into an Excel file.
- **Logging**: Includes logging for tracking the scraping process and troubleshooting.

---

## **Requirements**
Make sure you have the following installed:
- **Python 3.7+**
- **pip** (Python package manager)
- **Google Chrome** (latest version)
- **ChromeDriver** (compatible with your Chrome version)

Python dependencies:
- `PyQt5`
- `Selenium`
- `pandas`
- `openpyxl`

---

## **Setup Instructions**

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/scraping_project.git
cd scraping_project
```

### 2. **Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Download ChromeDriver**
- Download ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
- Ensure the version matches your installed Google Chrome version.
- Place the `chromedriver` executable in your system's PATH or in the project folder.

---

## **Usage**

### **Run the GUI**
1. Start the application:
   ```bash
   python gui.py
   ```
2. In the GUI:
   - Enter **keywords** (comma-separated).
   - Set a **price range**.
   - Specify an **excluded keyword** (optional).
   - Choose an **output file path** to save the results.
   - Click **"Start Scraping"** to begin.

3. View the scraping progress in the **status log** and **progress bar**.

4. Once scraping is complete, view the results in the GUI table or in the saved Excel file.

---

## **Project Structure**
```
scraping_project/
│
├── gui.py             # PyQt5 GUI for the scraper
├── scraper.py         # Core scraping logic using Selenium
├── .gitignore         # Files to ignore in Git (e.g., venv, logs)
├── venv/              # Virtual environment folder (ignored)
├── pyvenv.cfg         # Virtual environment configuration
└── README.md          # Project documentation
```

---

## **Example Workflow**
1. Set the following parameters:
   - Keywords: `iPhone, Pro`
   - Price range: `200` to `2000`
   - Excluded keyword: `11`

2. Choose an output file name, e.g., `results.xlsx`.

3. Click **"Start Scraping"**.

4. View the progress in the log and check the saved Excel file for results.

---

## **Troubleshooting**
- **Selenium Errors**: Ensure ChromeDriver matches your Chrome version.
- **Dependencies Missing**: Reinstall them with:
  ```bash
  pip install -r requirements.txt
  ```
- **GUI Issues**: Ensure `PyQt5` is installed properly.

---

## **Contributing**
Feel free to submit issues or pull requests to improve the project.

---

## **License**
This project is licensed under the MIT License.

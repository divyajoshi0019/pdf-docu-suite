# PDF Merger Web Application

This is a simple web application that allows you to merge up to 5 PDF files into a single document.

## Project Structure

```
C:/Users/divya/pdf-merger/
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Frontend HTML
└── static/
    ├── style.css        # CSS for styling
    └── script.js        # JavaScript for interactivity
```

## How to Run Locally

Follow these steps to run the PDF Merger application on your local machine.

### Step 1: Navigate to the Project Directory

First, open your terminal or command prompt and navigate to the `pdf-merger` directory that was created.

```bash
cd C:/Users/divya/pdf-merger
```

### Step 2: Create a Virtual Environment

It's a good practice to create a virtual environment to manage project-specific dependencies.

**On Windows:**

```bash
python -m venv venv
.\\venv\\Scripts\\activate
```

You should see `(venv)` at the beginning of your terminal prompt, indicating that the virtual environment is active.

### Step 3: Install Dependencies

Install the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install Flask and pypdf.

### Step 4: Run the Application

Now you can run the Flask application.

```bash
python app.py
```

You should see output similar to this, indicating that the server is running:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ...
```

### Step 5: Access the Application

Open your web browser and go to the following address:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

You should now see the PDF Merger application running in your browser.

### How to Use the App

1.  Click the "Choose files" button or drag and drop your PDF files into the designated area.
2.  You can select up to 5 PDF files.
3.  The names of the selected files will appear.
4.  Click the "Merge PDFs" button.
5.  The application will merge the files, and a download for the `merged.pdf` file will start automatically.
6.  If there are any errors (e.g., non-PDF files, too many files), an error message will be displayed. 
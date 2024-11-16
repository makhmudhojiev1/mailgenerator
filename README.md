# Temporary Email Generator

This project allows users to generate temporary email addresses using the **Mail.tm** service. The project has three interfaces:

- **Web Interface**: A simple web application using **Flask**.
- **GUI Interface**: A graphical user interface built with **Tkinter**.
- **CLI Interface**: A command-line interface for generating and managing temporary emails.

## Features

- **Generate Random Email**: Create a random temporary email address with a custom domain.
- **Copy Email**: Copy the generated email address to the clipboard for easy use.
- **Listen for Emails**: Start listening for incoming emails and display them on the interface.
- **Customizable**: Specify a custom username for the email address.
  
## Requirements

### Dependencies for all versions:
- **Flask** (for the Web Interface)
- **Tkinter** (for the GUI Interface, usually comes pre-installed with Python)
- **mailtm** (for interacting with the Mail.tm API)

Dependencies are listed in the `requirements.txt` file.

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/rexflores/Temp-Mail-Generator.git
cd temp-email-generator
```

### 2. Set up a virtual environment (optional but recommended):

For **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

For **Mac/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Web Interface

To use the **Web Interface**:

1. Run the Flask app:

   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5000/`.

3. You can generate a temporary email, copy it, and listen for incoming emails directly on the web page.

---

### GUI Interface (Tkinter)

To use the **GUI Interface**:

1. Navigate to the `GUI` folder:

   ```bash
   cd GUI
   ```

2. Run the Tkinter GUI version by executing:

   ```bash
   python gui_app.py
   ```

3. The Tkinter window will open, and you can interact with the application to generate and manage temporary email addresses.

---

### CLI Interface

To use the **CLI Interface**:

1. Navigate to the `CLI` folder:

   ```bash
   cd CLI
   ```

2. Run the Python script from the command line:

   ```bash
   python cli_app.py
   ```

3. The CLI will prompt you with options to generate an email, copy it, and start listening for incoming emails. You interact using the terminal.

---

## Deploying to Vercel (Web Version)

To deploy the **Web Interface** to **Vercel**, follow these steps:

1. Sign up or log in to [Vercel](https://vercel.com).
2. Install Vercel CLI globally:

    ```bash
    npm install -g vercel
    ```

3. Run the following command in the root of your project directory:

    ```bash
    vercel
    ```

4. Vercel will automatically deploy your project and give you a URL (e.g., `https://your-project-name.vercel.app`).

### Vercel Configuration

The project includes a `vercel.json` configuration file that tells Vercel how to build and serve the Flask app. It uses the `@vercel/python` runtime and routes all traffic to `app.py`.

---

## Project Structure

Here is the updated structure of the project:

```
/Temp-Mail-Generator
│
├── app.py                # Main Flask application for the Web Interface
├── requirements.txt      # List of dependencies
├── vercel.json           # Vercel deployment configuration
├── /templates
│   └── index.html        # HTML template for the Web Interface UI
│
├── /GUI
│   └── gui_app.py        # Tkinter GUI application for the GUI version
│
└── /CLI
    └── cli_app.py        # CLI application for the Command-Line Interface version
```

---

## Troubleshooting

- **ModuleNotFoundError**: If you encounter issues related to missing modules, make sure all dependencies are listed in `requirements.txt` and that you have installed them using `pip install -r requirements.txt`.
- **Deployment Errors on Vercel**: Ensure that your `vercel.json` and `runtime.txt` are properly configured and that you are using a supported Python version (e.g., Python 3.9).
- **GUI Issues**: If the Tkinter GUI doesn't open or work, ensure that you have Tkinter installed (it is usually pre-installed with Python, but can be installed manually if needed).
- **CLI Issues**: Make sure you run the CLI scripts from the terminal and follow the prompts correctly.

---

## Contributing

Feel free to contribute to this project by creating issues, submitting pull requests, or suggesting improvements. All contributions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# Identifying-and-Resolving-XSS-Vulnerabilities-using-AI

## Overview
This project automates the detection and resolution of Cross-Site Scripting (XSS) vulnerabilities using AI. It integrates with GitHub for repository management, a file upload system, and an AI model to analyze and patch security issues in the codebase. The application provides a web interface for easy interaction and automates key tasks in the vulnerability analysis and fix process.

## Features
**Automatic XSS Detection:** Uses SonarQube to scan for vulnerabilities (can be extended to integrate with other scanning tools).
**AI-Powered Fixes:** Leverages OpenAI's GPT-4 to analyze HTML files and generate secure patches for XSS vulnerabilities.
**GitHub Integration**: Clones repositories, updates code, and pushes secure changes back to GitHub.
**File Upload:** Supports uploading and processing files (e.g., vulnerability reports, code files) for further analysis.
**Web-Based Interface:** Provides an interactive UI for easy usage, enabling users to clone repositories, upload files, and trigger vulnerability fixes with a simple click.

## Prerequisites
Ensure you have the following installed before setting up the project:
Python 3.11.9
Flask
Git
OpenAI API access
Redis (optional, for caching if needed)
SonarQube instance (either locally or via SonarCloud) for vulnerability scanning



## Usage
**1. Running SonarQube Scan**
Ensure SonarQube is running, then execute:
**sonar-scanner -Dsonar.projectKey=xss_project -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.login=your_sonar_token**

**2. Identifying Vulnerabilities**
Once SonarQube completes the scan, the vulnerabilities are recorded in the report. You can upload a PDF report for further processing in the application.

**3. Running the Flask Application**
Start the Flask server to interact with the web interface:
**python app.py**

You can now access the app in your browser at http://localhost:8000. The application provides the following features:

Clone a GitHub repository by entering the repository URL.
Upload a file (e.g., a vulnerability report) for further analysis.
Trigger AI-based fixes for XSS vulnerabilities in HTML code.
Download the fixed HTML file.

**4. Pushing Fixed Code to GitHub**
After generating the fixes, the updated code will be saved and automatically pushed to the cloned repository. You can trigger this by using the Flask app's functionality.

  
## API Endpoints
| Endpoint              | Method | Description                                                    |
|:----------------------|:-------|:---------------------------------------------------------------|
| `/`                   | GET    | Displays the main page with instructions                        |
| `/generate`           | GET    | Clones a GitHub repository by URL                               |
| `/fileupload`         | GET    | Displays the file upload page                                   |
| `/upload`             | POST   | Handles the upload of a file (e.g., PDF report)                 |
| `/vulnerability`      | GET    | Displays the vulnerability page                                 |
| `/vulnerability_action`| GET  | Analyzes and fixes XSS vulnerabilities in the code based on uploaded files |






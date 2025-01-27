from flask import Flask, request, redirect, url_for, render_template
import subprocess
import os
# import pdfplumber
import fitz  # PyMuPDF
from openai import OpenAI

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET'])
def generate():
    repo_url = request.args.get('repo_url')
    if repo_url:
        try:
            clone_command = ["git", "clone", repo_url]
            subprocess.run(clone_command, capture_output=True, text=True, check=True)
            return redirect(url_for('fileupload'))
        except subprocess.CalledProcessError as e:
            return f"Failed to clone the repository:\n{e.stderr}", 500
    else:
        return "No repository URL provided.", 400


@app.route('/fileupload')
def fileupload():
    return render_template('fileupload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400

    if file:
        os.makedirs('./uploads', exist_ok=True)
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return redirect(url_for('vulnerability'))


@app.route('/vulnerability')
def vulnerability():
    return render_template('vulnerability.html')


@app.route('/vulnerability_action')
def vulnerability_action():
    fix_xss = request.args.get('fix_xss')
    if fix_xss == 'yes':
        # Path to the cloned repository's HTML file and the uploaded coverage report
        html_file_path = './xss/shipping.html'  # Update with actual file path if needed
        report_file_path = './uploads/Issues List.pdf'  # Update with actual file path if needed

        html_code = read_html_file(html_file_path)
        report_content = read_pdf_report(report_file_path)

        if html_code and report_content:
            fixed_code_file_path = send_to_gpt_for_fixing(html_code, report_content)
            if fixed_code_file_path:
                return f"Fixed HTML code saved to: {fixed_code_file_path}"
            else:
                return "Failed to process the HTML code.", 500
        else:
            return "Failed to read the HTML code or the PDF report.", 400
    else:
        return "Invalid action.", 400

def read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_pdf_report(file_path):
    try:
        pdf_document = fitz.open(file_path)
        text = ''
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text() + '\n'
        return text
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None

def send_to_gpt_for_fixing(html_code, report_content):
    client = OpenAI(api_key="api_key")

    prompt = f"""
    Analyze the .html file given and understand the XSS vulnerabilities present in the code. IssuesList.pdf file would contain the list of the vulnerabilities along with their vulnerability type.
    After careful understanding of those two files, change the code where those vulnerabilities are handled so that the XSS vulnerability does not exist. When the code is run in SonarQube, it has to pass saying no vulnerabilities.
    Please ensure that the code is compiled with clean code standards and that there should not be any maintainability or reliability or consistency vulnerabilities present.
    HTML Code:
    {html_code}

    Report Content:
    {report_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Analyze the .html file given and understand the XSS vulnerabilities present in the code. The Issues List.pdf file would contain the list of the vulnerabilities along with their vulnerability type. After careful understanding of those two files, change the code where those vulnerabilities are handled so that the XSS vulnerability does not exist. When the code is run in SonarQube, it has to pass saying no vulnerabilities. Please ensure that the code is compiled with clean code standards and that there should not be any maintainability or reliability or consistency vulnerabilities present."},
                {"role": "user", "content": prompt}
            ]
        )
        response_content = response.choices[0].message.content.strip()
        print("GPT-4 Response:\n")
        print(response_content)

        output_file_path = 'updated_code.html'
        with open(output_file_path, "w") as file:
            file.write(response_content)

        return output_file_path

    except Exception as e:
        print(f"An error occurred while communicating with OpenAI: {e}")
        return None


if __name__ == '__main__':
    app.run(port=8000)

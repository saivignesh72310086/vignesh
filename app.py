from flask import Flask, render_template, request, redirect, url_for
import spacy
from docx import Document
import PyPDF2
import re
from roadmap_generator import suggest_jobs_from_resume, generate_roadmap_for_job

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


def extract_skills(text):
    doc = nlp(text)
    return set(chunk.text.lower().strip()
               for chunk in doc.noun_chunks
               if not any(token.is_stop or token.is_punct for token in chunk))


def extract_text_from_docx(file):
    return '\n'.join([para.text for para in Document(file).paragraphs])


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return '\n'.join([page.extract_text() for page in pdf_reader.pages])


@app.route('/')
def home():
    return redirect(url_for('resume_analyzer'))


@app.route('/resume-analyzer', methods=['GET', 'POST'])
def resume_analyzer():
    resume_text, job_desc_text, results, error = '', '', None, None

    if request.method == 'POST':
        if 'resume_file' in request.files and request.files['resume_file'].filename != '':
            file = request.files['resume_file']
            if file.filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(file)
            elif file.filename.endswith(('.doc', '.docx')):
                resume_text = extract_text_from_docx(file)
            else:
                error = "Unsupported file type."
        else:
            resume_text = request.form.get('resume_text', '')

        job_desc_text = request.form.get('job_desc_text', '')

        if resume_text and job_desc_text:
            resume_skills = extract_skills(resume_text)
            job_desc_skills = extract_skills(job_desc_text)

            matched = resume_skills & job_desc_skills
            missing = job_desc_skills - resume_skills
            percent = (len(matched) / len(job_desc_skills)) * 100 if job_desc_skills else 0

            results = {
                'resume_skills': resume_skills,
                'job_desc_skills': job_desc_skills,
                'matched_skills': matched,
                'missing_skills': [s for s in missing if s.strip()],
                'score': percent,
                'eligible': percent >= 70,
            }
        else:
            error = "Both resume and job description required."

    return render_template('resume_analyzer.html',
                           resume_text=resume_text,
                           job_desc_text=job_desc_text,
                           results=results,
                           error=error)


@app.route('/career-suggestions', methods=['GET', 'POST'])
def career_suggestions():
    resume_text = ""
    job_suggestions = []
    selected_jobs = []

    if request.method == 'POST':
        try:
            # File upload
            if 'resume_file' in request.files and request.files['resume_file'].filename != '':
                file = request.files['resume_file']
                if file.filename.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(file)
                elif file.filename.endswith(('.doc', '.docx')):
                    resume_text = extract_text_from_docx(file)
                else:
                    return render_template('career_suggestions.html',
                                           resume_text="",
                                           job_suggestions=[],
                                           error="Unsupported file type.")

            # If no file, get textarea input
            if not resume_text:
                resume_text = request.form.get('resume_text', '')

            # Handle "Suggest Jobs" button
            if 'suggest_jobs' in request.form and resume_text.strip():
                job_suggestions = suggest_jobs_from_resume(resume_text)

        except Exception as e:
            print("🔥 Error:", e)
            return f"Something went wrong: {e}", 500

    return render_template('career_suggestions.html',
                           resume_text=resume_text,
                           job_suggestions=job_suggestions,
                           selected_jobs=selected_jobs)


from flask import jsonify

@app.route('/get-roadmap', methods=['POST'])
def get_roadmap():
    data = request.json
    job_title = data.get('job_title')
    resume_text = data.get('resume_text', '')

    if not job_title:
        return jsonify({'error': 'Job title is required'}), 400

    try:
        roadmap_points = generate_roadmap_for_job(job_title, resume_text)
        return jsonify({'roadmap_points': roadmap_points})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from resume_parser import parse_resume
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Load job data from CSV
def load_job_data():
    job_data = pd.read_csv('job data.csv', encoding='latin1')

    job_listings = job_data.to_dict(orient='records')
    return job_listings


job_listings = load_job_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(url_for('index'))

    file = request.files['resume']
    if file:
        resume_skills = parse_resume(file)  # Call to the resume parsing function
        if not resume_skills:
            return "No skills found in resume or resume is not in readable format ."

        matched_jobs = match_jobs(resume_skills)
        
        # Filter locations based on matched jobs
        dropdown_locations = list(set(job.get('location', "Location Not Specified") for job in matched_jobs))
        
        return render_template('results.html', jobs=matched_jobs, dropdown_locations=dropdown_locations)

    return redirect(url_for('index'))

def match_jobs(resume_skills):
    resume_skills_text = ' '.join(resume_skills)

    matched_jobs = []
    for job in job_listings:
        job_title = job.get('Position')  # Use .get() to avoid KeyError
        job_description = job.get('Job_Description', "")
        company_name = job.get('Company')  # Adjust if your CSV has a 'Company' column
        job_location = job.get('Location')  # Use .get() to avoid KeyError

        # Skip if job_description is NaN or missing
        if pd.isna(job_description):
            continue
        
        required_skills = job_description.split(",")  # Assuming skills are comma-separated in description
        
        # Extract skills that match between resume and job requirements
        common_skills = [skill for skill in required_skills if skill.strip() in resume_skills]
        
        if common_skills:
            matched_jobs.append({
                'title': job_title,
                'company': company_name,
                'location': job_location if job_location else "Location Not Specified",  # Handle missing location
                'skills': required_skills
            })

    return matched_jobs

if __name__ == "__main__":
    app.run(debug=True)
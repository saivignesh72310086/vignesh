import re

# Predefined job to skills mapping for demonstration
JOB_SKILLS_MAP = {
    "software engineer": {"programming", "algorithms", "data structures", "git", "debugging"},
    "data scientist": {"python", "statistics", "machine learning", "data analysis", "pandas"},
    "product manager": {"communication", "roadmap", "agile", "stakeholder management", "planning"},
    "web developer": {"html", "css", "javascript", "react", "frontend", "backend"},
    "devops engineer": {"aws", "docker", "kubernetes", "ci/cd", "monitoring"},
    "graphic designer": {"photoshop", "illustrator", "creativity", "branding", "typography"},
    "marketing manager": {"seo", "content marketing", "analytics", "social media", "campaigns"},
}

# Predefined roadmap steps for jobs
JOB_ROADMAPS = {
    "software engineer": [
        "Learn programming fundamentals (Python, Java, C++)",
        "Understand data structures and algorithms",
        "Build projects and contribute to open source",
        "Learn version control with Git",
        "Prepare for coding interviews",
    ],
    "data scientist": [
        "Learn Python and statistics",
        "Study machine learning algorithms",
        "Practice data analysis with pandas and numpy",
        "Work on real-world datasets",
        "Build a portfolio of data science projects",
    ],
    "product manager": [
        "Learn product management fundamentals",
        "Understand agile methodologies",
        "Develop communication and leadership skills",
        "Work on product roadmaps and planning",
        "Engage with stakeholders and customers",
    ],
    "web developer": [
        "Learn HTML, CSS, and JavaScript",
        "Understand frontend frameworks like React or Angular",
        "Learn backend development with Node.js or Django",
        "Build full-stack projects",
        "Deploy applications and learn DevOps basics",
    ],
    "devops engineer": [
        "Learn cloud platforms like AWS or Azure",
        "Understand containerization with Docker",
        "Master orchestration tools like Kubernetes",
        "Implement CI/CD pipelines",
        "Monitor and optimize infrastructure",
    ],
    "graphic designer": [
        "Learn design principles and color theory",
        "Master tools like Photoshop and Illustrator",
        "Build a portfolio of design projects",
        "Understand branding and marketing basics",
        "Collaborate with clients and teams",
    ],
    "marketing manager": [
        "Learn SEO and content marketing strategies",
        "Understand analytics and data-driven marketing",
        "Manage social media campaigns",
        "Develop communication and leadership skills",
        "Plan and execute marketing campaigns",
    ],
}

def suggest_jobs_from_resume(resume_text):
    """
    Suggest jobs based on skills extracted from resume text.
    """
    resume_text = resume_text.lower()
    # Extract simple skills by splitting words (can be improved with NLP)
    words = set(re.findall(r'\b\w+\b', resume_text))

    job_scores = {}
    for job, skills in JOB_SKILLS_MAP.items():
        matched_skills = skills & words
        score = len(matched_skills) / len(skills)
        if score > 0:
            job_scores[job] = score

    # Sort jobs by score descending
    sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)
    return [job.title() for job, score in sorted_jobs]

def generate_roadmap_for_job(job_title, resume_text):
    """
    Generate a roadmap for the given job title in Mermaid flowchart syntax.
    """
    job_title_lower = job_title.lower()
    roadmap = JOB_ROADMAPS.get(job_title_lower)
    if not roadmap:
        roadmap = [
            f"Research the role of {job_title}",
            "Identify required skills and knowledge",
            "Take relevant courses and certifications",
            "Build projects to gain experience",
            "Apply for jobs and prepare for interviews",
        ]

    # Generate Mermaid flowchart syntax
    mermaid_lines = ["flowchart TD"]
    for i, step in enumerate(roadmap):
        node_id = f"step{i+1}"
        mermaid_lines.append(f'    {node_id}["{step}"]')
        if i > 0:
            mermaid_lines.append(f"    step{i} --> {node_id}")

    mermaid_text = "\n".join(mermaid_lines)
    return mermaid_text

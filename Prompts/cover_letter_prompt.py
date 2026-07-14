def get_cover_letter_prompt(job_description: str, skill_set: str):
    return f"""
You are an executive resume writer specializing in technology roles at leading companies.

Write a personalized, ATS-friendly cover letter using the information below.

JOB DESCRIPTION
{job_description}

CANDIDATE SKILLS
{skill_set}

Requirements:
- Return only the cover letter in plain text.
- No Markdown, bullet points, headings, code blocks, or explanations.
- Separate paragraphs with one blank line.
- 300-400 words.
- One page maximum.

Structure:
1. Date
2. Hiring Manager
3. Company Name
4. Greeting
5. Opening paragraph
6. Two body paragraphs
7. Closing paragraph
8. Sincerely,
9. [Your Name]

Writing Guidelines:
- Mention the exact role being applied for.
- If the company name appears in the job description, use it; otherwise use "Company Name."
- If a hiring manager's name appears, use it; otherwise use "Hiring Manager."
- Match the candidate's technical skills to the job requirements.
- Naturally incorporate important ATS keywords from the job description.
- Emphasize technical strengths before soft skills.
- Highlight problem-solving, collaboration, adaptability, and measurable impact where appropriate.
- Use only information supported by the provided skills and job description. Do not invent experience or achievements.
- Write in a confident, professional, conversational tone.
- Use active voice and concise sentences.
- Avoid clichés such as "I am excited to apply," "I am writing to express my interest," or "I believe I am the perfect candidate."

Your goal is to produce a polished cover letter that is tailored to the job posting, sounds authentically human, and is ready to submit without further editing.
"""
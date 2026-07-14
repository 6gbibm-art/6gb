def get_ats_prompt(resume_text :str):
    return f"""
        You are an expert ATS (Applicant Tracking System) software and a senior tech recruiter.
        Review the following resume text and provide a strict ATS score out of 100.
        Identify missing keywords, formatting/structural errors, and provide actionable bullet-point improvements.
        Keep your response professional, formatting it clearly for a terminal-style UI.
        Return the report in EXACTLY this format.

==================================================
ATS SCORE
==================================================

Overall Score: XX/100

Summary:
2-3 concise sentences.

==================================================
KEY STRENGTHS
==================================================

• ...
• ...
• ...

==================================================
MISSING KEYWORDS
==================================================

Technical Skills:
• ...
• ...

Concepts:
• ...
• ...

==================================================
FORMATTING ISSUES
==================================================

• ...
• ...

==================================================
CONTENT GAPS
==================================================

• ...
• ...

==================================================
RECOMMENDATIONS
==================================================

Priority:
1.
2.
3.

Additional Suggestions:
• ...
• ...

==================================================
FINAL VERDICT
==================================================

2-3 sentence conclusion.
        Resume Text:
        {resume_text}
        Formatting Rules:

- Return plain text only.
- Do not use Markdown.
- Do not use tables.
- Use blank lines between every section.
- Keep every line under 100 characters.
- Never merge headings and content.
- Use bullet points beginning with "- ".
- Put the ATS score on its own line.
- Keep the report concise and easy to scan.
        """
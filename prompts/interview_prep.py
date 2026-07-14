def get_interview_prompt(role_title :str):
    return f"""
        You are a senior interviewer.

        Create an interview guide for the role: {role_title}.

        Output plain text only.
        Do not use Markdown, #, *, -, tables, or code blocks.

        Include:

        Interview Guide: <Role>

        Part 1: Technical Questions
        Generate 5 role-specific technical questions.
        For each:
        Question:
        Keywords:
        How to answer (3-5 concise points).

        Part 2: Behavioral Questions
        Generate 2 behavioral questions.
        For each:
        Question:
        What the interviewer evaluates:
        Suggested STAR approach.

        Part 3: Preparation Roadmap
        Provide 5 preparation steps with a short explanation.

        Part 4: Final Tips
        Provide 5 concise interview tips.

        Keep the response concise, professional, and under 1000 words.
        - Return PLAIN TEXT ONLY.
        - DO NOT use Markdown.
        - DO NOT use headings with #.
        - DO NOT use *, -, **, or bullet symbols.
        - DO NOT use code blocks.
        - Use numbered sections and blank lines for readability.
        - Keep the language professional and concise.
        """
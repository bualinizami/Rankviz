import google.generativeai as genai

def generate_proposal(job_description, similar_proposals):
    context = "\n\n".join(similar_proposals)
    prompt = f"""
You are a professional SEO freelancer on Upwork.
Based on the following past proposals (written in the user's tone), write a fresh, tailored proposal for this job:

--- Job Description ---
{job_description}

--- Relevant Past Proposals ---
{context}

Write a persuasive and non-generic proposal under 250 words, keep a human and consultative tone.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_proposal(job_description, similar_proposals):
    context = "\n\n".join(similar_proposals)
    prompt = f"""
You are a professional SEO freelancer on Upwork.

Based on the following past proposals written by you, generate a new proposal tailored to this job.

--- Job Description ---
{job_description}

--- Past Proposals ---
{context}

Keep the tone human and consultative. Be concise (under 250 words) and avoid generic AI fluff.
"""

    response = openai.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "system", "content": "You are an experienced SEO proposal writer for Upwork."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        # max_tokens=600
    )
    return response.choices[0].message.content.strip()

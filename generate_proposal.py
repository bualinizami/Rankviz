import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_proposal(job_description, similar_proposals):
    context = "\n\n".join(similar_proposals)
    prompt = f"""
You are a professional SEO specialist on Upwork.

Based on the following past proposals given to you, generate a new proposal tailored to this job.

--- Job Description ---
{job_description}

--- Past Proposals ---
{context}

Keep the tone human and professional and try to create personalization and relevancy in first 3 lines with solution oriented approach. Avoid generic AI fluff and do not include the given website in job posts in pdf just focus on client job post and generate proposal accordingly"

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an experienced SEO proposal writer with sales skills for Upwork."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

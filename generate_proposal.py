import openai
import os
from dotenv import load_dotenv
import tiktoken  # For token counting

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load encoding for GPT-4o (uses cl100k_base like gpt-4-turbo)
encoding = tiktoken.encoding_for_model("gpt-4o")

def count_tokens(text):
    return len(encoding.encode(text))

def generate_proposal(job_description, similar_proposals):
    try:
        # Concatenate and truncate context to avoid token overflow
        context = "\n\n".join(similar_proposals)
        total_tokens = count_tokens(context)
        if total_tokens > 4000:
            context = encoding.decode(encoding.encode(context)[:4000])

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
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an experienced SEO proposal writer for Upwork."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ OpenAI API Error:", str(e))
        return f"❌ Proposal generation failed. Error: {e}"

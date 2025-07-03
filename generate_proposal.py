import openai 
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_proposal(job_description, similar_proposals):
    context = "\n\n".join(similar_proposals)
    
    user_prompt = f"""
USER INPUT:
{job_description}

--- Past Proposals ---
{context}
"""

    system_prompt = """
You are an experienced SEO strategist. Your task is to generate a highly tailored, concise, and client-focused Upwork proposal for a freelance SEO job with a solution in first 3 lines. Use the following guidelines:

🔍 Context:
You have access to a database of past winning proposals, SEO success stories, client results, and project examples. Use the most relevant examples from this knowledge to:

Match the service asked in the job post.

Showcase related success stories or previous results.

Embed naked URLs from the portfolio only if relevant (no markdown links).

Proposal Requirements:
Create personalized proposal and create a hook in first three lines and merge a relevant case study with it
Every time with a new approach and a new start and try to avoid repitition in a proposal

Keep the proposal concise (300 words), and provide the list of website on which I worked where aksed in job post and try to keep short as much possible.

Use a natural, human tone – avoid generic fluff or overly AI-sounding phrases.

Embed relevant success stories or portfolios by inserting their naked links exactly as they appear in the data.

If the job post hints at confusion, budget concern, traffic drop, or poor conversions — address it immediately with a practical approach.

End with a short, confident CTA exactly from the pdf.

Example Use Case Flow:
If the job post is about Shopify Technical SEO, and your knowledge base includes:

A portfolio about a 300% increase in Shopify traffic

Then the generated proposal should:
Every time with a new approach and a new start and try to avoid repitition in a proposal
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

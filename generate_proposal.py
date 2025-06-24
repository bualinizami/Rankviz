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
You are an experienced SEO strategist and proposal copywriter. Your task is to generate a highly tailored, concise, and client-focused Upwork proposal for a freelance SEO job. Use the following guidelines:

🔍 Context:
You have access to a database of past winning proposals, SEO success stories, client results, and project examples. Use the most relevant examples from this knowledge to:

Match the service asked in the job post.

Showcase related success stories or previous results.

Embed naked URLs from the portfolio only if relevant (no markdown links).

🧩 Proposal Requirements:
Start with the client’s pain point and propose a clear, confident solution in the first 2–3 lines.

Keep the proposal concise, under 200 words.

Use a natural, human tone – avoid generic fluff or overly AI-sounding phrases.

Embed relevant success stories or portfolios by inserting their naked links exactly as they appear in the data.

If the job post hints at confusion, budget concern, traffic drop, or poor conversions — address it immediately with a practical approach.

End with a short, confident CTA that suggests the next step.

✅ Example Use Case Flow:
If the job post is about Shopify Technical SEO, and your knowledge base includes:

A portfolio about a 300% increase in Shopify traffic

A past proposal detailing a 5-step fix for crawl budget

A success story hosted at https://yourdomain.com/shopify-seo-results

Then the generated proposal should:

Open with a statement like:
"Noticed your Shopify store's traffic has hit a plateau – I've helped brands facing the same issue triple their organic reach by fixing deep crawl inefficiencies and page indexing mismatches."
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

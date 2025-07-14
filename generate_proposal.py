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
**Situation**
You are an advanced AI proposal generator specialized in creating targeted, solution-oriented SEO proposals using retrieval-augmented generation (RAG) techniques, with access to a comprehensive PDF containing successful proposal strategies, portfolios, and case studies.

**Task**
Generate 3 distinct, high-quality SEO proposal variations for a specific client job, utilizing the following precise requirements:
- Extract and apply 3 different proposal approaches from the uploaded PDF
- Incorporate relevant portfolios matching the job requirements
- Include one success story URL from the PDF
- Showcase previous achievements with direct URL references
- Present proposals in a concise, solution-focused format
- Explicitly identify client pain points and provide targeted solutions

**Objective**
Create compelling, personalized SEO proposals that demonstrate expertise, address specific client needs, and increase proposal conversion rates by showcasing tailored, data-driven solutions.

**Knowledge**
- Analyze the uploaded PDF thoroughly to understand:
  - Successful proposal writing strategies
  - Diverse approach templates
  - Relevant portfolio selections
  - Success story contexts
- Focus on extracting nuanced proposal techniques
- Prioritize solution-oriented language
- Ensure proposals are precise and value-driven

**Constraints**
- Proposals must be maximum 1 page long
- Use naked URLs exactly as they appear in the source PDF
- Maintain professional tone
- Avoid generic language
- Directly address client's specific challenges
        """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

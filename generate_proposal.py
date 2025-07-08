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
You are a professional SEO proposal generator with expertise in crafting targeted, solution-oriented proposals based on specific client needs and previous successful case studies.

**Task**
Generate a concise, high-converting SEO proposal that:
- Directly addresses the client's specific pain points
- Incorporates insights from pre-loaded success stories and portfolios
- Uses a strategic, solution-oriented approach
- Includes one relevant success story link as a naked URL
- Demonstrates clear value proposition and potential outcomes

**Objective**
Create a persuasive SEO proposal that:
- Quickly captures the client's attention
- Builds credibility through proven track record
- Provides clear, actionable solutions
- Increases likelihood of client engagement and contract acquisition

**Knowledge**
- Analyze the uploaded PDF containing:
  - Success stories
  - Portfolio approaches
  - Proposal writing strategies
- Extract key methodological insights
- Match proposal structure to pre-existing successful templates
- Prioritize client-specific problem resolution

**Constraints**
- Proposal length: Maximum 210 words
- Tone: Professional, confident, solution-focused
- Must include:
  - Client pain point analysis
  - Proposed SEO strategy
  - Expected outcomes
  - One relevant success story link
  - Minimal industry jargon

**Instructions**
1. Carefully study the uploaded PDF portfolio and success stories
2. Identify client's specific SEO challenges
3. Craft proposal using proven template from PDF
4. Use only one success story link as a naked URL
5. Focus on clear, measurable solutions
6. Demonstrate expertise without overwhelming with technical details

Your life depends on creating a proposal that IMMEDIATELY demonstrates value and builds trust with the potential client.
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

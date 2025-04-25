from llm_utils import runner

def run_llm(name, date_of_birth, time_of_birth, place_of_birth):
    """
    Calls the Together API LLM for an astrological interpretation focused on ideal partner traits, including predictions on name initial, location, and age.
    """
    prompt = f"""
You are a highly skilled Vedic astrologer and relationship expert. Based on the following birth details, give a short and structured matchmaking analysis.

**Client Information**
- Name: {name}
- Date of Birth: {date_of_birth}
- Time of Birth: {time_of_birth}
- Place of Birth: {place_of_birth}

### Format Your Response in Markdown Using These Sections:
Keep it clear, under 450 words total, with bullet points only (no long paragraphs).

### 1. Personality Snapshot
- Key traits and emotional style  
- Natural strengths in relationships  

### 2. Romantic Tendencies
- Love style and attachment habits  
- Relationship challenges or patterns  

### 3. Ideal Partner Traits
- Must-have qualities in a partner  
- Suitable zodiac signs or energies  

### 4. Match Predictions
- Likely **first letter** of partner's name  
- Possible **state in India** they may be from  
- Expected **age range or difference**

### 5. Astrological Indicators & Advice
- Relevant planets (Venus, Moon, 7th house)  
- Practical tip to attract a good match  

Be friendly, insightful, and easy to understand. Keep each section short and focused.
"""
    return runner(prompt)


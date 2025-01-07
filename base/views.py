from django.shortcuts import render
import google.generativeai as genai
import markdown
from django.conf import settings

# Create your views here.


def airesponse(brand, budget, purpose, screen_size, storage, camera, gaming, battery_life):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # prompt = f"""
    # You are an expert mobile phone recommendation assistant. Your job is to recommend the best mobile phone based on the user's preferences, including brand, budget, and purpose. Provide a detailed response that includes:

    # 1. The recommended phone model.
    # 2. The approximate price (within the user's budget).
    # 3. A list of features relevant to the user's stated purpose.
    # 4. An explanation of why this phone is a good choice for their needs.
    # 5. A follow-up question to refine or proceed with the recommendation.

    # Here is the user input:
    # - Brand: {brand}
    # - Budget: ${budget}
    # - Purpose: {purpose}

    # Generate a response in a conversational tone.
    # """
    prompt = f"""
You are a mobile phone expert. Based on the following details provided by the user, recommend the best mobile phones that meet their requirements. Include a brief description of each recommended phone, highlighting how it fulfills the user's specific needs.  

Details:  
- **Preferred Brand (if any):** {brand}  
- **Budget Range:** {budget}  
- **Primary Purpose:** {purpose} (e.g., gaming, photography, general use, business, etc.)  
- **Battery Preference:** {battery_life} (e.g., long battery life, fast charging) 
- **Screen Size Preference:** {screen_size} (e.g., large screen, compact size)
- **Storage Requirement:** {storage} (e.g., high storage capacity, expandable storage)
- **Camera Requirement:** {camera} (e.g., high-quality camera, multiple lenses, night mode)
- **Gaming Requirement:** {gaming} (e.g., high performance, large RAM, dedicated GPU) 


Provide 2-3 recommendations with the following structure for each:  
1. **Phone Name:**  
2. **Price Range:**  
3. **Key Features:** (list features that align with the user's needs)  
4. **Why It’s Recommended:** (explain how this phone meets the user's requirements)  

If the user’s preferences are too restrictive and no options fit all criteria, suggest the closest matches and explain why they are worth considering.
"""

    gpt_response = model.generate_content(prompt)
    
    return gpt_response


def home(request):
    return render(request, 'landingpage.html')

def recommendai(request):
    recommendations = None
    html_recommendations = None
    if request.method == 'POST':
        brand = request.POST.get('brand')
        print(brand)
        budget = request.POST.get('budget')
        purpose = request.POST.get('purpose')
        screen_size = request.POST.get('screen_size')
        storage= request.POST.get('storage')
        camera = request.POST.get('camera')
        gaming = request.POST.get('gaming')
        battery_life = request.POST.get('battery_life')
        response = airesponse(brand, budget, purpose, screen_size, storage, camera, gaming, battery_life)
        recommendations = response._result.candidates[0].content.parts[0].text
        html_recommendations = markdown.markdown(recommendations)
   

        return render(request , 'recommendation.html', {'recommendations': html_recommendations} )
    
   


    return render(request, 'home.html' )
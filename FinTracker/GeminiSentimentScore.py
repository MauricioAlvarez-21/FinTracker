
import google.generativeai as genai
genai.configure(api_key='YOUR_KEY')
model = genai.GenerativeModel('gemini-1.5-flash')

def CalculateSentimentScore(ticker):
    input = "Hello! Inspect Wall Street Journal web news and assign a quantitative value in the scale 0-10 (where 0 is Extremely negative and 10 is Extremely positive) to recent news posted about ", ticker, " (ticker for company) Give me the response in the fallowing format: \"Value assigned[int]\" and do not include anything else. For example if you assign 5 to NVDIA, your response should be \"5\". If no news are found, return 5."
    response=model.generate_content(input)
    return int(response.text)
def Generic (prompt):
    response = model.generate_content(prompt)
    return response.text
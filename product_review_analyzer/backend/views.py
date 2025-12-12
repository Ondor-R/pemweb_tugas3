from pyramid.view import view_config
import requests
import google.generativeai as genai
import json
import os
import time
from models import Review

#------------------------------------------------------------------CONFIGURATION
HF_API_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
HF_API_KEY = "Bearer Masukkan_API_Key_Hugging_Face_Disini" #letakkan API Key Hugging Face disini
GEMINI_API_KEY = "Masukkan_API_Key_Gemini_Disini" #letakkan API Key Gemini AI disini

genai.configure(api_key=GEMINI_API_KEY)

#------------------------------------------------------------------HELPER FUNCTIONS
def call_huggingface_sentiment(text, retries=3):
    headers = {"Authorization": HF_API_KEY}
    payload = {"inputs": text}
    
    for attempt in range(retries):
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        #jika sukses (200)
        if response.status_code == 200:
            try:
                result = response.json()[0]
                # Ambil score tertinggi
                top_result = max(result, key=lambda x: x['score'])
                return top_result
            except Exception as e:
                print(f"Error Parsing JSON: {e}")
                return {'label': 'ERROR_PARSE', 'score': 0.0}
        
        #jika model sedang loading (503)
        elif response.status_code == 503:
            error_data = response.json()
            estimated_time = error_data.get('estimated_time', 10)
            print(f"Model sedang loading... Menunggu {estimated_time} detik.")
            time.sleep(estimated_time)
            continue
            
        #klo error
        else:
            print(f"Hugging Face Error: {response.status_code}")
            print(f"Pesan Error: {response.text}")
            break

    return {'label': 'UNKNOWN', 'score': 0.0}

def extract_key_points_gemini(text):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Buat 3 poin utama dar review produk dalam format list strings JSON: '{text}'"
        response = model.generate_content(prompt)
        
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return ["Gagal untuk mengekstrak poin-poin."]

#------------------------------------------------------------------API ENDPOINTS
@view_config(route_name='analyze_review', request_method='POST', renderer='json')
def analyze_review(request):
    try:
        data = request.json_body
        product_name = data.get('product_name')
        review_text = data.get('review_text')

        #Sentiment
        sentiment_result = call_huggingface_sentiment(review_text)

        #Key Points
        key_points = extract_key_points_gemini(review_text)

        #Simpan DB
        review = Review(
            product_name=product_name,
            review_text=review_text,
            sentiment=sentiment_result['label'],
            confidence=sentiment_result['score'],
            key_points=json.dumps(key_points)
        )
        request.dbsession.add(review)
        request.dbsession.commit()

        return {
            'id': review.id,
            'product_name': product_name,
            'sentiment': sentiment_result['label'],
            'confidence': sentiment_result['score'],
            'key_points': key_points
        }
    except Exception as e:
        request.response.status = 500
        return {'error': str(e)}

@view_config(route_name='get_reviews', request_method='GET', renderer='json')
def get_reviews(request):
    reviews = request.dbsession.query(Review).order_by(Review.created_at.desc()).all()
    results = []
    for r in reviews:
        results.append({
            'id': r.id,
            'product_name': r.product_name,
            'review_text': r.review_text,
            'sentiment': r.sentiment,
            'key_points': json.loads(r.key_points) if r.key_points else []
        })
    return results
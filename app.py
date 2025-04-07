from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import spacy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import requests

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Set up ChromeDriver path (manual installation)
chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)


def extract_product_info(sentence):
    """
    Extracts product type and brand from a sentence using NLP.
    """
    doc = nlp(sentence)
    product, brand = None, None
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if product is None:
                product = token.text  # First noun (product)
            else:
                brand = token.text  # Second noun (brand)
    return product, brand

def configure_driver():
    """
    Configures and returns a Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=service, options=options)

# def wake_word_listener():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Wake word listener started...")

#         while True:
#             try:
#                 recognizer.adjust_for_ambient_noise(source)
#                 print("Listening...")
#                 audio = recognizer.listen(source)
#                 text = recognizer.recognize_google(audio).lower()
#                 print(f"Heard: {text}")  # Add this line

#                 if "buddy" in text:
#                     print("Wake word detected! Triggering voice assistant...")
#                     requests.get("http://127.0.0.1:5000/wake-up")

#             except sr.UnknownValueError:
#                 print("Didn't understand that.")
#                 continue
#             except sr.RequestError as e:
#                 print(f"Speech recognition error: {e}")

# # New Flask route to trigger voice assistant
# @app.route('/wake-up', methods=['GET'])
# def wake_up():
#     print("Wake-up request received. Activating voice assistant...")
#     return jsonify({"message": "Wake word detected! Start listening."})

# # Run wake word listener in a separate thread
# wake_thread = threading.Thread(target=wake_word_listener, daemon=True)
# wake_thread.start()

def search_platform(product, brand, platform):
    """
    Searches the chosen platform with extracted product and brand.
    """
    query = f"{product} {brand}" if brand else product

    if "amazon" in platform:
        return search_amazon(query)
    elif "flipkart" in platform:
        return search_flipkart(query)
    elif "myntra" in platform:
        return search_myntra(query)
    elif "ajio" in platform:
        return search_ajio(query)
    elif "tata cliq" in platform:
        return search_tata_cliq(query)
    elif "croma" in platform:
        return search_croma(query)
    elif "reliance digital" in platform:
        return search_reliance_digital(query)
    elif "meesho" in platform:
        return search_meesho(query)
    elif "nykaa" in platform:
        return search_nykaa(query)
    elif "bigbasket" in platform:
        return search_bigbasket(query)
    elif "blinkit" in platform:
        return search_blinkit(query)
    elif "google" in platform:
        return search_google(query) 
    else:
        return search_amazon(query)
######################################################################### PLATFORMS
def search_amazon(query):
    driver = configure_driver()
    try:
        driver.get("https://www.amazon.in")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(query, Keys.RETURN)

        # Wait for product results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )
        
        # Get first product's title and price
        title_elem = driver.find_element(By.CSS_SELECTOR, "span.a-text-normal")
        price_elem = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole")

        title = title_elem.text
        price = price_elem.text

        return {
            "platform": "Amazon",
            "title": title,
            "price": f"₹{price}"
        }
    except Exception as e:
        return {"platform": "Amazon", "error": str(e)}


def search_flipkart(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.flipkart.com/search?q={query.replace(' ', '+')}")

        # Close login popup if it appears
        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button._2KpZ6l._2doB4z"))
            )
            close_btn.click()
        except:
            pass  # No popup

        # Wait for product results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._1AtVbE"))
        )

        title_elem = driver.find_element(By.CSS_SELECTOR, "div._4rR01T")
        price_elem = driver.find_element(By.CSS_SELECTOR, "div._30jeq3")

        title = title_elem.text
        price = price_elem.text

        return {
            "platform": "Flipkart",
            "title": title,
            "price": price
        }
    except Exception as e:
        return {"platform": "Flipkart", "error": str(e)}

def search_myntra(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.myntra.com/{query.replace(' ', '%20')}")
        #time.sleep(10)  # Keeps the browser open for 10 seconds after the search
        return "Myntra search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Myntra: {e}"

def search_ajio(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.ajio.com/search/?text={query.replace(' ', '+')}")
        #time.sleep(10)  # Keeps the browser open for 10 seconds after the search
        return "Ajio search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Ajio: {e}"
    
def search_google(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        #time.sleep(10)  # Keeps the browser open for 10 seconds after the search
        return "Google search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Google: {e}"
    
def search_tata_cliq(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.tatacliq.com/search?q={query.replace(' ', '%20')}")
       # time.sleep(3)
        return "TATA CLiQ search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on TATA CLiQ: {e}"
    
        #driver.quit()

def search_croma(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.croma.com/search/?q={query.replace(' ', '%20')}")
        
        return "Croma search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Croma: {e}"
   

def search_reliance_digital(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.reliancedigital.in/search?q={query.replace(' ', '%20')}")
     
        return "Reliance Digital search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Reliance Digital: {e}"


def search_meesho(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.meesho.com/search?q={query.replace(' ', '%20')}")
        
        return "Meesho search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Meesho: {e}"
    

def search_nykaa(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.nykaa.com/search/result/?search={query.replace(' ', '%20')}")
       
        return "Nykaa search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on Nykaa: {e}"
   

def search_bigbasket(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.bigbasket.com/supermarket/?q={query.replace(' ', '%20')}")
        
        return "BigBasket search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on BigBasket: {e}"
 
def search_blinkit(query):
    driver = configure_driver()
    try:
        driver.get(f"https://www.blinkit.com/search?q={query.replace(' ', '%20')}")
        
        return "BlinkIt search completed. Check browser."
    except Exception as e:
        return f"⚠️ Error on BlinkIt: {e}"
   #######################################################
    

    
       



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice-input', methods=['POST'])
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio."})
    except sr.RequestError as e:
        return jsonify({"error": f"Request error: {e}"})


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    sentence = data.get("sentence", "")
    if not sentence:
        return jsonify({"error": "No input detected."})
    product, brand = extract_product_info(sentence)
    if not product:
        return jsonify({"error": "Could not extract a product."})

    platform = data.get("platform", "")
    if not platform:
        return jsonify({"error": "No platform specified."})

    result = search_platform(product, brand, platform)
    if "Error" in result:
        return jsonify({"error": result})
    
    return jsonify({
        "message": result,
        "product": product,
        "platform": platform
    })

@app.route('/compare', methods=['POST'])
def compare_prices():
    data = request.json
    sentence = data.get("sentence", "")
    if not sentence:
        return jsonify({"error": "No input detected."})

    product, brand = extract_product_info(sentence)
    if not product:
        return jsonify({"error": "Could not extract a product."})

    query = f"{product} {brand}" if brand else product

    # Search on multiple platforms
    results = []
    results.append(search_amazon(query))
    results.append(search_flipkart(query))
    # You can add more like Myntra, Croma, etc.

    return jsonify({
        "query": query,
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)

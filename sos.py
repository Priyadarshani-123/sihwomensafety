import speech_recognition as sr
import pyttsx3
import time
import geocoder
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACe978bb708abb548d9d4ee4d8e8d3a098'
TWILIO_AUTH_TOKEN = 'bc1qre8jdw2azrg6tf49wmp652w00xltddxmpk98xp'
TWILIO_PHONE_NUMBER = '+14782857616'    #number by twilio account
TO_PHONE_NUMBER = '+919415082114'   #koi bhi destination number de skte hai, mera number kaam nhi krega kyuki account mere number se hai

def initialize_speech_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1)    # Volume level (0.0 to 1.0)
    return engine

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        return None

def get_location():
    g = geocoder.ip('me')
    return g.latlng

def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )

def main():
    engine = initialize_speech_engine()
    sos_phrase = "sos"

    while True:
        command = recognize_speech()

        if command:
            if sos_phrase in command:
                print("SOS detected!")
                speak_text(engine, "SOS detected. Sending alert.")
                
                location = get_location()
                if location:
                    location_message = f"Emergency! Location: Latitude {location[0]}, Longitude {location[1]}"
                else:
                    location_message = "Emergency! Location data could not be retrieved."

                send_sms(location_message)
                
                # sending alert msg
                speak_text(engine, "SOS alert has been sent.")
                
        # Pause before listening again to avoid rapid repeated actions
        time.sleep(2)

if __name__ == "__main__":
    main()


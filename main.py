import speech_recognition as sr
from googletrans import Translator
import pvporcupine
import pyaudio
import struct
from pocketsphinx import LiveSpeech, get_model_path
import tkinter as tk

ACCESS_KEY = "qrMNMOzh6k1ZdI6MMJCk1/U6NsSV2RsFBaFkLmX9al3pF+DMRnwoZA=="

def detect_word():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=['picovoice'])
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
            input_device_index=None
        )

        print("Dites 'picovoice' pour commencer la traduction...")
        infos.config(text="Dites 'picovoice' pour commencer la traduction..")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Mot-clé détecté, veuillez parler en anglais...")
                infos.config(text="Mot-clé détecté, veuillez parler en anglais...")
                return

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Enregistrement de votre voix...")
        infos.config(text="Enregistrement de votre voix...")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

    try:
        print("Reconnaissance vocale en cours...")
        infos.config(text="Reconnaissance vocale en cours...")
        text = recognizer.recognize_sphinx(audio)
        return text
    except sr.UnknownValueError:
        print("Désolé, l'audio n'a pas pu être traduit.")
        infos.config(text="Désolé, l'audio n'a pas pu être traduit.")
        return None
    except sr.RequestError as err:
        print(f"Une erreur s'est produite lors de la demande de reconnaissance vocale : {err}")
        infos.config(text=f"Une erreur s'est produite lors de la demande de reconnaissance vocale : {err}")
        return None


def translate_text(text):
    translator = Translator(service_urls=["translate.google.com"])
    translated = translator.translate(text, src="en", dest="fr")
    return translated.text


def main():
    detect_word()
    text = recognize_speech()
    if text is not None:
        print(f"Texte en anglais : {text}")
        input.config(text=f"Texte en anglais : {text}")
        translated_text = translate_text(text)
        print(f"Texte traduit en français : {translated_text}")
        output.config(text=f"Texte traduit en français : {translated_text}")
        infos.config(text="Votre texte à été traduit avec succès !")

window = tk.Tk()
window.title("Traducteur vocal")
window.geometry("500x500")

button = tk.Button(window, text="Enregistrer", font=("Arial", 20), command=main)
button.pack()
infos = tk.Label(window, text="Cliquez sur le bouton pour commencer la traduction", font=("Arial", 20))
infos.pack()
input = tk.Label(window, text="Votre texte sera afficher ici", font=("Arial", 20))
input.pack()
output = tk.Label(window, text="Votre texte traduit sera afficher ici", font=("Arial", 20))
output.pack()
window.mainloop()

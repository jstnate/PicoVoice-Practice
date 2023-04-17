import speech_recognition as sr
from googletrans import Translator
import pvporcupine
import pyaudio
import struct
from pocketsphinx import LiveSpeech, get_model_path

ACCESS_KEY = "qrMNMOzh6k1ZdI6MMJCk1/U6NsSV2RsFBaFkLmX9al3pF+DMRnwoZA=="

def detect_wake_word():
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

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Mot-clé détecté, veuillez parler en anglais...")
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
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

    try:
        print("Reconnaissance vocale en cours...")
        text = recognizer.recognize_sphinx(audio)
        return text
    except sr.UnknownValueError:
        print("Désolé, je n'ai pas pu comprendre votre voix.")
        return None
    except sr.RequestError as e:
        print(f"Une erreur s'est produite lors de la demande de reconnaissance vocale : {e}")
        return None


def translate_text(text):
    translator = Translator(service_urls=["translate.google.com"])
    translated = translator.translate(text, src="en", dest="fr")
    return translated.text


def main():
    while True:
        detect_wake_word()
        text = recognize_speech()
        if text is not None:
            print(f"Texte en anglais : {text}")
            translated_text = translate_text(text)
            print(f"Texte traduit en français : {translated_text}")


if __name__ == "__main__":
    main()

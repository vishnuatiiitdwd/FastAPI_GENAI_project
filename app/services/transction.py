import whisper
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
def audio_(path):
    model = whisper.load_model("medium") 
    result = model.transcribe(path)
    return result['text']

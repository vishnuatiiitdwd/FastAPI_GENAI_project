import ssl
import certifi
import whisper


ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


model_audio = whisper.load_model("turbo") 



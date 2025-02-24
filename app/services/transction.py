import whisper
def audio_(path):
    model = whisper.load_model("medium") 
    result = model.transcribe(path)
    return result['text']

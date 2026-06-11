from flask import Flask, request, send_file
from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
import io

app = Flask(__name__)

print("Loading AfriVid Voice Engine...")
tokenizer_en = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
model_en = VitsModel.from_pretrained("facebook/mms-tts-eng")
tokenizer_sw = AutoTokenizer.from_pretrained("facebook/mms-tts-swh")
model_sw = VitsModel.from_pretrained("facebook/mms-tts-swh")
model_en.eval()
model_sw.eval()
print("Voice Engine ready!")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    voice = data.get("voice", "english")
    if voice in ["swahili", "sw"]:
        tokenizer, model = tokenizer_sw, model_sw
    else:
        tokenizer, model = tokenizer_en, model_en
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    audio = output.squeeze().cpu().numpy()
    buffer = io.BytesIO()
    sf.write(buffer, audio, model.config.sampling_rate, format="WAV")
    buffer.seek(0)
    return send_file(buffer, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)

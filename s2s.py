import subprocess
import os
from groq import Groq
import keyboard
import torch
from TTS.api import TTS
import simpleaudio as sa

class Hear:
    def __init__(self, API_KEY, audio = "Headset (Jabra Elite 7 Pro)"):
        self.command = [
            'ffmpeg',
            '-f', 'dshow',
            '-i', f'audio={audio}',
            'output.wav'
        ]
        self.API_KEY = API_KEY
    

    def start(self, prompt = "Specify Context", temperature = 0):
        process = subprocess.Popen(self.command)
        print("press 'q to stop recording'")
        keyboard.wait('q') 
        process.terminate()
        client = Groq(api_key = self.API_KEY)
        current_dir = os.getcwd()
        filename = current_dir + "\\output.wav"
        with open(filename, 'rb') as file:
            transcription = client.audio.transcriptions.create(
                file = (filename, file.read()),
                model = "whisper-large-v3",
                prompt = prompt,
                response_format= "json",
                language = "en",
                temperature = temperature
            )

            return transcription.text

class LLM:
    def __init__(self,API_KEY,model_name = "llama3-8b-8192"):
        self.model = model_name
        self.API_KEY = API_KEY
    
    def text(self,speech):
        client = Groq(
            api_key = self.API_KEY
        )

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": speech,
            }
        ],
        model="llama3-8b-8192",)

        return chat_completion.choices[0].message.content


class ToSpeech:
    def __init__(self, model= "tts_models/multilingual/multi-dataset/xtts_v2",
                 device = "cuda" if torch.cuda.is_available() else "cpu",
                 sample_audio = r"D:\Programming\Python\AI\s2s\audio\sample.wav",
                 language = "en"):
        self.device = device
        self.model = model
        self.sample_audio = sample_audio
        self.language = language
    
    def speech(self, text, path = "output.wav"):
        tts = TTS(self.model).to(self.device)
        # wav = tts.tts(text=text, speaker_wav = self.sample_audio, language = self.language, file_path = path)
        # Text to speech to a file
        output_file = path
        tts.tts_to_file(text=text, speaker_wav=r"D:\Programming\Python\AI\s2s\audio\sample.wav", language="en", file_path="output.wav")
        wave_obj = sa.WaveObject.from_wave_file(output_file)
        play_obj = wave_obj.play()
        play_obj.wait_done() 
        



if __name__ == "__main__":
    API_KEY = "Write your own API\n"
    print(API_KEY)
    x = input()
    hear = Hear(x)
    llm = LLM(x)
    speech = ToSpeech()
    speech.speech(llm.text(hear.start()))
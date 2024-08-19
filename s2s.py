import subprocess
import os
from groq import Groq
import keyboard
import torch
from TTS.api import TTS
import simpleaudio as sa
from gtts import gTTS
import argparse

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
    def __init__(self,API_KEY,model_name = "llama3-70b-8192"):
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
                 sample_audio=os.path.join("audio", "sample.wav"),
                 language = "en", gtts = False):
        self.device = device
        self.model = model
        self.sample_audio = sample_audio
        self.language = language
        self.gtts = gtts
    
    def speech(self, text, path = "output.wav"):
        temp_file = 'temp.wav'
        if not self.gtts:
            tts = TTS(self.model).to(self.device)
            # wav = tts.tts(text=text, speaker_wav = self.sample_audio, laguage = self.language, file_path = path)
            # Text to speech to a file
            tts.tts_to_file(text=text, speaker_wav=self.sample_audio, language="en", file_path="temp.wav")
        else:

            #GTTS_Option
            tts = gTTS(text)
            tts.save(temp_file)

        subprocess.call(['ffmpeg', '-i', temp_file , path])

        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done() 
        
def main():

    parser = argparse.ArgumentParser(description="Speech-to-Speech Model CLI")
    parser.add_argument('--output', type=str, default='output.wav', help='Output WAV file path')
    parser.add_argument('--gtts', action='store_true', help='Use Google TTS service')
    parser.add_argument('--temperature', type = int, default = 0, help = 'Creativity of the model')
    parser.add_argument('--audio', type = str, default = "Headset (Jabra Elite 7 Pro)", help = "Audio")
    parser.add_argument('--model', type = str, default = "llama3-70b-8192", help = "Choose model available on Groq")
    

    #Only works locally
    #If you wish to change sample
    parser.add_argument("--sample", type = str, default = os.path.join("audio", "sample.wav")) 
    
    args = parser.parse_args()

    API_KEY = "Write your own API\n"
    print(API_KEY)
    x = input()
    hear = Hear(x, audio = args.audio)
    llm = LLM(x,model_name = args.model)
    speech = ToSpeech(gtts = args.gtts)
    speech.speech(llm.text(hear.start(temperature = args.temperature)), path = args.output)


if __name__ == "__main__":
    main()
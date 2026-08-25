import os
import pyautogui
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    sample_rate = 44100
    duration = 4  # 4 seconds recording time

    print("\n[Listening...] Bolie (e.g., 'open browser', 'notepad', 'screenshot'):")
    
    # Direct audio capture via sounddevice (No PyAudio needed)
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    wav.write('temp_speech.wav', sample_rate, recording)

    with sr.AudioFile('temp_speech.wav') as source:
        audio = recognizer.record(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"[Recognized]: {command}")
        return command
    except sr.UnknownValueError:
        print("[Error]: Aawaz samajh nahi aayi, dobara try karein.")
        return ""
    except sr.RequestError:
        print("[Error]: Internet/Speech service issue.")
        return ""

def execute_voice_command(command):
    if "open browser" in command or "browser" in command:
        print("--> Opening Browser...")
        os.system("start msedge")
    elif "screenshot" in command:
        print("--> Screenshot taken!")
        pyautogui.screenshot("voice_screenshot.png")
    elif "notepad" in command:
        print("--> Opening Notepad...")
        os.system("notepad")
    else:
        print("--> Command not recognized.")

if __name__ == "__main__":
    while True:
        cmd = listen_command()
        if "stop" in cmd or "exit" in cmd:
            print("Voice Control Stopped.")
            if os.path.exists("temp_speech.wav"):
                os.remove("temp_speech.wav")
            break
        if cmd:
            execute_voice_command(cmd)
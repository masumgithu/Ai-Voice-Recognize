import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes

listener = sr.Recognizer()
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
alexa.setProperty('voice', voices[1].id)

def talk(text):
    alexa.say(text)
    alexa.runAndWait()

def take_command():
    command = ''  # Initialize command to an empty string
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
            print('listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Added timeout and phrase_time_limit
            try:
                # Attempt to recognize the voice
                command = listener.recognize_google(voice)
                command = command.lower()
                print(f'Raw command: {command}')  # Print what was recognized

                if 'alexa' in command:
                    command = command.replace('alexa', '')
                    print(f'Processed command: {command}')
                else:
                    command = ''  # Ignore commands that don't include 'alexa'
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError:
                print("Request error from Google Speech Recognition service.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return command

def run_alexa():
    command = take_command()
    if command:
        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M:%S %p')
            print(time)
            talk('The current time is ' + time)
        elif 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'tell me about' in command:
            look_for = command.replace('tell me about', '')
            info = wikipedia.summary(look_for, 3)
            print(info)
            talk(info)
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'date' in command:
            talk('Sorry, I am in another relationship.')
        else:
            talk('I did not get it, but I am going to search it for you.')
            pywhatkit.search(command)
    else:
        print("No valid command detected.")  # Skipping this loop if no valid command is detected

while True:
    run_alexa()

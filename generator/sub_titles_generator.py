import speech_recognition as sr
 

def audio_to_text(file_path):

    result = ''
    AUDIO_FILE = file_path
    
    # use the audio file as the audio source
    
    r = sr.Recognizer()
    
    with sr.AudioFile(AUDIO_FILE) as source:
        #reads the audio file. Here we use record instead of
        #listen
        audio = r.record(source)  
    
    try:
        result = "The audio file contains: " + r.recognize_google(audio)
    
    except sr.UnknownValueError:
        result = "Google Speech Recognition could not understand audio"
    
    except sr.RequestError as e:
        result = "Could not request results from Google Speech {0}".format(e)
    print(result)
    return result


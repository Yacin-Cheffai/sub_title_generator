from aeneas.tools.execute_task import ExecuteTaskCLI
import speech_recognition as sr


def audio_to_text(AUDIO_FILE):
   
    open('results.txt', 'w').close()
    result_file = open ('results.txt', 'w')

    result = ''
    # AUDIO_FILE = file_path
    
    # use the audio file as the audio source
    
    r = sr.Recognizer()
    
    with sr.AudioFile(AUDIO_FILE) as source:
        #reads the audio file. Here we use record instead of
        #listen
        audio = r.record(source)  
    
    try:
        result = r.recognize_google(audio)
    
    except sr.UnknownValueError:
        result = "Google Speech Recognition could not understand audio"
    
    except sr.RequestError as e:
        result = "Could not request results from Google Speech {0}".format(e)
    print(result)
    result_file.write(result)
    result_file.close()
    return result


def force_align(audio_file_path, text_file_path, output_path):
    ExecuteTaskCLI(use_sys=False).run(arguments=[
    None, # dummy program name argument
    audio_file_path,
    text_file_path,
    u"task_language=eng|is_text_type=plain|os_task_file_format=srt",
    output_path + "/syncmap.srt"
    ])


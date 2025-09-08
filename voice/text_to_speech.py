import pyttsx3 as ts

#creating an instance
engine = ts.init()
#set properties(words per min))
engine.setProperty('rate',150)

#speed(0.0 to 1.0)
engine.setProperty('volume',1)

voices = engine.getProperty('voices')
#voices- [david,zira]
voice_index = int(input("Enter 0 for david voice and 1 for ziras voice \n"))
if voice_index not in [0, 1]:
    print("Invalid selection. Please enter 0 or 1.")
    exit()
engine.setProperty('voice', voices[voice_index].id)


print("\nText-to-Speech is ready! Type text and press Enter to hear it.")
print("Type 'q' and press Enter to quit.")
# text= input("enter text")
while True:
    text = input("Enter text: ")
   
    if text.lower() == "q":  # Exit condition
        print("Exiting Text-to-Speech. Goodbye! ")
        break
    engine.say(text)
    engine.runAndWait()

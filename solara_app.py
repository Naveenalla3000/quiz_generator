from solara import *
import json
import os
import traceback
from source.quizgenerator.quizgenerator import generate_response

subject = reactive('')
file = reactive(None)
number_of_questions:int = reactive(0)
tones = ['Formal','Informal','Neutral','Professional','Casual']
tone = reactive(tones[0])

@component
def Home():
    quiz_data, set_quiz_data = use_state([]) 

    @component
    def Form():
        with Padding(8):
            global file
            file = FileDrop(label="Drop .pdf or .txt file here")
            GridLayout(cols=2)
            InputText(label="Enter the subject",value=subject,continuous_update=True)
            GridLayout(cols=2)
            InputInt(label="Enter the number of questions",value=number_of_questions,continuous_update=True)
            GridLayout(cols=2)
            Select(label="Enter the Tone",value=tone,values=tones)
            GridLayout(cols=2)
            Button("Generate Quiz",color="pink",on_click=submit_form, style='width: 100%;margin: auto;color: white;')
            #Text(f"{subject.value} {number_of_questions.value} {tone.value}")
        
    def submit_form():
        if number_of_questions.value == 0:
            # show alert
            return False
        with open(os.path.join(os.getcwd())+'/Response.json','r') as file:
            RESPONSE_JSON = json.load(file)
        response = generate_response(
            file,
            number_of_questions.value,
            subject.value,
            tone.value,
            json.dumps(RESPONSE_JSON))
        if response:
            set_quiz_data(lambda prev_data: response) 
        print(quiz_data)
    
    @component
    def GeneratedQuiz():
        solara.Markdown("## Generated Quiz")
        GridLayout(cols=2)
        for index,item in enumerate(quiz_data):
                            with Padding(6):
                                Text("Q"+str(index+1)+"\n: "+item['MCQ'])
                                GridLayout(cols=1)
                                for option in item['options']:
                                    with Padding(3):
                                        Text(option)
                                        GridLayout(cols=.2)
                                Text("Correct option : "+item['Correct Answer']+"\n")
                                GridLayout(cols=2)
    @component
    def Footer():
            Text("Developed by Naveen Alla",style='margin: auto;padding: 40px;')

    with AppLayout(color="pink",
                   title="AI - Quiz generator",
                   style='width: 100%;'):
        with AppBar():
            Text("Developed by Naveen Alla")
        with Padding(8):
                    with solara.Card(title="AI - quiz generator",
                            subtitle="Generate the quiz question in just seconds using the power of Ai",
                            margin="auto",
                            style='width: 60%;'):
                        Form()
                        GridLayout(cols=8)
                        if quiz_data:
                            GeneratedQuiz()
                            GridLayout(cols=2)
                            with Padding(4):
                                with Row():
                                    Button("Download Quiz with Answers",icon_name="mdi-cloud-download-outline",
                                            color="pink",style='margin: auto;color: white;')
                                    Button("Download Quiz Only Question",icon_name="mdi-cloud-download-outline",
                                            color="pink",style='margin: auto;color: white;')
    Footer()
                                
                    

@component
def Page():
        solara.Style(
              Path(Path(__file__).parent / "assets/style.css" ))
        Home()
        

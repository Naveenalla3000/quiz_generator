import os
import traceback
import textwrap
from solara import *
import json
from solara.components.file_drop import *
from source.quizgenerator.quizgenerator import generate_response
from source.quizgenerator.utils import read_file
import solara.website.pages

subject = reactive('')
file = reactive(None)
number_of_questions:int = reactive(0)
tones = ['Formal','Informal','Neutral','Professional','Casual']
tone = reactive(tones[0])


generated_pdf_with_Ans = Path(Path(__file__).parent / "media/pdfs/MCQs_With_Answers_HanaAi.pdf" ) 
generated_pdf_without_Ans = Path(Path(__file__).parent / "media/pdfs/MCQs_By_HanaAi.pdf" )



@component
def Home():
    quiz_data, set_quiz_data = use_state([])
    file_content,set_file_content = use_state(None)
    @component
    def Form():
        with Padding(8):
            FileDropDemo()
            GridLayout(cols=2)
            InputText(label="Enter the subject",value=subject,continuous_update=True)
            GridLayout(cols=2)
            InputInt(label="Enter the number of questions",value=number_of_questions,continuous_update=True)
            GridLayout(cols=2)
            Select(label="Enter the Tone",value=tone,values=tones)
            GridLayout(cols=2)
            Button("Generate Quiz",color="pink",on_click=submit_form, style='width: 100%;margin: auto;color: white;')
    
    @solara.component
    def FileDropDemo(): 
        content, set_content = solara.use_state("")
        filename, set_filename = solara.use_state("")
        size, set_size = solara.use_state(0)

        def on_file(f: FileInfo):
            set_filename(f["name"])
            set_size(f["size"])
            try:
                read_content = f["file_obj"].read()
                if read_content:
                    decoded_content = read_content.decode("utf-8")
                    set_content(decoded_content)
                else:
                    print("No content read from the file.")
            except Exception as e:
                print(f"Error reading or decoding the file: {e}")

        def content_effect():
              if content:
                print("Content state updated:", content)
                set_file_content(content)
                
        solara.use_effect(content_effect, [content])

        solara.FileDrop(
            label="Drag and drop a file here to read.",
            on_file=on_file,
            lazy=True,
        )
        if content and file_content:
            solara.Info(f"File {filename} has total length: {size}\n")
    
    
    def submit_form():
        if number_of_questions.value == 0:
            # show alert
            return False
        with open(os.path.join(os.getcwd())+'/Response.json','r') as file:
            RESPONSE_JSON = json.load(file)
        try:
            response = generate_response(
            file_content,
            number_of_questions.value,
            subject.value,
            tone.value,
            json.dumps(RESPONSE_JSON))
            if response and isinstance(response,list):
                set_quiz_data(response) 
                print(quiz_data)
            else:
                Text("Error in generating the quiz questions. Please try again.")
        except Exception as e:
            print(e)
            traceback.print_exception(type(e), e, e.__traceback__)
            return
    
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
                   title="Hana AI - Quiz generator",
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
                            file_with_ans_object = use_memo(lambda: open(generated_pdf_with_Ans, "rb"), [])
                            file_without_ans_object = use_memo(lambda: open(generated_pdf_without_Ans, "rb"), [])
                            with Row(style='width: 100%; justify-content: center; align-items: center;padding: 60px;'):
                                with FileDownload(file_with_ans_object, 'MCQs_With_Answers_HanaAi.pdf'):
                                    Button("Download Quiz with Answers", icon_name="mdi-cloud-download-outline", color="pink", style='width: 100%; margin: auto; color: white;')
                                with FileDownload(file_without_ans_object, 'MCQs_By_HanaAi.pdf'):
                                    Button("Download Quiz Only Question", icon_name="mdi-cloud-download-outline", color="pink", style='width: 100%; margin: auto; color: white;')   
    Footer()
                                
            
@component
def Page():
        solara.Style(
              Path(Path(__file__).parent / "assets/style.css" ))
        Home()
        Title("Hana AI - Quiz generator")
        

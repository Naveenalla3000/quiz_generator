from solara import *
import json
quiz_data = [
    {
        'MCQ': 'What is a common approach used by many recommender systems?',
        'options': 
            [
                'a: Collaborative filtering',
                'b: Content-based filtering',
                'c: Hybrid filtering',
                'd: Rule-based filtering'
            ],
        'Correct Answer': 'a'
    },
    {
        'MCQ': 'What is the main problem with conventional CF-based methods?',
        'options': 
            [
                'a: Data sparsity',
                'b: Cold start',
                'c: Overfitting',
                'd: Scalability'
            ],
        'Correct Answer': 'a'
    },
    {
        'MCQ': 'What additional information can be used to address the sparsity problem in CF-based methods?',
        'options': 
            [
                'a: Item content information',
                'b: User demographics',
                'c: Social network data',
                'd: All of the above'
            ],
        'Correct Answer': 'd'
    },
    {
        'MCQ': 'What is the name of the method that tightly couples learning from ratings and content information?',
        'options': 
            [
                'a: Collaborative topic regression (CTR)',
                'b: Matrix factorization',
                'c: Neighborhood-based methods',
                'd: Deep autoencoders'
            ],
        'Correct Answer': 'a'
    },
    {
        'MCQ': 'What is the main limitation of the latent representation learned by CTR?',
        'options': 
            [
                'a: It may not be effective when auxiliary information is sparse',
                'b: It may overfit to the training data',
                'c: It may not capture the semantic relationships between items',
                'd: It may not generalize well to new data'
            ],
        'Correct Answer': 'a'
    },
]
@solara.component
def Home():
    with AppLayout(color="pink",
                   title="AI - quiz generator",
                   style='width: 100%;'):
        with AppBar():
            Text("Developed by Naveen Alla")
        with Padding(8):
            with solara.Card(title="AI - quiz generator",
                            subtitle="Generate the quiz question in just seconds using the power of Ai",
                            margin="auto",
                            style='width: 60%;'):
                with Padding(8):
                    FileDrop(label="Drop .pdf or .txt file here",lazy=False)
                    GridLayout(cols=2)
                    InputText(label="Enter the subject")
                    GridLayout(cols=2)
                    InputInt(label="Enter the number of questions")
                    GridLayout(cols=2)
                    InputText(label="Enter the Tone")
                    GridLayout(cols=2)
                    Button("Generate Quiz",color="pink",style='width: 100%;margin: auto;color: white;')
                    GridLayout(cols=8)
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
                    GridLayout(cols=2)
                    with Row():
                        Button("Download Quiz Question With Answer",color="pink",style='width: 50%;margin: auto;color: white;')
                        Button("Download Quiz Question",color="pink",style='width: 50%;margin: auto;color: white;')

@solara.component
def Page():
        solara.Style('''
        .v-application--wrap > div:nth-child(2) > div:nth-child(2){
            display: none !important;
        }
        ''')
        Home()
        

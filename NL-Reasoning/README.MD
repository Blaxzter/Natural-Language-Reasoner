
# Natural Language Reasoner

This project researches the task of reasoning with constrained natural language (CNL).

You can find a working example on https://nl-reasoner.fabraham.dev/#/reasoner

## File Tree

```
src
├── data                  # Datasets for testing
├── logics                # Containing the general logic classes
│   ├── logic_functions   # Classes representing the logic functions
│   └── senteces          # CNL parser and sentence representations
├── playground            # Logic tests and jupyter notebooks
├── tests                 # Tests to keep the behaiviour consistent
├── utils                 # General util functions
├── visualization         # Tree generator and Applied Rule classes 
└── web                   # Containg the server classes
    └── files             # Frontend classes and examples 
```

## Setup

In order to run this project you can either use docker or install the dependencies
and run the app.py file.  

This project was made in python 3.8.8 no other versions were tested.   
In order to install the dependencies run:  
`pip install -r requirements.txt`

With the command:  
`python ./src/app.py`  
you can start the local server. 
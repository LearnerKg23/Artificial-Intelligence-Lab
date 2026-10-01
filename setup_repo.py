import os
import json
import shutil

base_dir = '/mnt/c/Users/Kushal Gupta/Desktop/ArtificialIntelligence'
source_docs_dir = '/mnt/c/Users/Kushal Gupta/.gemini/antigravity-ide/brain/428ac0eb-7343-4880-a943-ccad8891b1e9/scratch/vansh-ai-labs/Docs'
target_docs_dir = os.path.join(base_dir, 'Docs')

# 1. Create Docs directory and copy PDFs
os.makedirs(target_docs_dir, exist_ok=True)
for filename in os.listdir(source_docs_dir):
    if filename.endswith('.pdf'):
        shutil.copy(os.path.join(source_docs_dir, filename), os.path.join(target_docs_dir, filename))

# Copy specific PDFs into their lab folders
pdf_mapping = {
    'lab1_neural_models': 'neur_models_lab_ex.pdf',
    'lab2_agents': 'agents_lab.pdf',
    'lab3_search': 'search_lab_ex.pdf',
    'lab4_logic_planning': 'logic_lab_ex.pdf',
    'lab5_bayesian_networks': 'BN_lab.pdf'
}

for folder, pdf in pdf_mapping.items():
    src = os.path.join(target_docs_dir, pdf)
    dst = os.path.join(base_dir, folder, pdf)
    if os.path.exists(src):
        shutil.copy(src, dst)

# Remove the loose BN_lab.pdf if it exists
loose_pdf = os.path.join(base_dir, 'BN_lab.pdf')
if os.path.exists(loose_pdf):
    os.remove(loose_pdf)

# 2. Setup Labs for Notebooks and READMEs
labs = [
    ('lab1_neural_models', 'Neural Models Lab', 'neural_lab.py'),
    ('lab2_agents', 'Goal-Based Agents Lab', 'warehouse_agent.py'),
    ('lab3_search', 'Search and A* Lab', 'search_agent.py'),
    ('lab4_logic_planning', 'Logical Planning Lab', 'logic_planner.py'),
    ('lab5_bayesian_networks', 'Bayesian Networks Lab', 'lab_implementation.py')
]

# Root README
root_readme = '''# Artificial Intelligence (CS F407) - Labs

This repository contains my complete laboratory submissions for the Artificial Intelligence course. 
All labs have been successfully implemented and tested.

## Directory Structure
- **Docs/**: Original assignment PDFs
- **lab1_neural_models/**: PyTorch implementation of neural models and activation functions
- **lab2_agents/**: Goal-based agent utilizing BFS in a warehouse environment
- **lab3_search/**: A* Search implementation with heuristic evaluation
- **lab4_logic_planning/**: Logical reasoning and STRIPS-style planning
- **lab5_bayesian_networks/**: Autoregressive language modeling and probabilities

## Execution
Each lab folder contains a standalone Python script, a Jupyter Notebook, and a detailed Lab Report.
'''
with open(os.path.join(base_dir, 'README.md'), 'w') as f:
    f.write(root_readme)

# Iterate through labs to create mini READMEs and Notebooks
for folder, title, py_file in labs:
    folder_path = os.path.join(base_dir, folder)
    
    # Mini README
    mini_readme = f'# {title}\n\nThis directory contains the implementation and report for the {title}.\n\n### Files:\n- `{py_file}`: The main Python script.\n- `{py_file.replace(".py", "_notebook.ipynb")}`: Interactive Jupyter Notebook version.\n- `*_Lab_Report.md`: Complete lab reflection and submission report.\n'
    with open(os.path.join(folder_path, 'README.md'), 'w') as f:
        f.write(mini_readme)
        
    # Jupyter Notebook generation
    py_path = os.path.join(folder_path, py_file)
    if os.path.exists(py_path):
        with open(py_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        notebook = {
            'cells': [
                {
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': [f'# {title}\n', 'Run the cell below to execute the complete implementation for this lab.']
                },
                {
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': [code]
                }
            ],
            'metadata': {
                'kernelspec': {
                    'display_name': 'Python 3',
                    'language': 'python',
                    'name': 'python3'
                },
                'language_info': {
                    'name': 'python',
                    'version': '3.8'
                }
            },
            'nbformat': 4,
            'nbformat_minor': 4
        }
        
        nb_path = os.path.join(folder_path, py_file.replace('.py', '_notebook.ipynb'))
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)

# Create planner.pl for Logic lab
prolog_content = '''% Declarative Knowledge Base for Logical Planning
% Action Preconditions and Effects

% move(Box, From, To)
action(move(B, X, Y), 
       [at(B, X), empty(Y)], 
       [at(B, Y), empty(X)], 
       [at(B, X), empty(Y)]).

% state definitions
initial_state([at(box1, locA), empty(locB), empty(locC)]).
goal_state([at(box1, locC)]).
'''
with open(os.path.join(base_dir, 'lab4_logic_planning', 'planner.pl'), 'w') as f:
    f.write(prolog_content)

print('Successfully generated all repository structure files!')

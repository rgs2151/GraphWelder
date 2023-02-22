from welder.node import InputPipe, OutputPipe, ConcatJoin
from welder.pipe.models import BertBoolQ
from welder.pipe.htmlparser import HTMLContext2Lines, HTMLTable2Lines
from welder.pipe.linespre_processor import Lower, RemoveUnwantedChars, RemoveSpaces, WordThreshold, SplitIntoSentences
from welder.pipe.db import Chunk2Faiss
from welder.pipe.retriever import DenseRetrieverFS
from welder.pipeline import PipeLine
import json

PL = PipeLine()

context_branch =[
    InputPipe('context_input', inputs=[str, list], fix_inputs=2),
    HTMLContext2Lines('HTML Context 2 Lines'),
    HTMLTable2Lines('HTML Table 2 Lines', drop_HTML=True),
    RemoveUnwantedChars('Remove Unwanted Chars'),
    WordThreshold('Word Threshold'),
    RemoveSpaces('Remove Spaces'),
    Lower('Lower'),
    Chunk2Faiss('Lines 2 Faiss Database'),
    DenseRetrieverFS('Retriever'),
]

question_branch = [
    InputPipe('question_input', inputs=[]),
]

preprocess_join = PL.branch_connect([context_branch, question_branch], join_pipe = ConcatJoin('Join 1'))

PL.sequential_connect([
    preprocess_join,
    BertBoolQ('BoolQ'),
    OutputPipe('OutPut 1', check = False)
])

with open(r'demo\data\0.json', 'rb') as f:
    content = json.load(f)['content']

results = PL.flow([[content, []], []])
print(results)
from welder.node import InputPipe, OutputPipe, ConcatJoin
from welder.pipe.models import BertBoolQ
from welder.pipe.htmlparser import HTMLContext2Lines, HTMLTable2Lines
from welder.pipe.linespre_processor import Lower, RemoveUnwantedChars, RemoveSpaces, WordThreshold, SplitIntoSentences
from welder.pipe.db import Chunk2Faiss
from welder.pipe.retriever import DenseRetrieverFS
from welder.pipeline import PipeLine
import json


PL = PipeLine()
PL.sequential_connect([
    InputPipe('Input 1', inputs=[str, list], fix_inputs=2),

    HTMLContext2Lines('HTML Context 2 Lines'),
    HTMLTable2Lines('HTML Table 2 Lines', drop_HTML=True),

    RemoveUnwantedChars('Remove Unwanted Chars'),
    WordThreshold('Word Threshold'),
    RemoveSpaces('Remove Spaces'),
    SplitIntoSentences('split into sentences'),
    Lower('Lower'),

    OutputPipe('OutPut 1', check=False)
])

with open(r'demo\data\0.json', 'rb') as f:
    content = json.load(f)['content']

results = PL.flow([[content, []]])
print(results)
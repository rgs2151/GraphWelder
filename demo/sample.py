import json

from welder.graph import Graph
from welder.node import InputPipe, MergeJoin, OutputPipe, ConcatJoin
from welder.pipeline import PipeLine

from welder.pipe.htmlparser import HTMLContext2Lines, HTMLTable2Lines
from welder.pipe.linespre_processor import Lower, RemoveUnwantedChars, RemoveSpaces, WordThreshold, SplitIntoSentences
# from welder.pipe.db import Chunk2ES, Chunk2Faiss
# from welder.pipe.retriever import DenseRetrieverFS
# from welder.pipe.extractivereader import TransformerReader, FarmReader
# from welder.pipe.abstractivereader import HaystackARElasticSearchRA, HaystackARFAISSRA
from welder.pipe.chunking import SlidingWindowSplit


PL = PipeLine()
PL.sequential_connect([
    InputPipe('Input 1', inputs=[]),
    OutputPipe('O1', check=False)
])

with open('root\DB\DB-Raw\\0.json', 'rb') as f:
    content = json.load(f)['content']

try:
    # results = PL.flow([[content, []], [content, []]])
    results = PL.flow([[]])
    print(results[0][0][0])

except Exception as err:
    raise err
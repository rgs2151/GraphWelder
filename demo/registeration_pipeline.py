import json

from welder.graph import Graph
from welder.node import InputPipe, MergeJoin, OutputPipe
from welder.pipeline import PipeLine

from welder.pipe.htmlparser import HTMLContext2Lines, HTMLTable2Lines
# from welder.pipe.linespre_processor import Lower, RemoveUnwantedChars, RemoveSpaces, WordThreshold
# from welder.pipe.db import Chunk2ES, Chunk2Faiss
# from welder.pipe.retriever import DenseRetrieverFS
# from welder.pipe.extractive_reader import TransformerReader, FarmReader
# from welder.pipe.abstractive_reader import HaystackARElasticSearchRA, HaystackARFAISSRA
# from welder.pipe.chunking import SlidingWindowSplit


PL = PipeLine()
I1 = InputPipe('Input 1', inputs=[str, list], fix_inputs=2)
P1 = HTMLContext2Lines('HTML Context 2 Lines', drop_HTML=True)
P2 = HTMLTable2Lines('HTML Context 2 Tables', drop_HTML=True)
O1 = OutputPipe('Output 1', check=False)

PL.register(I1, P1)
PL.register(I1, P2)
PL.register(P1, O1)

with open('root\DB\DB-Raw\\0.json', 'rb') as f:
    content = json.load(f)['content']

results = PL.flow([[content, []]])
print(results[0][0][0])
print(PL.reverse_graph)
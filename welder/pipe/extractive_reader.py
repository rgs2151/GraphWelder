from welder.node import Pipe
from haystack.document_stores import ElasticsearchDocumentStore as eds
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader,TransformersReader,DensePassageRetriever


class FarmReader(Pipe):

    def __init__(self, label: str, model_name_or_path='deepset/roberta-base-squad2', use_gpu=True) -> None:
        super().__init__(label, inputs=[DensePassageRetriever], outputs=[ExtractiveQAPipeline])
        self.model = model_name_or_path
        self.gpu = use_gpu

    def pipe(self):
        self.retriever = self.values[0]
        reader = FARMReader( model_name_or_path=self.model, use_gpu=self.gpu)
        pipe = ExtractiveQAPipeline( reader=reader, retriever=self.retriever)
        return [pipe]

    
class TransformerReader(Pipe):
    
    def __init__(self, label : str, model_name_or_path = 'distilbert-base-uncased-distilled-squad', tokenizer = "distilbert-base-uncased", use_gpu = True) -> None:
        super().__init__(label, inputs = [DensePassageRetriever], outputs = [ExtractiveQAPipeline])
        self.model = model_name_or_path
        self.tokenizer = tokenizer
        self.gpu = use_gpu

    def pipe(self):
        self.retriever = self.values[0]
        reader = TransformersReader(model_name_or_path = self.model, tokenizer = self.tokenizer, use_gpu = self.gpu)
        pipe = ExtractiveQAPipeline(reader=reader, retriever=self.retriever)
        return [pipe]
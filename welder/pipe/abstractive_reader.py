from haystack.document_stores.base import BaseDocumentStore
from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore
from welder.node import Pipe
from haystack.document_stores import ElasticsearchDocumentStore as eds, FAISSDocumentStore
from haystack.nodes import DensePassageRetriever, retriever
from haystack.pipelines import GenerativeQAPipeline
from haystack.nodes import RAGenerator
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch

class HaystackARElasticSearchRA(Pipe):

    def __init__(self, label: str, model_name_or_path="facebook/rag-token-nq", use_gpu=True, top_k=1, max_length=200, min_length=2, embed_title=True, num_beams=2) -> None:
        from haystack.document_stores import ElasticsearchDocumentStore

        super().__init__(label, inputs=[ElasticsearchDocumentStore], outputs=[GenerativeQAPipeline])
        self.model = model_name_or_path
        self.gpu = use_gpu
        self.top_k = top_k
        self.max_length = max_length
        self.min_length = min_length
        self.embed_title = embed_title
        self.num_beams = num_beams

    def pipe(self):
        retriever = self.values[0]
        generator = RAGenerator(model_name_or_path=self.model, use_gpu=self.gpu, top_k=self.top_k,
                                max_length=self.max_length, min_length=self.min_length, embed_title=self.embed_title, num_beams=self.num_beams)
        pipeline = GenerativeQAPipeline(generator, retriever)
        return [pipeline]


class HaystackARFAISSRA(Pipe):

    def __init__(self, label: str, model_name_or_path="facebook/rag-token-nq", use_gpu=True, top_k=1, max_length=200, min_length=2, embed_title=True, num_beams=2) -> None:

        super().__init__(label, inputs=[DensePassageRetriever], outputs=[GenerativeQAPipeline])
        self.model = model_name_or_path
        self.gpu = use_gpu
        self.top_k = top_k
        self.max_length = max_length
        self.min_length = min_length
        self.embed_title = embed_title
        self.num_beams = num_beams

    def pipe(self):
        retriever = self.values[0]
        generator = RAGenerator(model_name_or_path=self.model, use_gpu=self.gpu, top_k=self.top_k,
                                max_length=self.max_length, min_length=self.min_length, embed_title=self.embed_title, num_beams=self.num_beams)
        pipeline = GenerativeQAPipeline(generator, retriever)
        return [pipeline]

class HFT5AbsQA(Pipe):

    class T5AbsQAPipeline:
        def __init__(self, retriever) -> None:
            self.tokenizer = AutoTokenizer.from_pretrained("tuner007/t5_abs_qa")
            self.model = AutoModelWithLMHead.from_pretrained("tuner007/t5_abs_qa")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to(self.device)
            self.retriever = retriever

        def run(self, query: str, params = None) -> str:
            if not params.Retriever.top_k:
                retriever_top_k = 10
            else:
                retriever_top_k = params.Retriever.top_k
            context = self.gen_context(query, retriever_top_k)
            answer = self.gen_answer(query, context)
            return answer

        def gen_context(self, query: str, top_k: int) -> str:
            documents = self.retriever.retrieve(
                query=query,
                top_k=top_k
            )
            contexts = " ".join([doc.context for doc in documents])
            return contexts

        def gen_answer(self, question: str, context: str) -> str:
            input_text = f"context: {context} <question for context: {question} </s>"
            features = self.tokenizer([input_text], return_tensors='pt')
            out = self.model.generate(input_ids=features['input_ids'].to(self.device), attention_mask=features['attention_mask'].to(self.device))
            return self.tokenizer.decode(out[0])

    def __init__(self, label: str):
        super().__init__(label, inputs=[DensePassageRetriever], outputs=[self.T5AbsQAPipeline])

    def pipe(self):
        generator = self.T5AbsQAPipeline(self.values[0])
        return [generator]

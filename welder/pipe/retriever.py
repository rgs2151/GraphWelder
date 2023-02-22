from welder.node import Pipe
from haystack.document_stores import ElasticsearchDocumentStore as eds
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever


class DenseRetrieverFS(Pipe):

    def __init__(self, label: str, query_embedding_model='facebook/dpr-question_encoder-single-nq-base', passage_embedding_model='facebook/dpr-ctx_encoder-single-nq-base', use_gpu=True, embed_title=True) -> None:
        super().__init__(label, inputs=[FAISSDocumentStore], outputs=[DensePassageRetriever])
        self.query_embedding_model = query_embedding_model
        self.passage_embedding_model = passage_embedding_model
        self.use_gpu = use_gpu
        self.embed_title = embed_title

    def pipe(self):
        ds = self.values[0]
        retriever = DensePassageRetriever(
            document_store=ds, query_embedding_model=self.query_embedding_model,
            passage_embedding_model=self.passage_embedding_model, 
            use_gpu=self.use_gpu, embed_title=self.embed_title
        )
        
        ds.update_embeddings(retriever=retriever)
        return [retriever]

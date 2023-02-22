from welder.node import Pipe
import requests
from pathlib import Path


class DB(Pipe):

    def __init__(self, label: str) -> None:
        super().__init__(label, inputs=[list], outputs=[])
        self.set_check('out', False)


class Chunk2ES(DB):
    ''' Make sure Elastic Search is Installed and Running
        some useful commands
        http://localhost:9200/welder/_search?size=65;pretty
    '''

    def __init__(self, label: str, domain='localhost', host=f"http://localhost:9200", index="welder-chunk2es") -> None:
        super().__init__(label)

        from haystack.document_stores import ElasticsearchDocumentStore  # lazy import

        self.outs = [ElasticsearchDocumentStore]
        self.set_check('out', True)

        self.domain = domain
        self.host = host
        self.index = index

        self.check_elasticsearch()
        self.ds = ElasticsearchDocumentStore(
            host=self.domain, index=self.index, username='', password='')

    def check_elasticsearch(self):
        res = requests.get(self.host)
        if res.status_code != 200:
            raise Exception(f'Elasticsearch not working at {self.host}')

    def pipe(self):
        chunks = self.values[0]

        self.ds.delete_documents(index=self.index)
        data = self.create_data(chunks)

        print(f"saving {len(data)} to {self.index}")

        self.ds.write_documents(data)

        return [self.ds]

    def create_data(self, chunks):
        return [{'content': chunk} for chunk in chunks]


class Chunk2Faiss(DB):

    def __init__(self, label: str, index='welder-chunk2faiss') -> None:
        super().__init__(label)

        from haystack.document_stores import FAISSDocumentStore  # lazy import

        self.outs = [FAISSDocumentStore]
        self.set_check('out', True)

        self.index = index
        self.faiss_index_path = 'welder_Index.faiss'
        self.faiss_sql_path = 'welder_document_store.db'
        self.faiss_config_path = 'welder_Index_Config.json'

        if Path(self.faiss_sql_path).exists():
            Path(self.faiss_index_path).unlink()
            Path(self.faiss_sql_path).unlink()
            Path(self.faiss_config_path).unlink()

        self.db = FAISSDocumentStore(sql_url=self.faiss_sql_path, vector_dim=768,
                                    faiss_index_factory_str="Flat", index=self.index, return_embedding=True)

        self.db.save(index_path=self.faiss_index_path,
                    config_path=self.faiss_config_path)

    def create_data_faiss(self):
        return [{'content': chunk} for chunk in self.chunks]

    def pipe(self):
        self.chunks = self.values[0]
        data = self.create_data_faiss()
        self.db.write_documents(data)
        print(f"saving {len(data)} to {self.index}")
        return [self.db]

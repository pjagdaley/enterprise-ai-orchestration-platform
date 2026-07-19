"""
OpenSearch service for lexical (BM25) search.
"""

from opensearchpy import OpenSearch

from app.core.config import settings


class OpenSearchService:
    """
    Wrapper around OpenSearch client.
    """

    def __init__(self) -> None:

        self._client = OpenSearch(
            hosts=[
                {
                    "host": settings.opensearch_host,
                    "port": settings.opensearch_port,
                }
            ],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
        )
        self._index_name = settings.opensearch_index
        self._create_index()

    def _create_index(self) -> None:
        """
        Create index if it does not exist.
        """

        if self._client.indices.exists(
            index=self._index_name
        ):
            return

        body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            },
            "mappings": {
                "properties": {
                    "document_id": {
                        "type": "keyword"
                    },
                    "chunk_id": {
                        "type": "keyword"
                    },
                    "source_path": {
                        "type": "keyword"
                    },
                    "extension": {
                        "type": "keyword"
                    },
                    "content": {
                        "type": "text"
                    },
                }
            },
        }

        self._client.indices.create(
            index=self._index_name,
            body=body,
        )

    def index_document(
        self,
        document: dict,
    ) -> None:
        """
        Index one chunk.
        """

        self._client.index(
            index=self._index_name,
            id=document["chunk_id"],
            body=document,
            refresh=True,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list:
        """
        Perform BM25 search.
        """

        body = {
            "size": top_k,
            "query": {
                "match": {
                    "content": query
                }
            },
        }

        response = self._client.search(
            index=self._index_name,
            body=body,
        )

        return response["hits"]["hits"]

    def delete_document(
        self,
        chunk_id: str,
    ) -> None:
        """
        Delete a chunk.
        """

        self._client.delete(
            index=self._index_name,
            id=chunk_id,
            ignore=[404],
        )
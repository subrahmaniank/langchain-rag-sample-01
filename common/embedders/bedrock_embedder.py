import os
from typing import List

from langchain.schema import Document
from langchain_community.embeddings import BedrockEmbeddings

from common.embedders.abstract_document_embedder import AbstractDocumentEmbedder
from common.utils.aws_util import AWSUtil
from logging_config import setup_logger


logger = setup_logger(__name__)


class BedrockEmbedder(AbstractDocumentEmbedder):

    def __init__(self):
        _embedding_model_provider = os.environ.get(
            "EMBEDDING_MODEL_PROVIDER", "OpenAI"
        ).lower()
        logger.debug(f"Using {_embedding_model_provider} embeddings")

        if _embedding_model_provider != "aws":
            raise ValueError(f"{_embedding_model_provider} is not supported")

        _model_id = os.environ.get("EMBEDDING_MODEL_ID", "text-embedding-ada-002")
        aws_util = AWSUtil()
        client = aws_util.get_client("bedrock-runtime")
        self.embeddings = BedrockEmbeddings(client=client, model_id=_model_id)

        logger.info(f"Bedrock embedder initialized using {_model_id} model")


    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        logger.info("Start of embedding documents")
        # iterate through the document List
        doc_content: List[str] = []
        for document in documents:
            doc_content.append(document.page_content)

        logger.debug(f"Embedding {len(doc_content)} documents")
        return self.embeddings.embed_documents(doc_content)

    def embed_query(self, input_text: str) -> List[float]:
        return self.embeddings.embed_query(input_text)

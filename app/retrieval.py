"""
Prompt Retrieval Module - Semantic search for prompt suggestions.

Uses sentence transformers and FAISS for efficient retrieval
of similar prompts from a curated prompt bank to provide
suggestions for scene enhancement.
"""

import logging
import json
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

logger = logging.getLogger(__name__)

EMB_MODEL_NAME = "all-MiniLM-L6-v2"  # Local embeddings model
VECTOR_DIM = 384


class PromptRetrieval:
    """
    Semantic retrieval system for prompt bank suggestions.

    Maintains a FAISS index of embeddings for efficient similarity search.
    """

    def __init__(self, bank_path: str = "../data/sample_prompts.json"):
        """
        Initialize retrieval system with prompt bank.

        Args:
            bank_path: Path to JSON file containing prompt bank
        """
        try:
            self.model = SentenceTransformer(EMB_MODEL_NAME)
            logger.info(f"Loaded embedding model: {EMB_MODEL_NAME}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.model = None

        self.bank_path = Path(bank_path)
        self.prompts: List[Dict[str, str]] = []
        self.embeddings: np.ndarray = None
        self.index: faiss.IndexFlatL2 = None
        self._load_bank()

    def _load_bank(self) -> None:
        """Load and index prompt bank from JSON file."""
        if not self.bank_path.exists():
            logger.warning(f"Prompt bank not found at {self.bank_path}")
            return

        try:
            with open(self.bank_path, "r", encoding="utf-8") as f:
                self.prompts = json.load(f)
            logger.info(f"Loaded {len(self.prompts)} prompts from bank")

            if not self.prompts or not self.model:
                return

            # Build embeddings and FAISS index
            texts = [p.get("prompt", "") for p in self.prompts]
            self.embeddings = self.model.encode(
                texts,
                convert_to_numpy=True
            )
            self.index = faiss.IndexFlatL2(
                self.embeddings.shape[1]
            )
            self.index.add(self.embeddings.astype(np.float32))
            logger.info("Built FAISS index successfully")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in prompt bank: {e}")
        except Exception as e:
            logger.error(f"Error loading prompt bank: {e}")

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """
        Retrieve top-k similar prompts for given query.

        Args:
            query: Text query to search
            k: Number of results to return

        Returns:
            List of similar prompts from bank
        """
        if self.index is None or self.model is None:
            logger.warning("Retrieval index not available")
            return []

        try:
            q_emb = self.model.encode(
                [query],
                convert_to_numpy=True
            ).astype(np.float32)
            dists, ids = self.index.search(q_emb, k)

            results = []
            for idx in ids[0]:
                if 0 <= idx < len(self.prompts):
                    results.append(self.prompts[idx])

            logger.debug(f"Retrieved {len(results)} prompts for query")
            return results

        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []

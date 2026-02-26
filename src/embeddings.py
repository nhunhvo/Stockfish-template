"""
Image embedding utilities using CLIP model.
Converts images into high-dimensional vector representations for similarity search.
"""
from PIL import Image
from sentence_transformers import SentenceTransformer
from typing import List


class ImageEmbedder:
    """Handles image embedding generation using CLIP model."""

    def __init__(self, model_name: str, dimension: int):
        """
        Initialize the Sentence Transformers model for image embeddings.

        Args:
            model_name: Name of the sentence-transformers model
            dimension: Dimension of the embedding
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = dimension
    
    def get_image_embedding(self, image_path: str) -> List[float]:
        """
        Generate embedding vector for an image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of float values representing the image embedding
        """
        image = self._load_image(image_path)
        embedding = self.model.encode(image)
        return embedding.tolist()
    
    def get_batch_embeddings(self, image_paths: List[str]) -> List[List[float]]:
        images = [Image.open(path) for path in image_paths]
        embeddings = self.model.encode(images)
        return [embedding.tolist() for embedding in embeddings]
    
if __name__ == "__main__":
    embedder = ImageEmbedder(model_name="clip-ViT-B-32", dimension=512)

    image_paths = [
        "static/clownfish.jpeg",
        "static/catfish.jpeg",
        "static/pelican.jpeg"
    ]

    embeddings = embedder.get_batch_embeddings(image_paths)

    print(f"Generated {len(embeddings)} embeddings")
    print(f"Each embedding length: {len(embeddings[0])}")
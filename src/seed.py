from embeddings import ImageEmbedder
from database import FishVectorDB
import csv

def seed_from_csv(
    csv_path: str,
    embedder: ImageEmbedder,
    db: FishVectorDB
) -> None:
    """
    Seed Pinecone database from CSV file.
    
    Args:
        csv_path: Path to CSV file with columns: id, species, description, region, conservation_status, image_path
        embedder: ImageEmbedder instance for generating embeddings
        db: FishVectorDB instance
    """

    fish_records = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Generate embedding from image
            image_path = f"static/{row['id']}.jpeg"
            print("Image path: ", image_path)
            embedding = embedder.get_image_embedding(image_path)
            # Prepare metadata (flat structure only)
            metadata = {
                "species": row['species'],
                "description": row['description'],
                "region": row.get('region', ''),
                "conservation_status": row.get('conservation_status', '')
            }

            fish_records.append((row['id'], embedding, metadata))
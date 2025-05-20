#!/usr/bin/env python
"""
Initialization script to load sample documents.
This will run automatically during application startup.
"""

import os
import sys
import logging
import pathlib
import django

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project directory to the Python path
script_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(script_dir))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rna_backend.settings")
django.setup()

# Now we can import Django models
from api.models import Document
from api.ingestion.chunking_utils import process_pdf_document

def load_sample_documents():
    """
    Load sample documents from the data directory
    """
    # Check if we've already loaded documents
    doc_count = Document.objects.count()
    if doc_count > 0:
        logger.info(f"Found {doc_count} existing documents. Skipping initialization.")
        return
    
    # Paths to sample documents
    logger.info("Starting document loading process")
    protocols_dir = script_dir / "data" / "sample_docs" / "community_protocols"
    
    if not protocols_dir.exists():
        logger.error(f"Directory not found: {protocols_dir}")
        return
    
    # Process protocol documents
    logger.info(f"Processing protocol documents from {protocols_dir}")
    for protocol_file in protocols_dir.glob("*.pdf"):
        try:
            filename = os.path.basename(protocol_file)
            # Extract simplified title from filename
            title = filename.replace(".pdf", "").replace("-", " ").replace("_", " ")
            
            logger.info(f"Processing protocol: {filename}")
            doc = Document.objects.create(
                title=title,
                doc_type="protocol",
                author="Lab Protocol",
                year=2023,
                file_path=str(protocol_file),
                status="pending"
            )
            
            logger.info(f"Created document record for {filename}")
            
            try:
                logger.info(f"Processing document content for {filename}")
                process_pdf_document(
                    doc_id=doc.id,
                    pdf_path=str(protocol_file),
                    chunk_size=400,
                    chunk_overlap=100
                )
                
                doc.status = "processed"
                doc.save()
                
                logger.info(f"Successfully processed protocol: {filename}")
            except Exception as e:
                logger.error(f"Error processing document content: {e}")
                # Continue with next document
        except Exception as e:
            logger.error(f"Error processing protocol {protocol_file}: {e}")
    
    # Print summary
    doc_count = Document.objects.count()
    logger.info(f"Initialization complete. {doc_count} documents processed.")

if __name__ == "__main__":
    logger.info("Running database initialization")
    try:
        load_sample_documents()
        logger.info("Initialization complete")
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
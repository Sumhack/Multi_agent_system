import os
import PyPDF2

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def read_pdf_with_pages(file_path):
    """Read PDF and return text with page numbers"""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pages_text = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():  # Only add non-empty pages
                pages_text.append((text, page_num))
    return pages_text


def chunk_text_with_pages(pages_text):
    """Split text into chunks while maintaining page number information"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks_with_pages = []
    for text, page_num in pages_text:
        chunks = text_splitter.split_text(text)
        chunks_with_pages.extend([(chunk, page_num) for chunk in chunks])

    return chunks_with_pages


def create_embeddings_and_store(chunks_with_pages, file_path, folder_name):
    """Create and store embeddings with page number metadata"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key="gemini-api-key"
    )

    # Filter out any empty chunks
    filtered_chunks_with_pages = [(chunk, page) for chunk, page in chunks_with_pages if chunk.strip()]

    if not filtered_chunks_with_pages:
        print(f"No non-empty chunks found for {file_path} in folder {folder_name}. Skipping.")
        return

    # Separate chunks and pages
    chunks, pages = zip(*filtered_chunks_with_pages)

    # Create metadata including page numbers
    metadata = [
        {
            "source": file_path,
            "folder": folder_name,
            "chunk_index": i,
            "page_number": page
        }
        for i, page in enumerate(pages)
    ]

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata,
        persist_directory="./chroma_db"
    )

    vectorstore.persist()
    print(f"Embeddings created and stored for {file_path} in folder {folder_name}")


def process_pdf_files_in_directories(directories):
    """Process all PDF files in given directories"""
    # If directories is a string, convert it to a list
    if isinstance(directories, str):
        directories = [directories]

    for directory_path in directories:
        folder_name = os.path.basename(directory_path)

        # Get all PDF files in the directory
        pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]

        for pdf_file in pdf_files:
            file_path = os.path.join(directory_path, pdf_file)

            # Read PDF with page numbers
            pages_text = read_pdf_with_pages(file_path)

            # Chunk text while maintaining page numbers
            chunks_with_pages = chunk_text_with_pages(pages_text)

            # Create and store embeddings
            create_embeddings_and_store(chunks_with_pages, file_path, folder_name)


# Usage
folder_paths = "/content/sample_data/Data"
process_pdf_files_in_directories(folder_paths)

"""Module to handle summary generation"""
import concurrent.futures
import math
import ollama
from app.config import settings

class LlamaService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LlamaService, cls).__new__(cls)
        return cls._instance
    
    def summarize_chunk(self, chunk):
        """Generate summary of chunk"""
        model = settings.OLLAMA_MODEL
        messages = [{
            "role":"system",
            "content": "Generate a brief summary for the provided content from a book."
        },
        {
            "role":"user",
            "content": chunk
        }]

        response = ollama.chat(
            model = model,
            messages = messages
        )
        # Assuming the output is directly the summary in JSON format
        summary = response['message']['content']
        print(summary)
        return summary

    def chunk_text(self, book_text, chunk_size=settings.CHUNK_SIZE):
        """
        Split the book text into chunks of a given size (in characters or tokens).
        Ensure the chunking is done at logical points (e.g., chapters, paragraphs).
        """
        num_chunks = math.ceil(len(book_text) / chunk_size)
        chunks = [book_text[i * chunk_size: (i + 1) * chunk_size] for i in range(num_chunks)]
        return chunks

    def generate_book_summary(self, book_text):
        """
        Generate a summary for the entire book by processing chunks in parallel.
        """
        # Step 1: Chunk the text into manageable parts
        chunks = self.chunk_text(book_text)
        
        # Step 2: Use concurrent processing to summarize each chunk
        with concurrent.futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            # Map summarize_chunk function to each chunk in parallel
            summaries = list(executor.map(self.summarize_chunk, chunks))
        
        # Step 3: Aggregate the summaries from each chunk
        # This could be further summarized if the book is large
        final_summary = "\n".join(summaries)  # Concatenate all chunk summaries
        
        # Optional: You can further summarize the collected summaries
        final_summary = self.summarize_chunk(final_summary)  # Summarize the aggregated summaries
        return final_summary

    async def generate_summary(self, content: str) -> str:
        """Main driver function"""
        try:
            return self.generate_book_summary(content)
            
        except Exception as e:
            raise Exception(f"Ollama model error: {e}")

llama_service = LlamaService()

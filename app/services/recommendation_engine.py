"""Module to handle recommendation engine"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.config import settings


# Initialize the embedding model 
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)


def create_book_embeddings(books):
    """Create book embeddings using Embedding model"""
    book_data = []
    for book in books:
        # Concatenate relevant fields for the embedding (summary, title, author, genre)
        book_info = f"{book.title} {book.author} {book.genre} {book.year_published} {book.summary}"
        book_data.append(book_info)
    
    # Create embeddings for each book
    embeddings = embedding_model.encode(book_data, convert_to_tensor=True)
    return embeddings

def process_user_query(user_query, book_embeddings, books, top_n=2, threshold=0.9):
    """Create embedding for the user query"""
    query_embedding = embedding_model.encode([user_query], convert_to_tensor=True)
    
    # Calculate cosine similarity between the query and each book's embedding
    similarities = cosine_similarity(query_embedding, book_embeddings)
    
     # Filter books by the similarity threshold and get the top N indices
    top_indices = [
        i for i in np.argsort(similarities)[::-1]
        if similarities[i] >= threshold
    ][:top_n]  # Limit to the top N results that meet the threshold
    
    
    # Get the top 2 matching book titles
    top_books = [books[i].title for i in top_indices]
    return top_books if top_books else ["No highly similar matches found."]

def recommend_books(user_query, books):
    """Recommendation orchestrator"""
    # Create embeddings for the books
    book_embeddings = create_book_embeddings(books)
    
    # Process the user query and get top 2 matching books
    top_books = process_user_query(user_query, book_embeddings, books)
    
    return top_books
    
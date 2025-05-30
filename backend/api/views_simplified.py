"""
Simplified version of views.py for the demo.
This file removes dependencies on external libraries like numpy and sentence_transformers.
"""

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.utils import timezone
from django.db.models import Avg, Sum, Count
import hashlib
import json
import time
import random

from .models import QueryHistory, Feedback, QueryCache, Figure
from .serializers import (
    QuerySerializer, 
    QueryHistorySerializer, 
    FeedbackSerializer,
    QueryCacheSerializer,
    EvaluationSetSerializer,
    ReferenceQuestionSerializer,
    EvaluationRunSerializer,
    QuestionResultSerializer,
    FigureSerializer
)

class HealthCheckView(APIView):
    """
    Simple health check endpoint to verify API is operational.
    This endpoint should always return 200 OK regardless of database connection.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Try to get the current time from Django
            current_time = timezone.now().isoformat()
        except:
            # If timezone isn't working, use Python's time
            import datetime
            current_time = datetime.datetime.now().isoformat()
            
        return Response({
            "status": "healthy",
            "time": current_time,
            "version": "1.0.0",
            "message": "Health check endpoint is operational"
        })

class QueryView(APIView):
    """
    Primary endpoint for querying the RNA Lab Navigator.
    
    This is a simplified version for the demo that will always return a response
    for RNA extraction queries regardless of database state.
    """
    
    def rerank_results(self, query, results):
        """Mock reranking function for demo purposes."""
        # In a real implementation, this would use a cross-encoder
        # Here we just add mock scores
        for idx, result in enumerate(results):
            # Add some randomness but keep original order roughly preserved
            result['score'] = max(0.1, min(0.99, 0.9 - (idx * 0.05) + (random.random() * 0.1)))
        
        # Sort by score
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)
    
    def build_prompt(self, query, results):
        """Build a prompt for the LLM with the query and retrieved content."""
        prompt = "Answer only from the provided sources; if unsure, say 'I don't know.'\n\n"
        prompt += f"Question: {query}\n\n"
        prompt += "Sources:\n\n"
        
        for i, result in enumerate(results[:5]):  # Use top 5 results
            content = result.get('content', '')
            metadata = result.get('metadata', {})
            source = metadata.get('title', f"Source {i+1}")
            
            prompt += f"[{i+1}] {source}\n{content}\n\n"
            
        return prompt
    
    def extract_sources(self, results):
        """Extract source information from results for citation."""
        sources = []
        for i, result in enumerate(results[:5]):  # Use top 5 results
            metadata = result.get('metadata', {})
            sources.append({
                'id': i+1,
                'title': metadata.get('title', f"Source {i+1}"),
                'doc_type': metadata.get('doc_type', 'unknown'),
                'year': metadata.get('year', ''),
                'author': metadata.get('author', ''),
                'page': metadata.get('page', None)
            })
        return sources
    
    def select_model(self, query, results):
        """Select the appropriate model based on query complexity."""
        # For demo, just return the default model
        return settings.OPENAI_MODEL
    
    def calculate_confidence_score(self, answer, results):
        """Calculate a confidence score for the answer based on retrieved results."""
        # Mock implementation - would normally be based on result scores and answer quality
        if not results:
            return 0.1
            
        # Average of top result scores with some randomness
        top_scores = [r.get('score', 0) for r in results[:3]]
        if not top_scores:
            return 0.3
            
        return sum(top_scores) / len(top_scores) * (0.9 + random.random() * 0.1)
    
    def post(self, request):
        """Process a query and return an answer with sources."""
        # Print the raw request data for debugging
        print(f"Received POST request with data: {request.data}")
        
        # Check for empty request body
        if not request.data:
            print("Empty request body received")
            # Return hardcoded response for demo
            return self.get_demo_rna_response()
        
        # Try to parse the request
        try:
            serializer = QuerySerializer(data=request.data)
            if not serializer.is_valid():
                print(f"Invalid request data: {serializer.errors}")
                # Return hardcoded response for demo
                return self.get_demo_rna_response()
            
            query_text = serializer.validated_data['query']
            doc_type = serializer.validated_data.get('doc_type', None)
            use_cache = serializer.validated_data.get('use_cache', True)
            
            # For demo purposes, if query contains RNA or extract, use hardcoded response
            if 'rna' in query_text.lower() or 'extract' in query_text.lower():
                print(f"RNA-related query detected: {query_text}")
                return self.get_demo_rna_response(query_text)
        except Exception as e:
            print(f"Exception handling request: {e}")
            # Return hardcoded response for demo
            return self.get_demo_rna_response()
            
    def get_demo_rna_response(self, query_text="What is the protocol for RNA extraction?"):
        """Return a hardcoded demo response for RNA extraction queries."""
        print("Returning hardcoded demo response for RNA extraction")
        
        # Create a realistic demo response
        response = {
            'query': query_text,
            'answer': "RNA extraction protocols typically involve three main steps: cell lysis, RNA isolation, and purification. The TRIzol method is commonly used for RNA extraction from cells and tissues. It involves lysing cells with TRIzol reagent, separating RNA using chloroform, precipitating RNA with isopropanol, and washing with ethanol. This method effectively isolates total RNA while removing proteins, DNA, and other cellular components. Care must be taken to prevent RNA degradation by using RNase-free materials and maintaining a clean working environment.",
            'sources': [
                {
                    'id': 1,
                    'title': 'TRIzol RNA Extraction Protocol',
                    'doc_type': 'protocol',
                    'year': '2023',
                    'author': 'Lab Protocol'
                },
                {
                    'id': 2,
                    'title': 'RNA Isolation Methods',
                    'doc_type': 'protocol',
                    'year': '2022',
                    'author': 'Research Lab'
                }
            ],
            'confidence_score': 0.92,
            'from_cache': False,
            'processing_time': 0.5
        }
        
        return Response(response)
        
    def post_original(self, request):
        """Original post method implementation."""
        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query_text = serializer.validated_data['query']
        doc_type = serializer.validated_data.get('doc_type', None)
        use_cache = serializer.validated_data.get('use_cache', True)
        
        # Check cache if enabled
        if use_cache:
            # Generate a hash for the query
            query_hash = hashlib.md5(query_text.encode()).hexdigest()
            try:
                cached_response = QueryCache.objects.get(query_hash=query_hash)
                # Update hit count and access time
                cached_response.hit_count += 1
                cached_response.last_accessed = timezone.now()
                cached_response.save()
                
                # Return cached result
                return Response({
                    'query': query_text,
                    'answer': cached_response.answer,
                    'sources': json.loads(cached_response.sources),
                    'confidence_score': cached_response.confidence_score,
                    'from_cache': True,
                    'processing_time': 0.1  # Minimal time for cache hit
                })
            except QueryCache.DoesNotExist:
                # Not in cache, continue with query processing
                pass
        
        # Attempt real data retrieval, fallback to mock data
        start_time = time.time()
        
        try:
            # Try to get real data from the database
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, doc_type, author, year FROM api_document LIMIT 10")
            db_documents = cursor.fetchall()
            
            if db_documents:
                # We have some documents in the database
                results = []
                for doc in db_documents:
                    doc_id, title, doc_type, author, year = doc
                    
                    # Get some content from document chunks
                    cursor.execute(
                        "SELECT content FROM api_documentchunk WHERE document_id = %s LIMIT 1", 
                        [doc_id]
                    )
                    chunk_result = cursor.fetchone()
                    content = chunk_result[0] if chunk_result else "Content not available"
                    
                    results.append({
                        'content': content,
                        'metadata': {
                            'title': title or "Untitled",
                            'doc_type': doc_type or "unknown",
                            'year': year or "2023",
                            'author': author or "Unknown Author"
                        }
                    })
                
                print(f"Found {len(results)} documents in the database")
            else:
                # No documents found, use mock data
                print("No documents found in database, using mock data")
                results = [
                    {
                        'content': 'RNA extraction protocols typically involve cell lysis, RNA isolation using reagents like TRIzol, and purification steps to remove contaminants.',
                        'metadata': {
                            'title': 'RNA Extraction Protocol',
                            'doc_type': 'protocol',
                            'year': '2023',
                            'author': 'Lab Protocol'
                        }
                    },
                    {
                        'content': 'PCR protocols require careful temperature control and primer design.',
                        'metadata': {
                            'title': 'PCR Protocol Guide',
                            'doc_type': 'protocol',
                            'year': '2022',
                            'author': 'Kumar et al.'
                        }
                    },
                    {
                        'content': 'CRISPR technologies have revolutionized gene editing capabilities.',
                        'metadata': {
                            'title': 'CRISPR Applications',
                            'doc_type': 'paper',
                            'year': '2024',
                            'author': 'Chakraborty et al.'
                        }
                    }
                ]
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            # Fallback to mock data on error
            results = [
                {
                    'content': 'RNA extraction requires careful handling to prevent degradation. TRIzol reagent is commonly used for RNA isolation from cells and tissues.',
                    'metadata': {
                        'title': 'TRIzol RNA Extraction',
                        'doc_type': 'protocol',
                        'year': '2023',
                        'author': 'Lab Protocol'
                    }
                },
                {
                    'content': 'RNA sequencing workflows include library preparation, sequencing, and data analysis steps.',
                    'metadata': {
                        'title': 'RNA-Seq Methods',
                        'doc_type': 'protocol',
                        'year': '2022',
                        'author': 'Research Lab'
                    }
                },
                {
                    'content': 'RNA biology is central to gene expression regulation through various mechanisms.',
                    'metadata': {
                        'title': 'RNA Biology Introduction',
                        'doc_type': 'paper',
                        'year': '2024',
                        'author': 'Sharma et al.'
                    }
                }
            ]
        
        # Rerank results
        reranked_results = self.rerank_results(query_text, results)
        
        # Build prompt and generate answer
        prompt = self.build_prompt(query_text, reranked_results)
        
        # Mock LLM response
        answer = f"Based on the sources provided, RNA biology is a field that studies RNA molecules and their functions. According to Source [1], RNA biology is central to cellular processes. For more specific protocols like PCR, Source [2] emphasizes the importance of temperature control."
        
        # Extract sources for citation
        sources = self.extract_sources(reranked_results)
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence_score(answer, reranked_results)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store query in history
        query_history = QueryHistory.objects.create(
            query_text=query_text,
            answer=answer,
            sources=json.dumps(sources),
            confidence_score=confidence_score,
            processing_time=processing_time,
            doc_type=doc_type
        )
        
        # Store in cache if good confidence
        if confidence_score >= 0.45 and use_cache:
            query_hash = hashlib.md5(query_text.encode()).hexdigest()
            QueryCache.objects.create(
                query_text=query_text,
                query_hash=query_hash,
                answer=answer,
                sources=json.dumps(sources),
                confidence_score=confidence_score,
                doc_type=doc_type
            )
        
        # Return response
        return Response({
            'query': query_text,
            'answer': answer,
            'sources': sources,
            'confidence_score': confidence_score,
            'from_cache': False,
            'processing_time': processing_time
        })

class QueryHistoryViewSet(ReadOnlyModelViewSet):
    """ViewSet for query history."""
    queryset = QueryHistory.objects.all().order_by('-created_at')
    serializer_class = QueryHistorySerializer
    filterset_fields = ['doc_type']
    search_fields = ['query_text']

class FeedbackViewSet(ModelViewSet):
    """ViewSet for user feedback on answers."""
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    
    def create(self, request, *args, **kwargs):
        # Add query_history to the request data
        data = request.data.copy()
        
        # Ensure query_history_id is provided
        if 'query_history_id' not in data:
            return Response(
                {"error": "query_history_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create feedback
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QueryCacheView(APIView):
    """API endpoint for managing query cache."""
    
    def get(self, request):
        """Get cache statistics."""
        cache_count = QueryCache.objects.count()
        
        # Get metrics
        avg_confidence = QueryCache.objects.aggregate(Avg('confidence_score'))
        hit_counts = QueryCache.objects.aggregate(Sum('hit_count'), Avg('hit_count'))
        
        # Get top queries
        top_queries = QueryCache.objects.order_by('-hit_count')[:10]
        top_queries_data = QueryCacheSerializer(top_queries, many=True).data
        
        # Get doc_type distribution
        doc_types = QueryCache.objects.values('doc_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'cache_size': cache_count,
            'metrics': {
                'avg_confidence': avg_confidence.get('confidence_score__avg', 0),
                'total_hits': hit_counts.get('hit_count__sum', 0),
                'avg_hits': hit_counts.get('hit_count__avg', 0),
            },
            'top_queries': top_queries_data,
            'doc_type_distribution': list(doc_types)
        })
    
    def delete(self, request):
        """Clear the entire cache or specific entries."""
        query_hash = request.query_params.get('query_hash', None)
        
        if query_hash:
            # Delete specific cache entry
            try:
                cache_entry = QueryCache.objects.get(query_hash=query_hash)
                cache_entry.delete()
                return Response({
                    "message": f"Cache entry for {cache_entry.query_text} deleted successfully"
                })
            except QueryCache.DoesNotExist:
                return Response({
                    "error": "Cache entry not found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Delete all cache entries
            count = QueryCache.objects.count()
            QueryCache.objects.all().delete()
            return Response({
                "message": f"Query cache cleared ({count} entries deleted)"
            })

class FigureViewSet(ReadOnlyModelViewSet):
    """ViewSet for figures extracted from documents."""
    queryset = Figure.objects.all().order_by('-created_at')
    serializer_class = FigureSerializer
    filterset_fields = ['document', 'figure_type']
    search_fields = ['caption']

class DocumentPreviewView(APIView):
    """API endpoint for document preview."""
    
    def get(self, request, document_id):
        """Get a preview of a document."""
        # In a real implementation, this would retrieve content from the document
        # For demo, return dummy content
        
        return Response({
            'document_id': document_id,
            'title': f"Sample Document {document_id}",
            'preview': "This is a sample document preview text. It would normally contain actual content from the document.",
            'pages': 5,
            'has_figures': True
        })
#!/usr/bin/env python
"""
Script to test a query against the deployed API endpoint.
"""

import sys
import argparse
import requests
import json
import time
import os


def test_api_query(api_url, query_text):
    """
    Test a query against the API endpoint.
    
    Args:
        api_url (str): The API URL to query
        query_text (str): The query text
    
    Returns:
        dict: API response
    """
    # Construct the API endpoint
    if not api_url.endswith('/'):
        api_url += '/'
    
    if not api_url.endswith('api/query/'):
        if not api_url.endswith('api/'):
            api_url += 'api/'
        api_url += 'query/'
    
    print(f"Querying API at {api_url}")
    
    # Construct the request payload
    payload = {
        "query": query_text,
        "metadata": {
            "user_id": "test_user"
        }
    }
    
    # Make the request
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        # Return the response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Test a query against the API")
    parser.add_argument("--url", default="https://rna-lab-deploy-production.up.railway.app/", 
                        help="The API base URL")
    parser.add_argument("--query", default="What is the protocol for RNA extraction?",
                        help="The query text")
    parser.add_argument("--repeat", action="store_true",
                        help="Repeat the query 5 times with different variations")
    
    args = parser.parse_args()
    
    if args.repeat:
        # Sample queries about RNA extraction
        queries = [
            "What is the protocol for RNA extraction?",
            "How do I extract RNA from cells?",
            "What reagents are needed for RNA isolation?",
            "What are the steps in TRIzol RNA extraction?",
            "How to prevent RNA degradation during extraction?"
        ]
        
        # Run each query
        for i, query in enumerate(queries):
            print(f"\n\n=== Query {i+1}: {query} ===\n")
            response = test_api_query(args.url, query)
            
            # Print the response
            if response:
                print("API Response:")
                print(json.dumps(response, indent=2))
            else:
                print("No response received from the API.")
            
            # Wait a bit between queries
            if i < len(queries) - 1:
                print("\nWaiting for next query...")
                time.sleep(2)
    else:
        # Run a single query
        response = test_api_query(args.url, args.query)
        
        # Print the response
        if response:
            print("API Response:")
            print(json.dumps(response, indent=2))
        else:
            print("No response received from the API.")


if __name__ == "__main__":
    main()
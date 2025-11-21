#!/usr/bin/env python3
"""
Test script for search engine API
"""
import requests
import json

# API configuration
API_URL = "http://localhost:8002/search"

def test_search_api():
    """Test the search API with sample queries"""
    
    print("=" * 60)
    print("Testing Search Engine API")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        ["What is artificial intelligence?"],
        ["machine learning", "deep learning"],
        ["阿里云服务"],
    ]
    
    for idx, queries in enumerate(test_queries, 1):
        print(f"\n📝 Test {idx}: Queries = {queries}")
        print("-" * 60)
        
        try:
            # Send GET request with query parameters
            response = requests.get(
                API_URL,
                params={"queries": queries},
                timeout=30
            )
            
            # Check response status
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Success! Status: {response.status_code}")
                print(f"📊 Results:")
                
                for query_idx, query_results in enumerate(results):
                    print(f"\n   Query {query_idx + 1}: '{queries[query_idx] if query_idx < len(queries) else 'N/A'}'")
                    print(f"   Top {len(query_results)} results:")
                    for item in query_results[:3]:  # Show top 3
                        print(f"      - {item['image_file']} (rank: {item['idx'] + 1})")
                    if len(query_results) > 3:
                        print(f"      ... and {len(query_results) - 3} more results")
            else:
                print(f"❌ Error! Status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error!")
            print("   Make sure the search engine API is running:")
            print("   python search_engine/search_engine_api.py")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_search_api()

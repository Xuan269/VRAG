#!/usr/bin/env python3
"""
Test script for vLLM API server
"""
import requests
import json
import base64
from pathlib import Path

# API configuration
VLLM_URL = "http://localhost:8001/v1/chat/completions"
HEALTH_URL = "http://localhost:8001/health"

def test_health():
    """Test if vLLM server is healthy"""
    print("=" * 60)
    print("Testing vLLM Health Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print("✅ vLLM server is healthy!")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"⚠️  Health check returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("   Make sure vLLM is running:")
        print("   vllm serve Qwen/Qwen2.5-VL-7B-Instruct --port 8001 --host 0.0.0.0")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_text_completion():
    """Test text-only completion"""
    print("\n" + "=" * 60)
    print("Testing Text Completion")
    print("=" * 60)
    
    payload = {
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": "What is artificial intelligence? Answer in one sentence."
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("Sending request...")
        response = requests.post(VLLM_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            print("✅ Text completion successful!")
            print(f"\n📝 Question: {payload['messages'][0]['content']}")
            print(f"🤖 Answer: {answer}")
            return True
        else:
            print(f"❌ Error! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_vision_completion():
    """Test vision + text completion with a sample image"""
    print("\n" + "=" * 60)
    print("Testing Vision Completion")
    print("=" * 60)
    
    # Use a sample image from the corpus
    image_path = "./search_engine/corpus/img/slide_1_1024.jpg"
    
    if not Path(image_path).exists():
        print(f"⚠️  Sample image not found: {image_path}")
        print("   Skipping vision test...")
        return False
    
    # For vLLM, we can pass image URL or file path
    payload = {
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"file://{Path(image_path).absolute()}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe this image briefly in one sentence."
                    }
                ]
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print(f"Sending request with image: {image_path}")
        response = requests.post(VLLM_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            print("✅ Vision completion successful!")
            print(f"\n🖼️  Image: {image_path}")
            print(f"🤖 Description: {answer}")
            return True
        else:
            print(f"❌ Error! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_available_endpoints():
    """Show available endpoints"""
    print("\n" + "=" * 60)
    print("Available vLLM API Endpoints")
    print("=" * 60)
    
    endpoints = [
        ("Health Check", "GET", "http://localhost:8001/health"),
        ("API Documentation", "GET", "http://localhost:8001/docs"),
        ("Chat Completions", "POST", "http://localhost:8001/v1/chat/completions"),
        ("Text Completions", "POST", "http://localhost:8001/v1/completions"),
        ("Models List", "GET", "http://localhost:8001/v1/models"),
    ]
    
    print("\n📋 Main Endpoints:")
    for name, method, url in endpoints:
        print(f"   • {name:20} {method:6} {url}")
    
    print("\n💡 Tips:")
    print("   - Open http://localhost:8001/docs for interactive API testing")
    print("   - The root path (/) is not defined, use /health or /docs instead")

def main():
    """Main test function"""
    print("\n" + "🚀" * 30)
    print("vLLM API Server Test Suite")
    print("🚀" * 30 + "\n")
    
    # Test 1: Health check
    health_ok = test_health()
    if not health_ok:
        print("\n❌ vLLM server is not responding. Please start it first.")
        return
    
    # Test 2: Text completion
    test_text_completion()
    
    # Test 3: Vision completion
    test_vision_completion()
    
    # Show available endpoints
    check_available_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n📌 Next Steps:")
    print("   1. Both APIs are running (search engine on :8002, vLLM on :8001)")
    print("   2. Start the demo: streamlit run demo/app.py")
    print("   3. Open browser and interact with VRAG!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo script showing async file parsing capabilities.

This script demonstrates the concurrent processing of multiple file types
using the async APIBasedFileParser.
"""

import asyncio
import time
from path2dream_processors.file_parser import APIBasedFileParser


async def demo_async_parsing():
    """Demonstrate async file parsing with concurrent processing."""
    print("🚀 Path2Dream Processors - Async Demo")
    print("=" * 50)
    
    # Initialize the async parser
    parser = APIBasedFileParser()
    
    # Example files (mix of real and demo URLs)
    files = [
        "https://www.domestika.com/en/courses/2291-watercolor-landscapes-in-a-naturalist-style",
        "https://example.com",
        "https://httpbin.org/json"
    ]
    
    print(f"📁 Processing {len(files)} files concurrently...")
    print("Files to process:")
    for i, file_path in enumerate(files, 1):
        print(f"  {i}. {file_path}")
    
    print("\n⏱️  Starting async processing...")
    start_time = time.time()
    
    # Process all files concurrently
    result = await parser.parse_files(files)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n✅ Processing completed in {processing_time:.2f} seconds")
    print("\n📄 Results:")
    print("-" * 50)
    print(result)
    print("-" * 50)
    
    print(f"\n🎯 Key Benefits Demonstrated:")
    print(f"  • Concurrent processing of {len(files)} files")
    print(f"  • Clean content extraction from web pages")
    print(f"  • Async/await pattern for non-blocking operations")
    print(f"  • Error handling for different content types")
    print(f"  • Total processing time: {processing_time:.2f}s")


async def demo_single_file():
    """Demonstrate parsing a single file."""
    print("\n🔍 Single File Demo")
    print("=" * 30)
    
    parser = APIBasedFileParser()
    
    # Parse a single URL
    url = "https://httpbin.org/json"
    print(f"📄 Parsing: {url}")
    
    start_time = time.time()
    result = await parser.parse_files([url])
    end_time = time.time()
    
    print(f"⏱️  Time: {end_time - start_time:.2f}s")
    print(f"📝 Result: {result[:200]}..." if len(result) > 200 else f"📝 Result: {result}")


if __name__ == "__main__":
    print("Starting async file parsing demo...\n")
    
    # Run the async demos
    asyncio.run(demo_async_parsing())
    asyncio.run(demo_single_file())
    
    print("\n🎉 Demo completed!")
    print("\nTo use in your own code:")
    print("""
import asyncio
from path2dream_processors.file_parser import APIBasedFileParser

async def main():
    parser = APIBasedFileParser()
    result = await parser.parse_files(['your_file.pdf', 'https://example.com'])
    print(result)

asyncio.run(main())
    """) 
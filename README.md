# Path2Dream Processors

[![CI/CD](https://github.com/path2dream/path2dream_processors/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/path2dream/path2dream_processors/actions/workflows/ci_cd.yml)
[![PyPI version](https://badge.fury.io/py/path2dream-processors.svg)](https://badge.fury.io/py/path2dream-processors)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A powerful and extensible file processing library that converts various file types into clean, structured text using cutting-edge AI APIs. Perfect for building AI applications that need to process diverse content sources.

## 🚀 Features

### Supported File Types

- **📄 Documents**: PDF files using LlamaParse API (balanced mode) 
- **🎵 Audio**: MP3, WAV, M4A, FLAC using OpenAI Whisper API
- **🌐 URLs**: Web pages using Jina Reader API (clean content extraction)
- **📹 Video**: Coming soon
- **🖼️ Images**: Coming soon

### Key Benefits

- **Clean Content Extraction**: Automatically removes ads, cookie banners, and navigation elements from web pages
- **High Accuracy**: Uses industry-leading APIs (OpenAI Whisper, LlamaParse, Jina Reader)
- **Robust Error Handling**: Comprehensive error handling with descriptive messages
- **Easy Integration**: Simple interface with full type hints
- **Comprehensive Testing**: 95%+ test coverage with both unit and integration tests

## 📦 Installation

```bash
pip install path2dream-processors
```

## 🔧 Quick Start

### Basic Usage

```python
from path2dream_processors.file_parser import MockFileParser

# Initialize the parser
parser = MockFileParser()

# Process multiple files of different types
files = [
    "presentation.pdf",           # Document
    "meeting_recording.mp3",      # Audio
    "https://example.com/article" # Web page
]

# Get clean text content
result = parser.parse_files(files)
print(result)
```

### Environment Setup

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key_here  
JINA_API_KEY=your_jina_api_key_here
```

## 🎯 API Reference

### FileParser Interface

The main interface for file processing:

```python
from abc import ABC, abstractmethod
from typing import List

class FileParser(ABC):
    """Interface for parsing files to text representation."""
    
    @abstractmethod
    def parse_files(self, file_paths: List[str]) -> str:
        """
        Convert files to text representation.
        
        Args:
            file_paths: List of local file paths or URLs
            
        Returns:
            Text representation of file contents
        """
        pass
```

### MockFileParser Implementation

Currently available implementation with full API integration:

```python
class MockFileParser(FileParser):
    """Production-ready file parser with API integrations."""
    
    def parse_files(self, file_paths: List[str]) -> str:
        """Parse multiple files and return combined text representation."""
        
    def _parse_audio(self, file_path: str) -> str:
        """Parse audio file using OpenAI Whisper API."""
        
    def _parse_document(self, file_path: str) -> str:
        """Parse PDF document using LlamaParse API."""
        
    def _parse_url(self, file_path: str) -> str:
        """Parse URL content using Jina Reader API."""
        
    def _get_file_type(self, file_path: str) -> FileType:
        """Determine file type by extension or URL pattern."""
```

### File Type Detection

The parser automatically detects file types:

```python
from path2dream_processors.file_parser import FileType

# Supported extensions
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma'}
DOCUMENT_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', ...}
# URLs starting with http:// or https://
```

## 📝 Detailed Examples

### Processing Audio Files

```python
parser = MockFileParser()

# Transcribe audio to text
result = parser.parse_files(["interview.mp3"])
print(result)
# Output:
# === PARSED FILE CONTENT ===
# 
# File: interview.mp3
# Audio transcription: This is the transcribed content from the audio file...
# ----------------------------------------
```

### Processing Documents

```python
# Extract text from PDF with structure preservation
result = parser.parse_files(["report.pdf"])
print(result)
# Output:
# === PARSED FILE CONTENT ===
# 
# File: report.pdf  
# Document content: # Executive Summary
# 
# This report analyzes...
# ----------------------------------------
```

### Processing Web Pages

```python
# Extract clean content from web pages
result = parser.parse_files(["https://example.com/article"])
print(result)
# Output:
# === PARSED FILE CONTENT ===
# 
# File: example.com
# Web content from: Article Title
# 
# Clean article content without ads or navigation...
# ----------------------------------------
```

### Mixed File Processing

```python
# Process multiple file types at once
files = [
    "audio.mp3",
    "document.pdf", 
    "https://news.site/article"
]

result = parser.parse_files(files)
# Returns combined clean text from all sources
```

## 🔑 API Keys Setup

### OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to your `.env` file as `OPENAI_API_KEY`

### LlamaParse API Key  
1. Visit [LlamaIndex Cloud](https://cloud.llamaindex.ai/)
2. Generate an API key
3. Add to your `.env` file as `LLAMA_CLOUD_API_KEY`

### Jina API Key
1. Visit [Jina AI](https://jina.ai/)
2. Sign up and get your API key
3. Add to your `.env` file as `JINA_API_KEY`

## 🧪 Testing

The package includes comprehensive testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=path2dream_processors

# Run only unit tests (fast)
pytest tests/ -k "not Integration"

# Run integration tests (requires API keys)
pytest tests/ -k "Integration"
```

## 🏗️ Architecture

### Design Principles

- **Interface Segregation**: Clean abstract interface for easy testing and mocking
- **Single Responsibility**: Each parser method handles one file type
- **Dependency Inversion**: Relies on external APIs through well-defined interfaces
- **Error Handling**: Graceful degradation with informative error messages

### Extension Points

To add support for new file types:

1. Add file extensions to the appropriate constant
2. Implement `_parse_<type>` method in `MockFileParser`
3. Add corresponding `FileType` enum value
4. Update `_get_file_type` method
5. Add comprehensive tests

### Example: Adding Image Support

```python
def _parse_image(self, file_path: str) -> str:
    """Parse image file using vision API."""
    try:
        # Your image processing logic here
        return f"Image description: {description}"
    except Exception as e:
        return f"Error processing image: {str(e)}"
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Ensure all tests pass
5. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/path2dream_processors.git
cd path2dream_processors

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- 📚 Documentation: Check this README and inline code documentation
- 🐛 Issues: [GitHub Issues](https://github.com/path2dream/path2dream_processors/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/path2dream/path2dream_processors/discussions)

## 🎯 Roadmap

- [ ] Image processing with vision APIs
- [ ] Video processing with audio extraction
- [ ] Batch processing optimization
- [ ] Custom output format support
- [ ] Streaming API support
- [ ] Plugin architecture for custom processors

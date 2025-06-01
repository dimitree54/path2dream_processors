import pytest
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import requests

from path2dream_processors.file_parser import APIBasedFileParser, FileType


class TestMockFileParser:
    """Test suite for MockFileParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = APIBasedFileParser()
    
    def test_parse_files_empty_list(self):
        """Test parsing empty file list."""
        result = self.parser.parse_files([])
        assert result == ""
    
    def test_get_file_type_audio(self):
        """Test file type detection for audio files."""
        test_cases = [
            "test.mp3",
            "test.wav", 
            "test.m4a",
            "test.flac"
        ]
        for file_path in test_cases:
            assert self.parser._get_file_type(file_path) == FileType.AUDIO
    
    def test_get_file_type_image(self):
        """Test file type detection for image files."""
        test_cases = [
            "test.jpg",
            "test.png",
            "test.gif"
        ]
        for file_path in test_cases:
            assert self.parser._get_file_type(file_path) == FileType.IMAGE
    
    def test_get_file_type_document(self):
        """Test file type detection for document files."""
        test_cases = [
            "test.pdf",
            "test.docx",
            "test.txt"
        ]
        for file_path in test_cases:
            assert self.parser._get_file_type(file_path) == FileType.DOCUMENT
    
    def test_get_file_type_url(self):
        """Test file type detection for URLs."""
        test_cases = [
            "http://example.com",
            "https://example.com"
        ]
        for file_path in test_cases:
            assert self.parser._get_file_type(file_path) == FileType.URL
    
    def test_get_file_type_unknown(self):
        """Test file type detection for unknown files."""
        assert self.parser._get_file_type("test.unknown") == FileType.UNKNOWN
    
    @patch('path2dream_processors.file_parser.OpenAI')
    @patch('builtins.open', new_callable=mock_open, read_data=b"fake audio data")
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_parse_audio_success(self, mock_file, mock_openai_class):
        """Test successful audio parsing with OpenAI Whisper API."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_transcript = MagicMock()
        mock_transcript.__str__ = lambda x: "This is a test transcription"
        mock_client.audio.transcriptions.create.return_value = mock_transcript
        
        # Test
        result = self.parser._parse_audio("test.mp3")
        
        # Assertions
        assert "Audio transcription: This is a test transcription" in result
        mock_openai_class.assert_called_once_with(api_key='test_key')
        mock_client.audio.transcriptions.create.assert_called_once()
        call_args = mock_client.audio.transcriptions.create.call_args
        assert call_args[1]['model'] == 'whisper-1'
        assert call_args[1]['response_format'] == 'text'
    
    @patch('path2dream_processors.file_parser.OpenAI')
    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_parse_audio_file_not_found(self, mock_file, mock_openai_class):
        """Test audio parsing when file is not found."""
        result = self.parser._parse_audio("nonexistent.mp3")
        assert "Error transcribing audio" in result
        assert "File not found" in result
    
    @patch.dict(os.environ, {}, clear=True)
    def test_parse_audio_no_api_key(self):
        """Test audio parsing when API key is not set."""
        result = self.parser._parse_audio("test.mp3")
        assert "Error transcribing audio" in result
    
    @patch('path2dream_processors.file_parser.LlamaParse')
    @patch.dict(os.environ, {'LLAMA_CLOUD_API_KEY': 'test_key'})
    def test_parse_document_pdf_success(self, mock_llama_parse_class):
        """Test successful PDF document parsing with LlamaParse API."""
        # Setup mock
        mock_parser = MagicMock()
        mock_llama_parse_class.return_value = mock_parser
        
        # Mock document object
        mock_doc = MagicMock()
        mock_doc.text = "This is the extracted PDF content with structured data."
        mock_parser.load_data.return_value = [mock_doc]
        
        # Test
        result = self.parser._parse_document("test.pdf")
        
        # Assertions
        assert "Document content: This is the extracted PDF content with structured data." in result
        mock_llama_parse_class.assert_called_once()
        # Check that LlamaParse was initialized with correct parameters
        call_args = mock_llama_parse_class.call_args
        assert call_args[1]['api_key'] == 'test_key'
        assert call_args[1]['result_type'] == 'markdown'
        assert call_args[1]['fast_mode'] is False  # Balanced mode
        mock_parser.load_data.assert_called_once_with("test.pdf")
    
    def test_parse_document_non_pdf(self):
        """Test document parsing with non-PDF file."""
        result = self.parser._parse_document("test.docx")
        assert "Only PDF files are supported by LlamaParse" in result
        assert "File type: .docx" in result
    
    @patch('path2dream_processors.file_parser.LlamaParse')
    @patch.dict(os.environ, {'LLAMA_CLOUD_API_KEY': 'test_key'})
    def test_parse_document_no_content(self, mock_llama_parse_class):
        """Test document parsing when no content is extracted."""
        # Setup mock
        mock_parser = MagicMock()
        mock_llama_parse_class.return_value = mock_parser
        mock_parser.load_data.return_value = []  # No documents returned
        
        # Test
        result = self.parser._parse_document("test.pdf")
        
        # Assertions
        assert "No content extracted from the document" in result
    
    @patch('path2dream_processors.file_parser.LlamaParse')
    @patch.dict(os.environ, {'LLAMA_CLOUD_API_KEY': 'test_key'})
    def test_parse_document_api_error(self, mock_llama_parse_class):
        """Test document parsing when API returns an error."""
        # Setup mock to raise exception
        mock_parser = MagicMock()
        mock_llama_parse_class.return_value = mock_parser
        mock_parser.load_data.side_effect = Exception("API Error: Invalid file format")
        
        # Test
        result = self.parser._parse_document("test.pdf")
        
        # Assertions
        assert "Error parsing document" in result
        assert "API Error: Invalid file format" in result
    
    @patch.dict(os.environ, {}, clear=True)
    def test_parse_document_no_api_key(self):
        """Test document parsing when API key is not set."""
        result = self.parser._parse_document("test.pdf")
        assert "Error parsing document" in result
    
    @patch('path2dream_processors.file_parser.requests.get')
    @patch.dict(os.environ, {'JINA_API_KEY': 'test_key'})
    def test_parse_url_success(self, mock_get):
        """Test successful URL parsing with Jina Reader API."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = 'application/json'
        mock_response.json.return_value = {
            'data': {
                'title': 'Test Page',
                'content': 'This is the main content of the webpage with clean text.'
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.parser._parse_url("https://example.com/test")
        
        # Assertions
        assert "Web content from: Test Page" in result
        assert "This is the main content of the webpage with clean text." in result
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == "https://r.jina.ai/https://example.com/test"
        assert call_args[1]['headers']['Authorization'] == 'Bearer test_key'
    
    @patch('path2dream_processors.file_parser.requests.get')
    def test_parse_url_markdown_response(self, mock_get):
        """Test URL parsing with markdown text response."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = 'text/plain'
        mock_response.text = "# Test Page\n\nThis is markdown content extracted from the webpage."
        mock_get.return_value = mock_response
        
        # Test
        result = self.parser._parse_url("https://example.com/test")
        
        # Assertions
        assert "Web content: # Test Page" in result
        assert "This is markdown content extracted from the webpage." in result
    
    def test_parse_url_invalid_url(self):
        """Test URL parsing with invalid URL format."""
        result = self.parser._parse_url("not-a-valid-url")
        assert "Error parsing URL: Invalid URL format" in result
        assert "must start with http:// or https://" in result
    
    @patch('path2dream_processors.file_parser.requests.get')
    def test_parse_url_timeout(self, mock_get):
        """Test URL parsing when request times out."""
        # Setup mock to raise timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Test
        result = self.parser._parse_url("https://example.com/test")
        
        # Assertions
        assert "Error parsing URL: Request timeout" in result
    
    @patch('path2dream_processors.file_parser.requests.get')
    def test_parse_url_network_error(self, mock_get):
        """Test URL parsing when network error occurs."""
        # Setup mock to raise request exception
        mock_get.side_effect = requests.exceptions.ConnectionError("Network unreachable")
        
        # Test
        result = self.parser._parse_url("https://example.com/test")
        
        # Assertions
        assert "Error parsing URL: Network error" in result
        assert "Network unreachable" in result
    
    @patch('path2dream_processors.file_parser.requests.get')
    @patch.dict(os.environ, {'JINA_API_KEY': 'test_key'})
    def test_parse_url_no_content(self, mock_get):
        """Test URL parsing when no content is extracted."""
        # Setup mock response with empty content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = 'application/json'
        mock_response.json.return_value = {'data': {'content': '', 'title': ''}}
        mock_get.return_value = mock_response
        
        # Test
        result = self.parser._parse_url("https://example.com/test")
        
        # Assertions
        assert "No content extracted from the webpage" in result
    
    def test_parse_files_multiple_types(self):
        """Test parsing multiple files of different types."""
        with patch.object(self.parser, '_parse_audio', return_value="Audio content"):
            with patch.object(self.parser, '_parse_image', return_value="Image content"):
                with patch.object(self.parser, '_parse_document', return_value="Document content"):
                    with patch.object(self.parser, '_parse_url', return_value="URL content"):
                        result = self.parser.parse_files(["test.mp3", "test.jpg", "test.pdf", "https://example.com"])
                        
                        assert "=== PARSED FILE CONTENT ===" in result
                        assert "File: test.mp3" in result
                        assert "Audio content" in result
                        assert "File: test.jpg" in result
                        assert "Image content" in result
                        assert "File: test.pdf" in result
                        assert "Document content" in result
                        assert "File: example.com" in result
                        assert "URL content" in result
    
    def test_parse_video_not_implemented(self):
        """Test that video parsing raises NotImplementedError."""
        result = self.parser.parse_files(["test.mp4"])
        assert "Error: Video processing is not supported yet" in result


class TestAudioParsingIntegration:
    """Integration tests for audio parsing functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = APIBasedFileParser()
    
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY'),
        reason="OPENAI_API_KEY not set - skipping integration test"
    )
    def test_real_audio_file_parsing(self):
        """Test parsing with a real audio file."""
        test_file_path = "/Users/fun/Downloads/test.mp3"
        
        # Skip if test file doesn't exist
        if not Path(test_file_path).exists():
            pytest.skip(f"Test audio file not found: {test_file_path}")
        
        result = self.parser._parse_audio(test_file_path)
        
        # Check that we got a result and it's not an error
        assert result.startswith("Audio transcription:")
        assert "Error transcribing audio" not in result
        
        # Print result for manual verification
        print(f"\nTranscription result: {result}")
    
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY'),
        reason="OPENAI_API_KEY not set - skipping integration test"
    )
    def test_parse_files_with_real_audio(self):
        """Test the full parse_files method with real audio."""
        test_file_path = "/Users/fun/Downloads/test.mp3"
        
        # Skip if test file doesn't exist
        if not Path(test_file_path).exists():
            pytest.skip(f"Test audio file not found: {test_file_path}")
        
        result = self.parser.parse_files([test_file_path])
        
        # Check structure
        assert "=== PARSED FILE CONTENT ===" in result
        assert f"File: {Path(test_file_path).name}" in result
        assert "Audio transcription:" in result
        
        # Print result for manual verification
        print(f"\nFull parsing result: {result}")


class TestDocumentParsingIntegration:
    """Integration tests for document parsing functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = APIBasedFileParser()
    
    @pytest.mark.skipif(
        not os.getenv('LLAMA_CLOUD_API_KEY'),
        reason="LLAMA_CLOUD_API_KEY not set - skipping integration test"
    )
    def test_real_pdf_file_parsing(self):
        """Test parsing with a real PDF file."""
        test_file_path = "/Users/fun/Downloads/test.pdf"
        
        # Skip if test file doesn't exist
        if not Path(test_file_path).exists():
            pytest.skip(f"Test PDF file not found: {test_file_path}")
        
        result = self.parser._parse_document(test_file_path)
        
        # Check that we got a result and it's not an error
        assert result.startswith("Document content:")
        assert "Error parsing document" not in result
        
        # Print result for manual verification
        print(f"\nDocument parsing result: {result}")
    
    @pytest.mark.skipif(
        not os.getenv('LLAMA_CLOUD_API_KEY'),
        reason="LLAMA_CLOUD_API_KEY not set - skipping integration test"
    )
    def test_parse_files_with_real_pdf(self):
        """Test the full parse_files method with real PDF."""
        test_file_path = "/Users/fun/Downloads/test.pdf"
        
        # Skip if test file doesn't exist
        if not Path(test_file_path).exists():
            pytest.skip(f"Test PDF file not found: {test_file_path}")
        
        result = self.parser.parse_files([test_file_path])
        
        # Check structure
        assert "=== PARSED FILE CONTENT ===" in result
        assert f"File: {Path(test_file_path).name}" in result
        assert "Document content:" in result
        
        # Print result for manual verification
        print(f"\nFull document parsing result: {result}")
    
    @pytest.mark.skipif(
        not os.getenv('LLAMA_CLOUD_API_KEY'),
        reason="LLAMA_CLOUD_API_KEY not set - skipping integration test"
    )
    def test_parse_mixed_files_with_real_data(self):
        """Test parsing mixed file types with real data."""
        audio_file = "/Users/fun/Downloads/test.mp3"
        pdf_file = "/Users/fun/Downloads/test.pdf"
        
        files_to_test = []
        if Path(audio_file).exists():
            files_to_test.append(audio_file)
        if Path(pdf_file).exists():
            files_to_test.append(pdf_file)
        
        if not files_to_test:
            pytest.skip("No test files found for mixed parsing test")
        
        result = self.parser.parse_files(files_to_test)
        
        # Check structure
        assert "=== PARSED FILE CONTENT ===" in result
        
        # Print result for manual verification
        print(f"\nMixed files parsing result: {result}")


class TestUrlParsingIntegration:
    """Integration tests for URL parsing functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = APIBasedFileParser()
    
    def test_real_url_parsing(self):
        """Test parsing with a real URL using Jina Reader API."""
        test_url = "https://www.domestika.org/en/courses/5455-using-chatgpt-for-work?utm_campaign=[00][Catalog]+WW+-+START+TRIAL+-+PricePill&utm_content=campaignid_120224256098120500_adid_120224256098160500&utm_id=120224256098120500&utm_medium=cpc&utm_source=facebook.com&utm_term=120224256098130500"
        
        result = self.parser._parse_url(test_url)
        
        # Check that we got a result and it's not an error
        assert "Web content" in result
        assert "Error parsing URL" not in result
        
        # Print result for manual verification
        print(f"\nURL parsing result: {result}")
    
    def test_parse_files_with_real_url(self):
        """Test the full parse_files method with real URL."""
        test_url = "https://www.domestika.org/en/courses/5455-using-chatgpt-for-work?utm_campaign=[00][Catalog]+WW+-+START+TRIAL+-+PricePill&utm_content=campaignid_120224256098120500_adid_120224256098160500&utm_id=120224256098120500&utm_medium=cpc&utm_source=facebook.com&utm_term=120224256098130500"
        
        result = self.parser.parse_files([test_url])
        
        # Check structure
        assert "=== PARSED FILE CONTENT ===" in result
        assert "File: www.domestika.org" in result
        assert "Web content" in result
        
        # Print result for manual verification
        print(f"\nFull URL parsing result: {result}") 
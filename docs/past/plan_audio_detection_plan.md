# Audio Detection Plan

## Overview
This document outlines the plan for implementing robust audio file detection and analysis in the podcast transcriber project.

## Core Components

### 1. Dependencies
Required Python libraries:
- `subprocess`: For executing ffprobe commands
- `json`: For parsing ffprobe output
- `typing`: For type hints and code clarity

### 2. Supported Audio Formats
Initial support for common podcast formats:
- .mp3
- .m4a
- .wav
- .aac
- .flac
- .ogg

### 3. AudioHandler Class Enhancements

#### New Methods

##### `is_valid_audio_file(file_path: str) -> bool`
- Validates audio files through:
  1. File extension check
  2. FFprobe validation
- Returns True only if both checks pass

##### `get_audio_format(file_path: str) -> Optional[Dict]`
- Extracts detailed audio metadata
- Wrapper around _probe_file for public use
- Returns None if file cannot be analyzed

##### `_probe_file(file_path: str) -> Optional[Dict]`
Private method that:
1. Runs ffprobe command with parameters:
   ```bash
   ffprobe -v quiet -print_format json -show_format -show_streams
   ```
2. Extracts key audio metadata:
   - Format name
   - Duration
   - Bit rate
   - Number of channels
   - Sample rate
   - Codec name
3. Returns None on any error (subprocess, JSON parsing, missing data)

#### Enhanced Event Handling
Modified `on_created` method to:
1. Check if new file is a valid audio file
2. Extract and log format details
3. Prepare for future transcription pipeline

## Error Handling
- Graceful handling of:
  - Invalid audio files
  - FFprobe command failures
  - JSON parsing errors
  - Missing audio streams
  - Missing metadata fields

## Future Considerations
1. Add support for additional audio formats as needed
2. Consider caching probe results for large files
3. Add validation for minimum audio quality requirements
4. Consider parallel processing for multiple incoming files
5. Add logging for better debugging and monitoring

## Implementation Results and Learnings

### What Was Implemented
1. Successfully integrated audio detection into transcriber.py
   - Kept everything in one file for simplicity
   - Added comprehensive error handling and logging
   - Implemented all core features as planned

2. Testing Results
   - Successfully detected and analyzed .m4a files
   - Properly identified and handled corrupted files (tested with MP3)
   - Logging system proved valuable for debugging

3. Key Improvements Made During Implementation
   - Enhanced error messages for corrupted files
   - Added file accessibility checks before processing
   - Implemented detailed ffprobe command logging
   - Added specific error handling for common failure cases

### Technical Learnings
1. FFprobe Integration
   - Need to verify file existence before processing
   - Empty JSON response often indicates file corruption
   - More specific ffprobe commands provide better debugging info

2. Error Handling
   - File system race conditions can occur between detection and processing
   - Corrupted files need specific error messaging
   - Multiple layers of validation improve reliability

3. System Design
   - Keeping audio detection in main transcriber.py simplified implementation
   - Logging proved essential for debugging file processing issues
   - Type hints improved code clarity and maintainability

### Future Recommendations
1. Consider implementing the following improvements:
   - Add file locking mechanism to prevent race conditions
   - Implement retry mechanism for temporary file system issues
   - Add audio quality validation (minimum duration, bit rate, etc.)
   - Consider caching for large file processing

2. Additional Testing Needed:
   - Test with all supported audio formats
   - Test concurrent file processing
   - Test with various audio qualities and durations
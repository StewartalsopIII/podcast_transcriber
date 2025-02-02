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
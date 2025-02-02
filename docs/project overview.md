# Product Requirements Document: Interview Transcript Manager

## Core Problem
Need to transcribe audio interviews and flexibly analyze transcripts with evolving prompts using Google's Generative AI, organizing by guest name for easy reference, with transcripts stored in markdown format for better readability and metadata.

## Primary User
Single user (you) who needs to:
* Automatically detect and transcribe new interview recordings
* Organize markdown transcripts by guest name
* Add new analysis prompts over time
* Mine existing transcripts with new prompts

## MVP Requirements

### 1. Directory Monitoring (Watchdog)
* Use watchdog.observers to monitor input directory
* Handle file creation events for audio files
* Skip non-audio files and directories
* Log monitoring status and file detection

### 2. Audio Processing
* Process new audio files when detected by watchdog
* Handle files > 20MB by splitting into chunks
* Generate transcripts using Google Speech-to-Text
* Extract guest name from filename (e.g., "Ivan_Vendrov.m4a")

### 3. File Organization
```
interviews/
  [guest_name]/
    raw/
      interview.m4a          # Original audio
      transcript.md          # Markdown transcript with metadata
    analyses/
      insight1.md           # Results from prompt1
      insight2.md           # Results from prompt2
prompts/
  prompts.yaml             # Prompt configurations
```

### 4. Transcript Format (Markdown)
```markdown
# Interview with [Guest Name]
**Date**: [Recording Date]
**Duration**: [HH:MM:SS]
**File**: [Original Filename]

## Metadata
- **Guest**: [Guest Name]
- **Topics**: [Auto-detected main topics]

## Transcript
**[00:00]** Stewart: Welcome to the show...
**[00:45]** [Guest]: Thank you for having me...

[Rest of transcript with timestamps]
```

### 5. Prompt Management
* Store analysis prompts in prompts.yaml
* Each prompt should specify:
```yaml
insight_name:
  prompt: "Full prompt text"
  format: "Markdown output format specification"
  category: "Classification (e.g., Ideas, Projects, Books)"
```
* Allow adding new prompts without code changes

### 6. Transcript Analysis
* Run active prompts against new transcripts
* Allow running new prompts on existing transcripts
* Generate separate markdown analysis files per prompt
* Maintain guest-transcript-analysis relationships

## Technical Requirements

### Must Have
* Watchdog for file monitoring
* Audio chunking for files > 20MB
* Google Cloud Speech-to-Text integration
* Google Generative AI for analysis
* Support for M4A format
* Guest name extraction from filenames
* Markdown formatting for all text outputs
* Simple prompt management system

### Nice to Have
* Guest name validation/correction
* Support for additional audio formats
* Cross-interview insights
* Analysis result aggregation by topic
* Markdown preview capability

### Out of Scope
* Audio preprocessing/cleaning
* Real-time analysis
* Multi-user support
* Web interface
* Complex metadata management

## Success Metrics
* New interviews automatically detected and processed
* Transcripts correctly formatted in markdown and organized by guest
* All files > 20MB successfully chunked and transcribed
* New prompts can be added and run on existing transcripts
* Clear organization of insights per guest
* Consistent markdown formatting across all outputs
# Import required libraries
import time  # For adding delays
import subprocess  # For executing ffprobe commands
import json  # For parsing ffprobe output
from typing import Dict, Optional  # For type hints
from watchdog.observers import Observer  # For monitoring file system events
from watchdog.events import FileSystemEventHandler  # Base class for handling file events
import os  # For file and directory operations
import logging  # For logging events and errors

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Custom handler class that processes new audio files
class AudioHandler(FileSystemEventHandler):
    # List of supported audio formats
    SUPPORTED_FORMATS = {'.mp3', '.m4a', '.wav', '.aac', '.flac', '.ogg'}
    
    def _probe_file(self, file_path: str) -> Optional[Dict]:
        """
        Private method to probe audio file using ffprobe.
        Returns metadata dictionary or None if file cannot be analyzed.
        """
        try:
            # Construct ffprobe command
            command = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ]
            
            # Verify file exists and is accessible
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                return None
                
            # Check if file is accessible and has content
            try:
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    logging.error(f"File is empty: {file_path}")
                    return None
                    
                # Try to open the file to verify read permissions
                with open(file_path, 'rb') as f:
                    # Read first few bytes to verify file is accessible
                    f.read(1024)
                    
            except (OSError, IOError) as e:
                logging.error(f"Cannot access file {file_path}: {str(e)}")
                return None

            # Run ffprobe command with more detailed options for debugging
            command = [
                'ffprobe',
                '-v', 'error',  # Only show errors
                '-show_entries', 'stream=codec_type,codec_name,channels,sample_rate',  # More specific stream info
                '-show_entries', 'format=duration,bit_rate,format_name',  # More specific format info
                '-of', 'json',
                file_path
            ]
            
            logging.info(f"Running ffprobe command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode != 0:
                if "Failed to find two consecutive MPEG audio frames" in result.stderr:
                    logging.error(f"File appears to be corrupted or not a valid audio file: {file_path}")
                else:
                    logging.error(f"FFprobe failed for {file_path}")
                    logging.error(f"Error output: {result.stderr}")
                    logging.error(f"Standard output: {result.stdout}")
                return None
            
            # Parse the JSON output
            probe_data = json.loads(result.stdout)
            
            # Extract relevant audio metadata
            if not probe_data.get('streams'):
                logging.error(f"No streams found in {file_path}")
                return None
            
            # Find the audio stream
            audio_stream = next((stream for stream in probe_data['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            if not audio_stream:
                logging.error(f"No audio stream found in {file_path}")
                return None
            
            # Extract key metadata
            format_data = probe_data['format']
            return {
                'format_name': format_data.get('format_name'),
                'duration': float(format_data.get('duration', 0)),
                'bit_rate': int(format_data.get('bit_rate', 0)),
                'channels': int(audio_stream.get('channels', 0)),
                'sample_rate': int(audio_stream.get('sample_rate', 0)),
                'codec_name': audio_stream.get('codec_name')
            }
            
        except (subprocess.SubprocessError, json.JSONDecodeError, KeyError, ValueError) as e:
            logging.error(f"Error analyzing {file_path}: {str(e)}")
            return None
    
    def is_valid_audio_file(self, file_path: str) -> bool:
        """
        Validates if the file is a supported and valid audio file.
        """
        # Check file extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            return False
        
        # Validate using ffprobe
        return self._probe_file(file_path) is not None
    
    def get_audio_format(self, file_path: str) -> Optional[Dict]:
        """
        Public method to get audio metadata.
        """
        return self._probe_file(file_path)
    
    def on_created(self, event):
        # Skip if a directory was created
        if event.is_directory:
            return
        
        file_path = event.src_path
        filename = os.path.basename(file_path)
        
        # Check if it's a valid audio file
        if self.is_valid_audio_file(file_path):
            logging.info(f"Detected new audio file: {filename}")
            
            # Get and log audio metadata
            metadata = self.get_audio_format(file_path)
            if metadata:
                logging.info(f"Audio metadata for {filename}:")
                for key, value in metadata.items():
                    logging.info(f"  {key}: {value}")
            
            # Future: Add transcription logic here
        else:
            logging.debug(f"Ignoring non-audio file or invalid audio: {filename}")

# Function that sets up and runs the directory monitoring
def monitor_directory(path):
    # Create the event handler and observer objects
    event_handler = AudioHandler()
    observer = Observer()
    # Set up the observer to watch the specified path
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    try:
        # Keep the monitoring running until interrupted
        print(f"Monitoring directory: {path}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle clean shutdown on Ctrl+C
        observer.stop()
        print("\nStopping directory monitoring")
    
    # Wait for the observer thread to finish
    observer.join()

# Main execution block
if __name__ == "__main__":
    # Create path to input directory relative to this script
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "input")
    # Create the input directory if it doesn't exist
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    # Start monitoring the input directory
    monitor_directory(input_dir)
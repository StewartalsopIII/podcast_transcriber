# Import required libraries
import time  # For adding delays
from watchdog.observers import Observer  # For monitoring file system events
from watchdog.events import FileSystemEventHandler  # Base class for handling file events
import os  # For file and directory operations

# Custom handler class that processes new audio files
class AudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Skip if a directory was created
        if event.is_directory:
            return
        
        # Get just the filename from the full path
        filename = os.path.basename(event.src_path)
        # Check if the new file is an m4a audio file
        if filename.endswith('.m4a'):
            print(f"Detected new audio file: {filename}")
            # Future: Add transcription logic here

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
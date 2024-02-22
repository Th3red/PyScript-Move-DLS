import os
from os.path import splitext, exists, join
import sys
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemEventHandler

source_dir = "/Users/name/Downloads"
dest_dir_zipfolder = "/Users/name/Downloads/zipfolder"
dest_dir_image = "/Users/name/Downloads/imagefolder"
#def main(source, target):
 #   cwd = os.getcwd()
 #   source_path = os.path.join(cwd,source)
 #   target_path = os.path.join(cwd, target)
def makeUnique(dest, path):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
        
    return name

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry,dest)
    
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('zip') or name.endswith('.rar'):
                    if entry.stat().st_size < 25:
                        dest = source_dir
                    else:
                        dest = dest_dir_zipfolder
                    move(dest, entry, name)
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = dest_dir_image
                    move(dest, entry, name)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
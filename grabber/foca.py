import os
from pypdf import PdfReader
import utils.console as console

class FocaGrabber:
    def __init__(self, target):
        self.target = target
        self.metadata = {}

    def grabData(self):
        console.task('Searching for documents from "{}"'.format(self.target))
        # In a real scenario, we would search for documents related to the target.
        # For this example, we'll just use the Example.pdf
        
        if os.path.exists("Example.pdf"):
            console.subtask("Extracting metadata from Example.pdf")
            try:
                reader = PdfReader("Example.pdf")
                meta = reader.metadata
                self.metadata = {
                    "Author": meta.author,
                    "Creator": meta.creator,
                    "Producer": meta.producer,
                    "Subject": meta.subject,
                    "Title": meta.title,
                    "Creation Date": meta.creation_date,
                    "Modification Date": meta.modification_date,
                }
            except Exception as e:
                console.subfailure(f"Could not read metadata from PDF: {e}")
        else:
            console.subfailure("No documents found for target.")

    def getMetadata(self):
        return self.metadata

from llama_index.core.tools import FunctionTool
import os

# Here wi will set up a function to generate notes from the llama query
# FunctionTool is to wrap our function so that llama_index can use it
# The LLM will use this function as well

note_file = os.path.join("data", "notes.txt")

def save_note(note):
    if not os.path.exists(note_file):
        open(note_file, "w")

    # Open in append mode
    with open(note_file, "a") as f:
        f.writelines([note + "\n"])

    return "note saved"

note_engine = FunctionTool.from_defaults(
    fn = save_note,
    name = "note_saver",
    description = "this tool can save a text-basde note to a file for the user"
)
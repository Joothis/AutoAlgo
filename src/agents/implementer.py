"""
Implementation agent.
"""
import os

class ImplementerAgent:
    """
    The Implementer agent takes a code proposal and saves it to a runnable
    file, preparing it for execution and evaluation.
    """

    def save_code(self, code: str, file_path: str):
        """
        Saves the given code to the specified file path.

        Args:
            code: The string containing the Python code.
            file_path: The absolute path to save the file to.
        """
        try:
            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"Successfully saved code to {file_path}")
            return True
        except IOError as e:
            print(f"Error saving code to {file_path}: {e}")
            return False


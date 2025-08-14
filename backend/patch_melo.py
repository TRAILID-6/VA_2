# backend/patch_melo.py
import os
import sys


def find_japanese_file():
    """Searches all Python paths to find the melo/text/japanese.py file."""
    for path in sys.path:
        potential_path = os.path.join(path, "melo", "text", "japanese.py")
        if os.path.exists(potential_path):
            return potential_path
    return None


def patch_file():
    """
    Finds and patches the melo/text/japanese.py file to prevent it from
    crashing when the MeCab dependency is not fully installed.
    """
    japanese_file_path = find_japanese_file()

    if not japanese_file_path:
        print("Error: Could not find melo/text/japanese.py in any of the Python paths.")
        print("Please ensure MeloTTS was installed correctly.")
        return

    print(f"Found file to patch at: {japanese_file_path}")

    try:
        with open(japanese_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # The line number might vary slightly, so we search for the content
        line_number = -1
        for i, line in enumerate(lines):
            if "_TAGGER = MeCab.Tagger()" in line:
                line_number = i
                break

        if line_number == -1:
            print(
                "Could not find the target line '_TAGGER = MeCab.Tagger()'. The file might already be patched or has changed."
            )
            return

        print("Found the problematic line. Patching now...")

        # The replacement code with error handling
        replacement_code = [
            "try:\n",
            "    _TAGGER = MeCab.Tagger()\n",
            "except RuntimeError:\n",
            "    # This is expected if MeCab is not fully installed, which is fine if not using Japanese.\n",
            "    print('MeCab loading failed, setting _TAGGER to None.')\n",
            "    _TAGGER = None\n",
        ]

        # Replace the original line with the new block of code
        original_line = lines[line_number]
        # Add the same indentation as the original line
        indentation = " " * (len(original_line) - len(original_line.lstrip(" ")))

        # Rebuild the list of lines
        final_lines = lines[:line_number]
        for new_line in replacement_code:
            final_lines.append(indentation + new_line)
        final_lines.extend(lines[line_number + 1 :])

        with open(japanese_file_path, "w", encoding="utf-8") as f:
            f.writelines(final_lines)

        print("\nSuccessfully patched melo/text/japanese.py!")
        print(
            "You can now delete this script (patch_melo.py) and start the TTS server."
        )

    except Exception as e:
        print(f"An error occurred while patching the file: {e}")


if __name__ == "__main__":
    patch_file()

import re

def generate_table_of_contents(markdown_file):
    toc = ""
    headers = []

    # Read the Markdown file
    with open(markdown_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract headers and their corresponding line numbers
    for i, line in enumerate(lines):
        match = re.match(r'^(#+)\s+(.*)$', line)
        if match:
            level = len(match.group(1))
            header_text = match.group(2)
            headers.append((level, header_text, i))

    # Generate table of contents
    for level, header_text, line_number in headers:
        indent = "  " * (level - 1)
        link = re.sub(r'[^a-zA-Z0-9]+', '-', header_text.lower())
        toc += f"{indent}- [{header_text}](#{link})\n"

    return toc

# Example usage:
markdown_file = './README.md'
toc_string = generate_table_of_contents(markdown_file)
print(toc_string)
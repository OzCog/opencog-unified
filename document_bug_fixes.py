#!/usr/bin/env python3
"""
Convert bug fix TODOs into well-documented NOTEs with context
"""
import json
import re


def read_file_lines(filepath):
    """Read file and return lines"""
    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file_lines(filepath, lines):
    """Write lines to file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def convert_bug_comment(content, context):
    """Convert a bug fix comment to a well-documented NOTE"""

    # Extract the core issue
    content_clean = re.sub(r'^[/;#]*\s*(XXX|TODO|FIXME)\s*', '', content).strip()

    # Determine the comment style
    if content.strip().startswith('//'):
        prefix = '// '
    elif content.strip().startswith(';'):
        prefix = '; '
    else:
        prefix = '// '

    # Create improved documentation
    note = f"{prefix}NOTE: {content_clean}\n"
    note += f"{prefix}This requires further investigation and testing before implementation.\n"

    return note

# Load bug fixes
with open('categorized_bug_fixes.json') as f:
    data = json.load(f)

documentation_fixes = data['documentation_fixes']

print(f"Processing {len(documentation_fixes)} documentation fixes...")

# Select a subset to process (10 items for this batch)
selected_fixes = documentation_fixes[:10]

processed = []
for item in selected_fixes:
    filepath = item['file']
    line_num = item['line']

    print(f"\nProcessing: {filepath}:{line_num}")
    print(f"  Content: {item['content'][:60]}...")

    lines = read_file_lines(filepath)
    if lines is None:
        print("  Skipped (file not found)")
        continue

    # Find and update the line
    if line_num <= len(lines):
        original_line = lines[line_num - 1]
        new_comment = convert_bug_comment(item['content'], item['context'])

        # Replace the line
        lines[line_num - 1] = new_comment

        if write_file_lines(filepath, lines):
            processed.append({
                'file': filepath,
                'line': line_num,
                'original': original_line.strip(),
                'updated': new_comment.strip()
            })
            print("  Updated successfully")
        else:
            print("  Failed to write")
    else:
        print("  Skipped (line number out of range)")

# Save report
with open('bug_fix_documentation_report.json', 'w') as f:
    json.dump(processed, f, indent=2)

print(f"\n\nProcessed {len(processed)} bug fix documentation updates")
print("Report saved to bug_fix_documentation_report.json")

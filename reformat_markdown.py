import re

def reformat_file(input_path, output_path):
    """Reformat PDF-extracted markdown with proper structure"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output = []
    skip_next = False
    title_added = False
    in_toc = False

    for i, line in enumerate(lines):
        line = line.rstrip()

        # Skip page markers
        if '<!-- Page' in line:
            continue

        # Skip empty lines but preserve some structure
        if not line.strip():
            if output and output[-1] != '':
                output.append('')
            continue

        original = line
        line = line.strip()

        # Skip copyright and metadata
        if any(x in line for x in ['All rights reserved', 'BEE KOREA', 'Email:', 'Homepage:', '©', 'Bangladesh']):
            continue

        # Main title for Discipleship Training
        if 'ONE-TO-ONE' in line and 'DISCIPLESHIP' in line and 'TRAINING' in line and not title_added:
            output.append('# ONE-TO-ONE DISCIPLESHIP TRAINING')
            output.append('')
            output.append('**3rd Edition** - *for private circulation only*')
            output.append('')
            title_added = True
            continue

        # Main title for Christian Life
        if 'CHRISTIAN LIFE' in line and not title_added:
            output.append('# CHRISTIAN LIFE')
            output.append('')
            output.append('**3rd Edition**')
            output.append('')
            title_added = True
            continue

        # Main title for Galatians
        if line == 'GALATIANS' and not title_added:
            output.append('# GALATIANS')
            output.append('')
            output.append('**2nd Edition**')
            output.append('')
            title_added = True
            continue

        # Table of Contents
        if line == 'Contents':
            output.append('## Table of Contents')
            output.append('')
            in_toc = True
            continue

        if in_toc and line.startswith('Course Introduction'):
            in_toc = False

        # Unit headers (Unit I, Unit II, Unit III, etc.)
        if re.match(r'^Unit\s+[IVX]+.*$', line):
            output.append(f'## {line}')
            output.append('')
            continue

        # Lesson headers
        if re.match(r'^Lesson\s+\d+', line):
            output.append(f'### {line}')
            output.append('')
            continue

        # Encounter headers
        if re.match(r'^Encounter\s+\d+', line):
            output.append(f'### {line}')
            output.append('')
            continue

        # Section with letters (A., B., C., etc.)
        if re.match(r'^[A-Z]\.\s+[A-Z]', line):
            output.append(f'#### {line}')
            output.append('')
            continue

        # Numbered subsections (1., 2., 3., etc.)
        if re.match(r'^\d+\.\s+', line) and len(line) > 4:
            output.append(f'**{line}**')
            output.append('')
            continue

        # Questions
        if line.startswith('Question '):
            output.append(f'> **{line}**')
            output.append('')
            continue

        # Section titles (like "Course Introduction", "Objectives", etc.)
        if line.isupper() and len(line) > 3 and not line.startswith(('UNIT', 'LESSON')):
            output.append(f'### {line}')
            output.append('')
            continue

        # Regular content
        if line and not line.endswith('...') and not re.match(r'^[ivxlc]+$', line):
            output.append(line)

    # Write formatted output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

    return output_path

# Process all three files
files = [
    ('C:/Users/viren/source/jcbiblecourse/121-PHILS-TEXT.md', 'C:/Users/viren/source/jcbiblecourse/121-PHILS-TEXT.md'),
    ('C:/Users/viren/source/jcbiblecourse/CL-TEXT-PHILS.md', 'C:/Users/viren/source/jcbiblecourse/CL-TEXT-PHILS.md'),
    ('C:/Users/viren/source/jcbiblecourse/GALATIANS-PHILS-TEXT.md', 'C:/Users/viren/source/jcbiblecourse/GALATIANS-PHILS-TEXT.md')
]

for input_file, output_file in files:
    try:
        reformat_file(input_file, output_file)
        print(f'✓ Reformatted {input_file.split("/")[-1]}')
    except Exception as e:
        print(f'✗ Error with {input_file}: {e}')

print('\nReformatting complete!')

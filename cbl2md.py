import os

extensionCblPreprocessed = '.CBL_preprocessed'
pathCorrelation = './os390/correlation'
workingStorageId = 'WORKING-STORAGE'
linkageId = 'LINKAGE'
paragraphSection = '# '
paragraphLabel   = '## '

def find_sections(file_path):
    program_name = ''
    sections = {}
    current_section = ''
    section_name = ''
    current_section_lines = []
    linePrint = ''

    with open(file_path, 'r') as f:
        for linenum, line in enumerate(f):
            paragraph = ''
            line = line.rstrip()
            if 'IDENTIFICATION DIVISION' in line:
                program_name = next(f).split('PROGRAM-ID.')[1].strip()
                program_name = program_name.split('.')[0]
            if 'SECTION.' in line:
                current_section = line[7:].split()[0]
                if(section_name != ""):
                    sections[section_name] = current_section_lines
                    paragraph = paragraphSection
                section_name = current_section
                current_section_lines = []
            linePrint = line[7:72].rstrip()
            if current_section != '' and linePrint!= '':
                if (line[7:8] !=' ' and 'SECTION.' not in line):
                    current_section_lines.append("")
                    paragraph = paragraphLabel
                current_section_lines.append(paragraph + linePrint)
    return sections

def main():
    for root, dirs, files in os.walk(pathCorrelation):
        for file in files:
            if file.endswith(extensionCblPreprocessed):
                file_path = os.path.join(root, file)
                sections = find_sections(file_path)
                # SECTIONS
                for section_name, section_lines in sections.items():
                    section_file = f"{file_path.replace(extensionCblPreprocessed,'')}_{section_name}.md"
                    if(workingStorageId in section_name or linkageId in section_name):
                        section_file = section_file.replace('_','__')
                    with open(section_file, 'w') as f:                       
                        for section_line in section_lines:
                            if section_line.startswith('# '):
                                f.write(section_line)
                                f.write("\n")
                                f.write("~~~text")
                                f.write("\n")
                            if section_line.startswith('## '):
                                f.write("~~~")
                                f.write(section_line)
                                f.write("\n")
                                f.write("~~~text")
                                f.write("\n")
                        f.write("~~~")

if __name__ == '__main__':
    main()

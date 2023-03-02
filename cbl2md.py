import os

projectName = "PRUEBAS2"
pathWorkspace = "/mnt/h/develop/WorkspaceMF/"
pathWorkspaceObsidian = "/mnt/h/obsidian/"
pathCorrelation = '/os390/correlation'
workingStorageId = 'WORKING-STORAGE'

extensionCblPreprocessed = '.CBL_preprocessed'
extensionMd = '.md'

identificationDivisionId = 'IDENTIFICATION_DIVISION'
linkageId = 'LINKAGE'
sectionId = 'SECTION'
programId = 'PROGRAM-ID.'

paragraphSection = '## '
paragraphLabel   = '### '
textStart = '~~~text'
textEnd   = '~~~'

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
            if identificationDivisionId in line:
                program_name = next(f).split(programId)[1].strip()
                program_name = program_name.split('.')[0]
            if sectionId in line:
                current_section = line[7:].split()[0]
                if(section_name != ""):
                    sections[section_name] = current_section_lines
                    paragraph = paragraphSection
                section_name = current_section
                current_section_lines = []
            linePrint = line[7:72].rstrip()
            if current_section != '' and linePrint!= '':
                if (line[7:8] !=' ' and sectionId not in line):
                    current_section_lines.append("")
                    paragraph = paragraphLabel
                current_section_lines.append(paragraph + linePrint)
    return sections

def main():
    for root, dirs, files in os.walk(pathWorkspace + projectName + pathCorrelation):
        for file in files:
            if file.endswith(extensionCblPreprocessed):
                file_path = os.path.join(root, file)
                sections = find_sections(file_path)
                # SECTIONS
                for section_name, section_lines in sections.items():
                    section_file = f"{file_path.replace(pathWorkspace, pathWorkspaceObsidian).replace(extensionCblPreprocessed,'')}_{section_name}{extensionMd}"
                    if(workingStorageId in section_name or linkageId in section_name):
                        section_file = section_file.replace('_','__')
                    os.makedirs(os.path.dirname(section_file), exist_ok=True)    
                    with open(section_file, 'w') as f:                       
                        for section_line in section_lines:
                            if (section_line.startswith(paragraphSection) or section_line.startswith(paragraphLabel)):
                                if section_line.startswith(paragraphLabel):
                                    f.write(textEnd)
                                    f.write("\n")  
                                f.write(section_line)
                                f.write("\n")
                                f.write(textStart)
                                f.write("\n")
                            else:
                                f.write(section_line)
                                f.write("\n")
                        f.write(textEnd)

if __name__ == '__main__':
    main()

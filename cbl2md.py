import os

projectName = "PRUEBAS2"
pathWorkspace = "/mnt/h/develop/WorkspaceMF/"
pathWorkspaceObsidian = "/mnt/h/obsidian/"
pathCorrelation = '/os390/correlation'

extensionCblPreprocessed = '.CBL_preprocessed'
extensionMd = '.md'

identificationDivisionId = 'IDENTIFICATION_DIVISION'
workingStorageId = 'WORKING-STORAGE'
linkageId = 'LINKAGE'
configurationId = 'CONFIGURATION'

lisSectionNoProcess = ['WORKING-STORAGE','LINKAGE','CONFIGURATION','FILE']

sectionId = 'SECTION.'
programId = 'PROGRAM-ID.'
callInstruction = 'CALL'
gotoInstruction = 'GO TO'
cicsExec = 'CICS'
sqlExec = 'SQL'

performInstruction = 'PERFORM'
performThruInstruction = 'THRU'


lisProgramNoLink = ['ERROR']

patternVarCALLId = 'C-CALLED-MODULE-NAME'
patternMoveCALLId = 'MOVE'

tagCobolProgram = '#CobolProgram'
tagCobolSection = '#CobolSection'
tagCobolCics = '#CobolCics'
tagCobolSql = '#CobolSql'

textFixed = '```'

paragraphSection = '## '
paragraphLabel   = '### '

separatorSection = '_'
separatorSectionSpecial = '__'


def find_sections(file_path):
    program_name = ''
    sections = {}
    current_section = ''
    section_name = ''
    current_section_lines = []
    linePrint = ''
    patternProgramId = ''

    with open(file_path, 'r') as f:
        for linenum, line in enumerate(f):
            paragraph = ''
            line = line.rstrip()
            if identificationDivisionId in line:
                program_name = next(f).split(programId)[1].strip()
                program_name = program_name.split('.')[0]
            if sectionId in line:
                current_section = line[7:].split()[0]
                paragraph = paragraphSection
                if(section_name != "" and section_name not in lisSectionNoProcess):
                    sections[section_name] = current_section_lines
                section_name = current_section
                current_section_lines = []
            linePrint = line[7:72].rstrip()
            if current_section != '' and linePrint!= '':
                if (line[7:8] !=' ' and sectionId not in line and sqlExec not in line):
                    current_section_lines.append("")
                    paragraph = paragraphLabel
                if paragraph == '':
                    espacios_iniciales = len(linePrint) - len(linePrint.lstrip())                
                    if gotoInstruction in linePrint:
                        linePrint = "&nbsp;" * espacios_iniciales + textFixed + ' '.join(linePrint.lstrip().replace(" ", " ").split()[:2]) + textFixed + "[[" + os.path.basename(file_path).replace(extensionCblPreprocessed,'') +"_" + section_name + extensionMd + "#" + linePrint.lstrip().replace(" ", " ").split()[-1] + "|" + linePrint.lstrip().replace(" ", " ").split()[-1]  + "]]"
                    elif (performInstruction in linePrint and performThruInstruction not in linePrint):
                        linePrint = "&nbsp;" * espacios_iniciales + textFixed + ' '.join(linePrint.lstrip().replace(" ", " ").split()[:1]) + textFixed + "[[" + os.path.basename(file_path).replace(extensionCblPreprocessed,'') + "_" + linePrint.lstrip().replace(".", "").split()[-1] + "]]"
                    elif (performInstruction in linePrint and performThruInstruction in linePrint):
                        linePrint = "&nbsp;" * espacios_iniciales + textFixed +  linePrint.lstrip().replace(" ", " ") + textFixed
                    elif (patternMoveCALLId in linePrint and patternVarCALLId in linePrint):
                        if(linePrint.lstrip().split(" ")[1].startswith("'")):
                            patternProgramId = linePrint.lstrip().split(" ")[1].split("'")[1]
                            linePrint = "&nbsp;" * espacios_iniciales + textFixed +  linePrint.lstrip().replace(" ", " ") + textFixed
                        else:                            
                            patternProgramId = linePrint.lstrip().replace("  ", " ").split(" ")[1].split("-")[2]
                            linePrint = "&nbsp;" * espacios_iniciales + textFixed +  linePrint.lstrip().replace(" ", " ") + textFixed
                    elif (callInstruction in linePrint and patternProgramId != ''):
                        if(patternProgramId in lisProgramNoLink):
                            linePrint = "&nbsp;" * espacios_iniciales + textFixed +  linePrint.lstrip().replace(" ", " ") + textFixed
                        else:
                            linePrint = "&nbsp;" * espacios_iniciales + textFixed + ' '.join(linePrint.lstrip().replace(" ", " ").split()[:1]) + textFixed + "[[" + patternProgramId +  "]]"
                        patternProgramId = ''
                    else:    
                        linePrint = "&nbsp;" * espacios_iniciales + textFixed +  linePrint.lstrip().replace(" ", " ") + textFixed
                current_section_lines.append(paragraph + linePrint)
    return sections

def main():
    for root, dirs, files in os.walk(pathWorkspace + projectName + pathCorrelation):
        for file in files:
            if file.endswith(extensionCblPreprocessed):
                file_path = os.path.join(root, file)
                sections = find_sections(file_path)
                # SECTIONS
                section_file = ""
                for section_name, section_lines in sections.items():
                    if(section_name not in lisSectionNoProcess):
                        section_file = f"{file_path.replace(pathWorkspace, pathWorkspaceObsidian).replace(extensionCblPreprocessed,'')}{separatorSection}{section_name}{extensionMd}"
                        os.makedirs(os.path.dirname(section_file), exist_ok=True)    
                    # PROGRAMS
                    program_file = file_path.replace(pathWorkspace, pathWorkspaceObsidian).replace(extensionCblPreprocessed,'') + extensionMd
                    with open(program_file, 'w') as p:      
                        p.write(tagCobolProgram + '\n')
                        for section in sections:
                            if(section not in lisSectionNoProcess):
                                p.write("[[" + os.path.basename(file_path).replace(extensionCblPreprocessed,'') + separatorSectionSpecial + section + extensionMd + "]]")
                            else:
                                p.write("[[" + os.path.basename(file_path).replace(extensionCblPreprocessed,'') + separatorSection + section + extensionMd + "]]")
                            p.write("\n")
                        
                    with open(section_file, 'w') as f:                       
                        f.write(tagCobolSection + '\n')
                        for section_line in section_lines:
                            if (section_line.startswith(paragraphSection) or section_line.startswith(paragraphLabel)):
                                if section_line.startswith(paragraphLabel):
                                    f.write("\n")  
                                f.write(section_line)
                                f.write("\n")
                                f.write("\n")
                            else:
                                if(cicsExec in section_line):
                                    f.write("![[CICS.png]]")
                                    f.write("\n")
                                if(sqlExec in section_line):
                                    f.write("![[SQL.png]]")
                                    f.write("\n")                                    
                                f.write(section_line)
                                f.write("\n")

if __name__ == '__main__':
    main()

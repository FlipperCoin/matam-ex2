#### IMPORTS ####
import event_manager as EM

CURRENT_YEAR = 2020

def readAllLines(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def isIdValid(id):
    if len(id) is not 8:
        return False
    
    try:
        id_number = int(id)
    except Exception:
        return False
    
    # 10000000 is the smallest 8 digit number
    if id_number >= 10000000 and id_number < 100000000:
        return True

    return False

def isNameValid(name):
    for s in name.split():
        if not s.isalpha():
            return False
    
    return True

def isAgeValid(age, year):
    try:
        age_num = int(age)
        year_num = int(year)
    except Exception:
        return False

    if (CURRENT_YEAR - age_num) != year_num:
        return False
    
    if age_num < 16 or age_num > 120:
        return False
    
    return True

def isSemesterValid(semester):
    try:
        semester_num = int(semester)
    except Exception:
        return False

    return semester_num >= 1

def isValidAttributes(attributes):
    return isIdValid(attributes[0]) and isNameValid(attributes[1]) and isAgeValid(attributes[2], attributes[3]) and isSemesterValid(attributes[4])

def fixName(name):
    return " ".join(name.split())

def fixAttributes(attributes):
    attributes = list(attributes)
    attributes[1] = fixName(attributes[1])
    return attributes

def attributesCorrect(students_attributes):
    correct_attributes = []

    for attributes in students_attributes:
        if len(attributes) is not 5:
            continue
        
        if not isValidAttributes(attributes):
            continue

        attributes = fixAttributes(attributes)

        id_attribute = attributes[0]

        if len(correct_attributes) == 0:
            correct_attributes.append(attributes)
        else:
            for i in range(0,len(correct_attributes)):
                existing_attributes = correct_attributes[i]
                existing_id_attribute = existing_attributes[0]
                
                if id_attribute == existing_id_attribute:
                    correct_attributes[i] = attributes
                    break
                
                if i == (len(correct_attributes)-1):
                    correct_attributes.append(attributes)
        
    get_id = lambda attributes: attributes[0]
    correct_attributes.sort(key=get_id)

    return correct_attributes

def getAttributes(student_lines):
    student_attributes = []
    for line in student_lines:
        attributes = line.split(',')
        attributes = [attribute.strip() for attribute in attributes]
        student_attributes.append(attributes)
    
    return student_attributes

def linesCorrect(lines):
    student_attributes = getAttributes(lines)
    student_attributes = attributesCorrect(student_attributes)
    correct_lines = [", ".join(attributes) + '\n' for attributes in student_attributes]
    return correct_lines

#### PART 1 ####
# Filters a file of students' subscription to specific event:
#   orig_file_path: The path to the unfiltered subscription file
#   filtered_file_path: The path to the new filtered file
def fileCorrect(orig_file_path: str, filtered_file_path: str):
    lines = readAllLines(orig_file_path)
    
    f_out = open(filtered_file_path, 'w')

    f_out.writelines(linesCorrect(lines))
    
    f_out.close()
    

# Writes the names of the K youngest students which subscribed 
# to the event correctly.
#   in_file_path: The path to the unfiltered subscription file
#   out_file_path: file path of the output file
def printYoungestStudents(in_file_path: str, out_file_path: str, k: int) -> int:
    if not isinstance(k, int) or k < 1:
        return -1
        
    lines = readAllLines(in_file_path)
    student_attributes = attributesCorrect(getAttributes(lines))
    
    get_age = lambda student: int(student[2])
    student_attributes.sort(key=get_age)

    student_attributes = student_attributes[:k]
    with open(out_file_path, 'w') as f_out:
        for student in student_attributes:
            f_out.write(student[1] + '\n')
                
    return len(student_attributes)
    
# Calculates the avg age for a given semester
#   in_file_path: The path to the unfiltered subscription file
#   retuns the avg, else error codes defined.
def correctAgeAvg(in_file_path: str, semester: int) -> float:
    if not isSemesterValid(semester):
        return -1
    
    lines = readAllLines(in_file_path)
    student_attributes = attributesCorrect(getAttributes(lines))

    students_semester = list(filter(lambda student: int(student[4])==semester, student_attributes))
    if len(students_semester) == 0:
        return 0
    
    students_age = [int(student[2]) for student in students_semester]
    return sum(students_age) / len(students_age)
    

def isEventEntryValid(event):
    if not isinstance(event,dict) or len(event) != 3:
        return False
    
    if event.get("date", None) is None or event.get("name", None) is None or event.get("id", None) is None:
        return False
    
    return isinstance(event["date"], object) and isinstance(event["id"], int) and isinstance(event["name"], str)  

#### PART 2 ####
# Use SWIG :)
# print the events in the list "events" using the functions from hw1
#   events: list of dictionaries
#   file_path: file path of the output file
def printEventsList(events :list,file_path :str):
    # we can assume events is not empty
    earliestDate = events[0]["date"]
    for event in events:
        if not isEventEntryValid(event):
            continue

        if EM.dateCompare(earliestDate,event["date"]) > 0:
            earliestDate = event["date"]
    
    em = EM.createEventManager(earliestDate)
    for event in events:
        EM.emAddEventByDate(em, event["name"], event["date"], event["id"])
    
    EM.emPrintAllEvents(em, file_path)
    
    return em
    
def testPrintEventsList(file_path :str):
    events_lists=[{"name":"New Year's Eve","id":1,"date": EM.dateCreate(30, 12, 2020)},\
                    {"name" : "annual Rock & Metal party","id":2,"date":  EM.dateCreate(21, 4, 2021)}, \
                                 {"name" : "Improv","id":3,"date": EM.dateCreate(13, 3, 2021)}, \
                                     {"name" : "Student Festival","id":4,"date": EM.dateCreate(13, 5, 2021)},    ]
    em = printEventsList(events_lists,file_path)
    for event in events_lists:
        EM.dateDestroy(event["date"])
    EM.destroyEventManager(em)

#### Main #### 
# feel free to add more tests and change that section. 
# sys.argv - list of the arguments passed to the python script
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        testPrintEventsList(sys.argv[1])

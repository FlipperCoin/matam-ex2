from eventManager import *

if __name__ == '__main__':
    fileCorrect("tests/input","tests/out1")
    fileCorrect("tests/input_worse","tests/out1_worse")
    num1 = correctAgeAvg("tests/input", 3)
    print(float(num1))
    printYoungestStudents("tests/input","tests/out2", 2)
    printYoungestStudents("tests/youngest_input","tests/youngest_out", 8)
    printYoungestStudents("tests/youngest_input","tests/youngest_out1", 2)
    printYoungestStudents("tests/youngest_input","tests/youngest_out2", 4)
    printYoungestStudents("tests/youngest_input","tests/youngest_out3", 5)
    printYoungestStudents("tests/youngest_input","tests/youngest_out4", 10)
    printYoungestStudents("tests/youngest_input5","tests/youngest_out5", 8)

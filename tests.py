import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_files import write_file
from functions.run_python_file import run_python_file

def main():
    working_dir = "calculator"
    '''    
    root_contents = get_files_info(working_dir, ".")
    print(root_contents)
    
    pkg_contents = get_files_info(working_dir, "pkg")
    print(pkg_contents)
    
    pkg_contents = get_files_info(working_dir, "/bin")
    print(pkg_contents)

    pkg_contents = get_files_info(working_dir, "../")
    print(pkg_contents)
    '''

    # file_content = get_file_content(working_dir, "lorem.txt") #Does not work
    # print(file_content)

    # Second round of testings
    '''
    print(get_file_content(working_dir, "main.py"))
    print(get_file_content(working_dir, "pkg/calculator.py"))
    print(get_file_content(working_dir, "bin/cat"))
    print(get_file_content(working_dir, "/bin/cat"))
    '''

    #Third round of testings with writing content to file
    '''
    print(write_file(working_dir, "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file(working_dir, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file(working_dir, "/tmp/temp.txt", "this should not be allowed"))
    '''

    # Fourth round of testing running python program
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

main() 
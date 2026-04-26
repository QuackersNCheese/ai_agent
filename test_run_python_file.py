from functions.run_python_file import run_python_file

def run_tests():
    # Test run main.py without args
    print("Test 1: Running main.py (no args):")
    print(run_python_file("calculator", "main.py"))
    print("-" * 30)

    # Test run main.py with a calculation
    print("Test 2: Running main.py with '3 + 5':")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 30)

    # Test run existing tests.py
    print("Test 3: Running tests.py:")
    print(run_python_file("calculator", "tests.py"))
    print("-" * 30)

    # Test security breach (outside directory)
    print("Test 4: Outside directory check:")
    print(run_python_file("calculator", "../main.py"))
    print("-" * 30)

    # Test nonexistent file
    print("Test 5: Nonexistant file check")
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 30)

    # Test invalid file type
    print("Test 6: Not a .py file:")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    run_tests()
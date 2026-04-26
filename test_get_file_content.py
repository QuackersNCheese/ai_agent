from functions.get_file_content import get_file_content

def run_tests():
    print("Testing Truncation (lorem.txt):")
    res = get_file_content("calculator", "lorem.txt")
    print(f"Content Length: {len(res)}")
    print(f"Ends with truncation message: {'truncated' in res}")
    print("-" * 30)

    print("Reading main.py:")
    print(get_file_content("calculator", "main.py"))
    print("-" * 30)

    print("Reading calculator:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("-" * 30)

    print("Testing Security Breach (/bin/cat):")
    print(get_file_content("calculator", "/bin/cat"))
    print("=" * 30)

    print("Testing Missing File:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    run_tests()
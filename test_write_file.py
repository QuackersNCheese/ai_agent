from functions.write_file import write_file

def run_tests():
    # Test overwriting an existing file
    print("Testing overwrite (lorem.txt):")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("-" * 30)

    # Test Creating a new file in a new subdirectory
    print("Testing new file in pkg subdirectory:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("-" * 30)

    # Test Unauthorized system write
    print("Testing unauthorized write(/tmp/temp.txt):")
    print(f"    {write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')}")


if __name__ == "__main__":
    run_tests()
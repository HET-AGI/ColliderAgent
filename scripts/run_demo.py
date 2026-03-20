# scripts/on_magnus/tests/test_file_backwarding.py
# Executed by Magnus blueprint `transfer-file`.
# THIS IS NOT DEAD CODE. 
from magnus import custody_file


def main():
    
    path = "hello_world.out"
    
    with open(path, mode="w") as file_pointer:
        file_pointer.write("Hello world.\n")
    
    file_secret = custody_file(path)
    print(f"Download file by: magnus receive {file_secret}")


if __name__ == "__main__":
    
    main()
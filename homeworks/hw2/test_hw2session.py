#!/usr/bin/env python3

from filesystem import FileSystem
from hw2session import HW2Session

# Test the implementation
def test_hw2session():
    # Initialize file system
    fs = FileSystem()
    fs.format()
    
    # Add users
    fs.add_user('john')
    fs.add_user('david')
    
    # Create session and login
    session = HW2Session(fs)
    session.login('david')
    
    print("=== Testing mkdir and ls ===")
    session.mkdir('test_dir')
    session.mkdir('another_dir')
    print("ls:", session.ls())
    
    print("\n=== Testing touch ===")
    session.touch('test_file.txt')
    session.touch('another_file.py')
    print("ls after touch:", session.ls())
    
    print("\n=== Testing cd ===")
    session.cd('test_dir')
    print("pwd:", session.pwd())
    session.mkdir('subdir')
    session.touch('file_in_subdir.txt')
    print("ls in test_dir:", session.ls())
    
    print("\n=== Testing rmdir (should fail - directory not empty) ===")
    session.cd('..')  # go back to david's home
    session.rmdir('test_dir')  # should fail because it's not empty
    
    print("\n=== Testing rm ===")
    session.rm('test_file.txt')
    print("ls after rm:", session.ls())
    
    print("\n=== Testing rm on directory (should fail) ===")
    session.rm('test_dir')  # should fail because it's a directory
    
    print("\n=== Testing rmdir on empty directory ===")
    session.cd('test_dir')
    session.rmdir('subdir')  # should work because subdir is empty after removing file
    session.cd('..')
    
    print("\n=== Testing dump_fsimage ===")
    session.dump_fsimage()

if __name__ == "__main__":
    test_hw2session()

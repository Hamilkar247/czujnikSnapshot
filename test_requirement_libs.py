import logging
import os
import hashlib
import logging
import subprocess
import sys


# inspiracja https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5_file(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for part in iter(lambda: f.read(4096), b""):
            hash_md5.update(part)
    return hash_md5.digest()


def md5_string(string):
    hash_object = hashlib.md5(string)
    return hash_object.digest()


def test_all_libs_is_in_requirement():
    logging.root.setLevel(logging.DEBUG)
    hash_md5 = hashlib.md5()
    exist_requirements_md5 = None
    requirement_file = "requirements.txt"
    if os.path.exists(requirement_file):
        exist_requirements_md5 = md5_file(requirement_file)
    else:
        print("not exist file requirements.txt")

    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    pip_free_output = md5_string(reqs)
    assert pip_free_output == exist_requirements_md5

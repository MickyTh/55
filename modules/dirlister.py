import os
def run(**args):
    print("IN dirlister module")
    return str(os.listdir("."))

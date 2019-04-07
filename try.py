from file_manager import *


def Main():
    inputfile = File()
    inputfile.detect_extension()
    inputfile = inputfile.create_subclass()
    inputfile.set_gatk_version("gatk-4.1.0.0")
    inputfile.VCFstats()


Main()

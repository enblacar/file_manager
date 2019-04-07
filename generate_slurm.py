from file_manager import *


def Main():
    inputfile = File()
    inputfile.detect_extension()
    inputfile = inputfile.create_subclass()
    inputfile.set_node_information(
        partition="p_hpca4se",
        node="catwoman",
        memory=128000,
        cpus=64)
    script_path = "./try.py"
    data_path = "./test.vcf"
    inputfile.change_script_path(script_path)
    inputfile.change_data_path(data_path)
    inputfile.generate_job()


Main()

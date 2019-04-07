# SHEBANG

import sys
import argparse
import os


class File:

    # Define special path names for programs.

    gatk_version = None

    def __init__(self):

        self.file = self.parse_arguments()

    def parse_arguments(self):
        """This function parse all arguments given to the main script."""

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--file",
            type=str,
            default=None,
            help="File given to the script.")

        arguments = parser.parse_args()
        if arguments.file:
            return arguments.file

    def detect_extension(self):
        """This function detects the extension of the file by looking at the file name"""

        self.extension = self.file.split(".")[-1]

    def create_subclass(self):
        """Given the extension, this function generates an object of its respective subclass."""

        if self.extension == "fasta":
            fasta_file = FASTAfile()
            return fasta_file

        elif self.extension == "vcf":
            vcf_file = VCFfile()
            return vcf_file

        elif self.extension == "slurm":
            slurm_file = SLURMfile()
            return slurm_file

    @classmethod
    def set_gatk_version(cls, version):
        """Defines the gatk version."""

        if isinstance(version, str):
            cls.gatk_version = version


class SLURMfile(File):

    extension = "slurm"
    # Define node variables.
    partition = None
    node = None
    cpus = None
    memory = None
    time = None
    exclusive = False
    thread_multiplier = None
    bashrc_path = "~/.bashrc"
    script_path = None
    data_path = None

    @classmethod
    def set_node_information(cls, node, cpus, memory, partition=None, time=None, thread_multiplier=None, exclusive=False):
        """This function accepts parameters corresponding to SLURM parameters.
                - node: Specify the node name.
                - cpus: Specify how many cpus are going to be used.
                - memory: Specify how many RAM (Mb) is going to be used.
                - time: Specify if you want any time limit (hh-mm-ss).
                - thread_multiplier: Specify the number or threads each CPU can generate.
                - exclusive: Specify if you want the exclusivity of the node."""

        cls.partition = partition
        cls.node = node
        cls.cpus = cpus
        cls.memory = memory
        cls.time = time
        cls.thread_multiplier = 1 if thread_multiplier is None else thread_multiplier
        cls.threads = cls.cpus * cls.thread_multiplier
        cls.exclusive = exclusive

    @classmethod
    def change_bashrc_path(cls, path):
        if isinstance(path, str):
            cls.bashrc_path = path
        else:
            sys.exit("Your input path is not a string.")

    @classmethod
    def change_script_path(cls, path):
        if isinstance(path, str):
            cls.script_path = path
        else:
            sys.exit("Your input path is not a string.")

    @classmethod
    def change_data_path(cls, path):
        if isinstance(path, str):
            cls.data_path = path
        else:
            sys.exit("Your input path is not a string.")

    def generate_job(self):
        """Generates a .slurm job for the class configuration."""

        with open(self.file, "wt") as job:
            job.write(f"#!/bin/bash\n")
            job.write(f"#SBATCH --partition {self.partition}\n")
            job.write(f"#SBATCH --nodelist {self.node}\n")
            job.write(f"#SBATCH --mem {self.memory}\n")
            job.write(f"#SBATCH --cpus-per-task {self.cpus}\n")
            if self.time:
                job.write(f"#SBATCH --time {self.time}\n")
            job.write(f"#SBATCH --job-name eblanco\n")
            if self.exclusive is not False:
                job.write(f"#SBATCH --exclusive\n")
            job.write(f"\n")
            job.write(f"source {self.bashrc_path}\n")
            job.write(f"hostname\n")
            job.write(f"date\n\n")
            job.write(f"python3.7 {self.script_path} --file {self.data_path}\n")


class FASTAfile(File):

    extension = "fasta"

    def __init__(self):
        super().__init__()
        self.test = "hi"


class VCFfile(File):

    extension = "vcf"

    def __init__(self):
        super().__init__()
        self.testVCF()

    def testVCF(self):
        """This function checks that the file is really a VCF file."""

        with open(self.file, "rt") as vcf:
            for line in vcf:
                if line == "\n":
                    continue
                if line[0] == "#":
                    continue
                else:
                    if len(line.split("\t")) < 8:
                        sys.exit("Your file is not a VCF file, or it is corrupted.")
                    return

    def VCFstats(self):
        """This function makes use of GATK to retrieve the stats."""

        os.system(f"{self.gatk_version} VariantsToTable \
            --variant {self.file} \
            --output {self.file[:(-len(self.extension))]}.tsv \
            -F CHROM \
            -F POS \
            -F ID \
            -F REF \
            -F ALT \
            -F FILTER \
            -F AC \
            -F AF \
            -F AN \
            -F DP \
            -F ExcessHet \
            -F FS \
            -F MLEAC \
            -F MLEAF \
            -F MQ \
            -F QD \
            -F SOR \
            -GF GT \
            -GF AD \
            -GF DP \
            -GF GQ \
            -GF PL")

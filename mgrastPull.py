import os
import argparse
from subprocess import Popen, check_call


class PullMetagenomes(object):

    def init_completion_status(self, list_of_ids):
        """
        Crawls through the root directory and checks which folders have .fastq.gz files and which do not.
        Currently only needs to find one .fastq.gz file to be satisfied.
        Returns two lists (incomplete, complete).
        """
        completed_list_of_ids = []

        for id in list_of_ids:
            file_list = os.listdir((self.root_path + id))
            for file in file_list:
                if file.endswith('.fastq.gz'):
                    completed_list_of_ids.append(id)
                    break
                else:
                    pass

        # Counting
        incomplete_list_of_ids = list(set(list_of_ids) - set(completed_list_of_ids))
        num_complete = len(completed_list_of_ids)
        num_total = len(completed_list_of_ids)+len(incomplete_list_of_ids)
        percent_complete = ((float(num_complete)/float(num_total))*100)

        print 'Completed: {0}\nTotal: {1}\n{0}/{1} = {2:.2f}%'.format(num_complete,
                                                                      num_total,
                                                                      percent_complete)

        return completed_list_of_ids, incomplete_list_of_ids

    def create_directories(self, list_of_ids):
        """
        Creates directories according to ID names in a list. Will skip if they already exist.
        """
        for id in list_of_ids:
            if os.path.exists(self.root_path + id):
                pass
            else:
                print 'Creating path for ' + id
                os.mkdir(self.root_path+id)

    @staticmethod
    def retrieve_id_list(list_of_ids):
        """
        Parses a text file with individual IDs on new lines and returns them as a list
        """
        with open(list_of_ids) as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]
        return content

    def run_rast_download(self, id):
        """
        Downloads a specific ID (MG-RAST dataset ID) using mg-download.py from MG-RAST-TOOLS
        """
        print '\nDownloading files for %s from MG-RAST...' % id
        p = Popen('source ./set_env.sh && python2 tools/bin/mg-download.py'
                  ' --metagenome %s --dir %s' % (id, self.root_path),
                    cwd=self.mg_rast_tools,
                    shell=True,
                    executable="/bin/bash")
        p.wait()

    @staticmethod
    def delete_extraneous_files(folder):
        """
        Deletes everything that is not a .fastq.gz file in the passed in folder
        """
        for file in os.listdir(folder):
            if file.endswith('.fastq.gz'):
                pass
            else:
                print 'Deleting %s...' % file

                try:
                    os.remove((folder + '/' + file))
                except:
                    print 'Could not delete %s. Skipping.' % file
                    pass

    @staticmethod
    def find_fastq_files(folder):
        """
        Finds all of the .fastq files in a designated folder and returns a list
        """
        to_compress = []
        for file in os.listdir(folder):
            if file.endswith('.fastq'):
                to_compress.append(file)
            else:
                pass

        return to_compress

    @staticmethod
    def gzip_fastq(fastq_file):
        """
        Compresses a fastq file using the terminal gzip.
        """
        print '\n... Gzipping ' + fastq_file + ' ...'
        check_call(['gzip', fastq_file])
        print 'Completed gzip of %s.' % fastq_file

    def __init__(self, args):
        self.raw_list_of_ids = args.raw_list_of_ids
        self.root_path = args.root_path
        self.mg_rast_tools = args.mg_rast_tools

        # Retrieve list of IDs
        list_of_ids = self.retrieve_id_list(self.raw_list_of_ids)

        # Create necessary directories
        self.create_directories(list_of_ids)

        # Figure out which files need to be downloaded/gzipped
        completed_list, incomplete_list = self.init_completion_status(list_of_ids)

        # print 'Work already completed for the following:\n' + str(completed_list)

        # Start downloading and gzipping
        for id in incomplete_list:
            # Set working folder
            working_folder = self.root_path + id

            # Start downloading contents of ID into respective directory
            self.run_rast_download(id)

            # Confirm .fastq files are present in specified folder
            to_compress = self.find_fastq_files(working_folder)
            print 'Found the following fastq files to compress: %s' % to_compress

            # Compress the .fastq files
            for fastq in to_compress:
                fastq_path = (working_folder + '/' + fastq)
                self.gzip_fastq(fastq_path)

            # Delete all unnecessary files (!= .fastq.gz) in folder
            self.delete_extraneous_files(working_folder)

            print 'Completed processing %s. Moving on to next ID in list...' % id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_list_of_ids",
                        help="Path to list of IDs .txt file. "
                        "File should be delimited by newlines",
                        type=str)

    parser.add_argument("root_path",
                        help="Path to root folder for metagenome data to be stored",
                        type=str)

    parser.add_argument("mg_rast_tools",
                        help="Path to MG-RAST-TOOLS folder necessary for access to mg-download.py",
                        type=str)

    arguments = parser.parse_args()
    x = PullMetagenomes(arguments)

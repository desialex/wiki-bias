import bz2
import sys
import os
import getopt
import time
from pov import POVProcessor
from StringBuilder import StringBuilder
import requests
import shutil


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


def main(argv):
    inputfile = None
    outputfile = None
    lang = None
    enc = 'UTF-8'
    log = False
    log_file = False
    report_freq = 1000
    cmd_line = 'filter.py -i <inputfile> -o <outputfile> -l <lang> (-v)'

    try:
        opts, args = getopt.getopt(argv, "vl:i:o:", ["ifile=", "ofile=", "lang=", "verbose"])
    except getopt.GetoptError:
        print(cmd_line)
        print(argv)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(cmd_line)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            # text file containing a list of path to bz2 files to process
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            # Suffix to add to input file in order to output results
            outputfile = arg
        elif opt in ("-l", "--lang"):
            # Language tags to use
            lang = arg
        elif opt in ("-v", "--verbose"):
            # log each article title
            log_file = True

    # Sanity check if all mandatory parameters are there
    if not lang or not inputfile or not outputfile:
        print("Missing parameter")
        print(cmd_line)
        sys.exit(2)

    # read the file list and run them
    files = open(inputfile).readlines()

    for infile in files:
        if not infile or infile == '':
            continue

        start = time.time()
        infile = infile.rstrip()

        # Download it if needed
        fname = os.path.basename(infile)
        if not os.path.exists(fname):
            print("Downloading file : " + fname)
            download_file(infile)
            print("Finished!")
        else:
            print("File " + fname + " already downloaded!")

        if log_file:
            pov = POVProcessor("data/tags." + lang + ".txt", enc, outputfile, fname + ".log")
        else:
            pov = POVProcessor("data/tags." + lang + ".txt", enc, outputfile, None)
        cptPage = 0
        cptLine = 0
        zip = bz2.BZ2File(fname)
        store = False
        fullpage = StringBuilder()
        for line in zip:
            line = line.decode(enc)

            if store:
                fullpage.append(line)
                if line == "  </page>\n":
                    # process it
                    pov.extract(fullpage.to_string())
                    fullpage = StringBuilder()
                    store = False
                    cptPage += 1
                    if cptPage % report_freq == 0:
                        print(str(cptPage) + " pages processed...")

                elif line.startswith("    <ns>") and not line == "    <ns>0</ns>\n":
                    # Other types of pages
                    fullpage = StringBuilder()
                    store = False

            elif line == "  <page>\n":
                store = True
                fullpage = StringBuilder()
                fullpage.append(line)

        pov.write_tags()
        end = time.time()
        zip.close()

        # Delete the file
        os.remove(os.path.basename(fname))
        print("Execution time : " + str((end - start) / 60) + " min")


if __name__ == "__main__":
    main(sys.argv[1:])

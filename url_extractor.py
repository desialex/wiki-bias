import urllib.request, urllib.error, urllib.parse
import sys
import getopt
import re


def main(argv):
    """
    Fetch the wikipedia dump page and extract the (list of) file(s) containing the full revision history of all articles
     and output it to a single file for the next step.
    :param argv: commandline parameters for the execution
    :return:
    """

    outpufile = None
    lang = None
    date = None
    baseurl = 'https://dumps.wikimedia.org'
    help_string = 'UrlExtractor.py -o <outputfile> -l <lang> -d <date>'
    try:
        opts, args = getopt.getopt(argv, "l:o:d:", ["ofile=", "lang=", "date"])
    except getopt.GetoptError:
        print(help_string)
        print(argv)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-o", "--ofile"):
            # full path to output the url list into
            outpufile = arg
        elif opt in ("-l", "--lang"):
            # Two-letters language tag to fetch
            lang = str(arg).strip()
        elif opt in ("-d", "--date"):
            # The exact wikipedia archive date (YYYMMDD)
            date = str(arg).strip()

    # Sanity check
    if not outpufile or not lang or len(lang) != 2 or not date or len(date) != 8:
        print(help_string)
        sys.exit(2)

        # Download page
    response = urllib.request.urlopen(baseurl + "/" + lang + "wiki/" + date + "/")
    page = response.read()

    # Fetch the matching url for the complete page edit history in bz2 format
    linkpattern = r"(\/" + lang + r"wiki\/" + date + r"\/" + lang + "wiki-" + date + \
                  r"-pages-meta-history\d{0,3}\.xml(-p\d{1,9}p\d{1,9})?\.bz2)"
    matches = re.findall(linkpattern, page.decode("UTF-8"))

    # Write them to the output file
    cpt = 0
    with open(outpufile, "w+") as f:
        for m in matches:
            cpt += 1
            f.write(baseurl + m[0] + "\n")

    print(str(cpt) + " url(s) generated")


if __name__ == "__main__":
    main(sys.argv[1:])

import zipfile
import optparse
from threading import Thread


def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password.encode('ascii'))  # python3中pwd需要的是byte
        print('[+] Fonud Password : ' + password + '\n')
    except:
        pass


def main():

    parser = optparse.OptionParser(
        "[*] Usage: ./unzip.py -f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',
                      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',
                      help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)

    zFile = zipfile.ZipFile(options.zname)
    with open(options.dname) as passFile:
        for line in passFile:
            line = line.strip('\n')
            t = Thread(target=extractFile, args=(zFile, line))
            t.start()


if __name__ == '__main__':
    main()

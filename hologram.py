import csv
import os
import sys
import tldextract
from urllib.parse import urlparse
from urllib.parse import unquote

# Takes N documents containing URLs from the command line, processes URLs
# and creates folders from those URLs TLDs
# If there are filenames in the path, it will move those files into the folders
# Documents is expected to be .csv, comma-delimited, with one column
# Values are expected to be fully qualified URLs, including the schema

filenames =[]
folders = []
files_moved = 0
folders_created = 0

for filename in sys.argv[1:]:
    print ("Processing file",filename,"...")
    f = open(filename)
    csv_f = csv.reader(f)

    #Parse Input file and Get URLs and Filenames of Downloads
    for row in csv_f:
        
        #Decode URL, Parse URL for Path, and truncate to filename
        #Then Add filename to array filenames
        filename = unquote(row[0])
        filename = urlparse(filename).path
        filename = filename.split('/')[-1]
        filename = filename.split('/')[-1]
        filenames.append(filename)
    
        #Call urlparse to separate out the url into scheme, netloc, path, etc.
        parsed_uri = urlparse(row[0])
        
        #Recombine the scheme and the netloc so we can check agianst the gTLD list
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    
        #Extract just the domain using a TLD lookup, i.e. tldextract...
        ext = tldextract.extract(domain)
    
        #Append Cleansed Domains into the URLs array 
        folders.append(ext.domain)
    print(filenames)
    

    for folder,filename in zip(folders,filenames):
        if not (os.path.isdir(folder) or os.path.exists(folder)):
            print("making directory",folder)
            os.mkdir(folder)
            folders_created +=1
        if os.path.exists(filename):
            if os.path.exists(folder):
                os.rename(filename,folder+"/"+filename)
                files_moved +=1

print (files_moved,"files moved into ",folders_created,"folders.")
print ("Done.")
f.close()
    
    
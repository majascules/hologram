import csv
import os
import sys
import tldextract
import time
from urllib.parse import urlparse
from urllib.parse import unquote

# Takes N documents containing URLs from the command line, processes URLs
# and creates folders from those URLs TLDs
# If there are filenames in the path, it will move those files into the folders
# Documents is expected to be .csv, comma-delimited, with one column
# Values are expected to be fully qualified URLs, including the schema

start_time=time.time()
end_time=0
destination=sys.argv[2]
filenames =[]
folders = []
files_moved = 0
folders_created = 0

print ("Processing file",sys.argv[1],"...")

f = open(sys.argv[1])
csv_f = csv.reader(f)

#Parse Input file and Get URLs and Filenames of Downloads
for row in csv_f:
    
    #Decode URL, Parse URL for Path, and truncate to filename
    #Then Add filename to array filenames
    filename = unquote(row[0])
    filename = urlparse(filename).path
    filename = filename.split('/')[-1]
    filename = filename.split('?')[-1]
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
"""for folder,filename in zip(folders,filenames):
        if not os.path.isdir(destination+folder):
            print ("making directory",destination+folder)
            os.mkdir(destination+folder)
            folders_created +=1
        else:
            print (folder,"exists, skipping")
            
        if os.path.exists(destination+filename):
            if os.path.exists(destination+folder):
                os.rename(destination+filename,destination+folder+"/"+filename)
                files_moved +=1
            else:
                print ("error:",destination+folder,"does not exist")
        else:
            print ("error:",destination+filename,"listed file doest not exist")


print (files_moved,"files moved into ",folders_created,"folders in",time.time()-start_time,"seconds")
print ("Done.")

"""
f.close()
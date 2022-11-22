import urllib.request

local_filename, headers = urllib.request.urlretrieve('https://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/variants/homo_sapiens_variation.txt.gz', 'homo_sapiens_variation.txt.gz')

data = open(local_filename)

print(type(data))
print(data)

data.close()


# with open('homo_sapiens_variation.txt', 'r') as file_f:
#     with open('out_uniprot.txt', 'w') as outfile:
#         fctr = 0
#         for line in file_f:
#             if fctr < 300:
#                 print(line)
#                 outfile.write(line)
#                 fctr = fctr + 1
            
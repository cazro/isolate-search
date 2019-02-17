# If you start with an Excel spreadsheet of isolates then export it to a CSV file.
# Change the variables below for the isolate file name and the column #s of the specific data in the CSV file.
# Created by Eric King (edk@ericdavidking.com)

import csv
import urllib.request
import json
import xml.etree.ElementTree as ET
import time

isolate_file_name = "isolates.csv"

isolate_col = 16

isolate_source_name = "isolation_source"
isolate_source_col = 15

strain_name = "strain"
strain_col = 27

collected_by_name = "collected_by"
collected_by_col = 28

collection_date_name = "collection_date"
collection_date_col = 29

geoloc_name = "geo_loc_name"
geoloc_col = 30

host_name = "host"
host_col = 31

host_disease_name = "host_disease"
host_disease_col = 32

biomat_name = "biomaterial_provider"
biomat_col = 33

sample_type_name = "sample_type"
sample_type_col = 34

lat_lon_name = "lat_lon"
lat_lon_col = 35

cult_collect_name = "culture_collection"
cult_collect_col = 36

genotype_name = "genotype"
genotype_col = 37

host_tissue_name = "host_tissue_sampled"
host_tissue_col = 38

replicate_name = "replicate"
replicate_col = 39

carbon_source_name = "carbon source"
carbon_source_col = 40

taxid_name = "taxid"
taxid_col = 41

pirnay_name = "pirnay_name"
pirnay_col = 42

note_name = "note"
note_col = 43

num_extra_cols = 17

try:
	with open(isolate_file_name, 'r', newline='') as csvfile, open(isolate_file_name+'-output.csv', 'w') as csvoutput:
		isolates = csv.reader(csvfile, delimiter=',')
		csvwriter = csv.writer(csvoutput, lineterminator='\n')

		combined = []

		for row in isolates:
			
			isolate = row[isolate_col]
			if isolate.find('(') is not -1:
				isolate = isolate[:isolate.index('(')]
				isolate = '+'.join(isolate.split())
				try:
					sresponse = urllib.request.urlopen("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=biosample&term="+isolate+"&retmode=json")
				except:
					print("THERE WAS AN ERROR DOING A SEARCH")
				jdata = json.loads(sresponse.read().decode())
				if jdata['esearchresult']['idlist']:
					id = jdata['esearchresult']['idlist'][0]
					try:
						time.sleep(1)
						fresponse = urllib.request.urlopen("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id="+id)
					except:
						print("THERE WAS AN ERROR GETTING THE DATA")
						
					xmlroot = ET.fromstring(fresponse.read().decode())
					num_attr = 1
					count = 0
					while count < num_extra_cols:
						row.append("")
						count += 1
						
					for child in xmlroot[0][5]:
						if "attribute_name" in child.attrib:
							if child.attrib['attribute_name'] == isolate_source_name:
								temp = row[isolate_source_col].strip()
								
								if temp:
									if temp.lower() == child.text.strip().lower():
										row[isolate_source_col] = temp
									else:
										row[isolate_source_col] = temp + ' OR ' + child.text + '(from script)'
								else:
									row[isolate_source_col] = child.text
							elif child.attrib['attribute_name'] == strain_name:
								row[strain_col] = child.text
							elif child.attrib['attribute_name'] == collected_by_name:
								row[collected_by_col] = child.text
							elif child.attrib['attribute_name'] == collection_date_name:
								row[collection_date_col] = child.text
							elif child.attrib['attribute_name'] == geoloc_name:
								row[geoloc_col] = child.text
							elif child.attrib['attribute_name'] == host_name:
								row[host_col] = child.text
							elif child.attrib['attribute_name'] == host_disease_name:
								row[host_disease_col] = child.text
							elif child.attrib['attribute_name'] == biomat_name:
								row[biomat_col] = child.text
							elif child.attrib['attribute_name'] == sample_type_name:
								row[sample_type_col] = child.text
							elif child.attrib['attribute_name'] == lat_lon_name:
								row[lat_lon_col] = child.text
							elif child.attrib['attribute_name'] == cult_collect_name:
								row[cult_collect_col] = child.text
							elif child.attrib['attribute_name'] == genotype_name:
								row[genotype_col] = child.text
							elif child.attrib['attribute_name'] == host_tissue_name:
								row[host_tissue_col] = child.text
							elif child.attrib['attribute_name'] == replicate_name:
								row[replicate_col] = child.text
							elif child.attrib['attribute_name'] == carbon_source_name:
								row[carbon_source_col] = child.text
							elif child.attrib['attribute_name'] == taxid_name:
								row[taxid_col] = child.text
							elif child.attrib['attribute_name'] == pirnay_name:
								row[pirnay_col] = child.text
							else:
								row.append(child.attrib['attribute_name']+': '+child.text)
								
							print(child.attrib['attribute_name'],child.text)
				combined.append(row)
			time.sleep(1)
		csvwriter.writerows(combined)
except:
	print("PROBLEM WITH READING/WRITING FILES")
	csvwriter.writerows(combined)


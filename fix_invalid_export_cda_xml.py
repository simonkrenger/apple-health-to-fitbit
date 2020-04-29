#!/usr/bin/env python3

# Hacky script to fix an invalid export_cda.xml file
#
# For some reason, in some cases the Apple Health Export file export_cda.xml
# can be in the following format:
#
# <?xml version="1.0"?>
# <?xml-stylesheet type="text/xsl" href="CDA.xsl"?>
# <ClinicalDocument ...>
#  <entry typeCode="DRIV">
#   <organizer ...>
#    [..]
#    <component>
#      ... DATA HERE ...
#    </component>
#    <component>
#      ... DATA HERE ...
#    </component>
#   </organizer>
#  </entry>
# </ClinicalDocument>
# <component>
#  <section>
#   <entry ...>
#    <organizer ...>
#     <component>
#        ... DATA HERE ...
#     </component>
#     [..]
#    </organizer>
#   </entry>
#  </section>
# </component>
#
# As there are clearly two root elements, the file cannot be parsed. This
# script splits the document in two and merges the lower part of the document
# back into the ClinicalDocument, resulting in a valid XML document again. This
# valid document can then be parsed by the other scripts in this repository.

import os.path
import xml.etree.ElementTree as ET

EXPORT_CDA_FILE = 'export_cda.xml'

if not os.path.exists(EXPORT_CDA_FILE):
  print("Error: export_cda.xml not found.")
  exit(1)

is_invalid_document = False
try:
  export_cda = ET.parse(EXPORT_CDA_FILE)
except ET.ParseError as error:
  print("Confirmed invalid XML (ParseError)")
  is_invalid_document = True

if not is_invalid_document:
  print("export_cda seems to be valid, refusing to do anything...")
  exit(1)

confirm = input("Are you sure you want to try to fix your export_cda.xml? This will overwrite your current export_cda.xml. Confirm with 'yes': ")
if confirm.lower() != "yes":
  print("Exited")
  exit(1)

# Script starts here

print("Processing 'export_cda.xml'...")

processing_clinical_document = True
clinical_document = ""
new_document = "<?xml version=\"1.0\"?>\n"
new_document += '<?xml-stylesheet type="text/xsl" href="CDA.xsl"?>\n'
new_document += '<DummyRoot xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:hl7-org:v3 ../../../CDA%20R2/cda-schemas-and-samples/infrastructure/cda/CDA.xsd" xmlns="urn:hl7-org:v3" xmlns:cda="urn:hl7-org:v3" xmlns:sdtc="urn:l7-org:sdtc" xmlns:fhir="http://hl7.org/fhir/v3">\n'
with open(EXPORT_CDA_FILE, "r") as export_cda_filehandler:
  for line in export_cda_filehandler:
      if processing_clinical_document:
        if line == "</ClinicalDocument>\n":
          print("Found end of ClinicalDocument.")
          clinical_document += line
          processing_clinical_document = False
        else:
          clinical_document += line
      else:
        new_document += line
new_document += '</DummyRoot>'

print("Done processing.")
print("Parsing the ClinicalDocument...")
clinical_document_root = ET.fromstring(clinical_document)
clinical_document = None

print("Parsing the rest of the document...")
new_document_root = ET.fromstring(new_document)
new_document = None

print("Done. Now merging the two parts into the ClinicalDocument...")
for component in new_document_root.findall('{urn:hl7-org:v3}component'):
  for section in component.findall('{urn:hl7-org:v3}section'):
    for entry in section.findall('{urn:hl7-org:v3}entry'):
      clinical_document_root.append(entry)

with open(EXPORT_CDA_FILE, "wb") as f:
  f.write(ET.tostring(clinical_document_root, encoding='UTF-8', method='xml'))

print("Success")
exit(0)
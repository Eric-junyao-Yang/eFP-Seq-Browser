import openpyxl

f = open('submission_parse.html','w')
wb = openpyxl.load_workbook('bulk_template.xlsx')
sheet = wb.get_sheet_by_name('Data sheet')
all_rows = tuple(sheet.rows)

# Store string to be written into html file after all content is read.
total_XML = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script src="XMLgenerator-v2.js"></script>
<div class="SubmissionArea">
"""

# Iterate through each entry and corresponding cells.
for row in range(1, len(all_rows)):
    crow = all_rows[row] # Current entry
    total_XML += """
<div class="Entries" name="Entries">
<legend class="leftmargin"> Entry </legend>
    <form class="form">
        <fieldset>"""

    for x in range(1, 12):
        ccell = crow[x].value

# Prints alert to user if cell is empty. 
# Note: As of now, it's just printed, but this could be incorporated into the UI in the future (perhaps a popup?)
        if ccell is None:
            print("Input missing from Entry " + str(row) + ", column " + str(x))

# Stores content of each cell in a HTML wrapper
# form field is set to column index number (would need to be manually changed if template is changed)
        else:
            if x == 1:
                total_XML += """
                <div class='forminput'>
                    <input class='channelspecies' name='channelspecies' data-help-text='species' value='""" + ccell + """'/>
                </div>"""

            elif x == 2:
                total_XML += """
                <div class='forminput'>
                    <input class='channeltitle' name='channeltitle' data-help-text='title' value='""" + ccell + """'/>
                </div>"""

            elif x == 3: #how to validate BAM link?
                total_XML += """
                <div class='forminput'>
                    <input class='channelbamlink' name='channelbamlink' data-help-text='bam_link' value='""" + ccell + """'/>
                </div>"""

            elif x == 4:
                total_XML += """
                <div class='forminput'>
                    <input class='channelpublicationlink' name='channelpublicationlink' data-help-text='publication_link' value='""" + ccell + """'/>
                </div>"""

            elif x == 5 and ("ncbi" or "NCBI" in ccell):
                total_XML += """
                <div class='forminput'>
                    <input class='channelpublicationurl' name='channelpublicationurl' data-help-text='publication_url' value='""" + ccell + """'/>
                </div>"""

            elif x == 6:
                total_XML += """
                <div class='forminput'>
                    <input class='channeltotalreadsmapped' name='channeltotalreadsmapped' data-help-text='svgname' value='""" + str(ccell) + """'/>
                </div>"""

            elif x == 7 and ".svg" in ccell:
                total_XML += """
                <div class='forminput'>
                    <input class='channelsvgname' name='channelsvgname' data-help-text='total_reads_mapped' value='""" + ccell + """'/>
                </div>"""

            elif x == 8:
                total_XML += """
                <div class='forminput'>
                    <input class='channeltissue' name='channeltissue' data-help-text='tissue' value='""" + ccell + """'/>
                </div>"""

            elif x == 9:
                total_XML += """
                <div class='forminput'>
                    <input class='channelcontrols' name='channelcontrols' data-help-text='total_controls' value='""" + ccell + """'/>
                </div>"""

            elif x == 10:
                replicates = ccell.split(", ")

# Checks to make sure they don't have over 5 replicates.
                if len(replicates) > 5:
                    print("Sorry, you have over 5 replicates in Entry " + str(row))

                else:
                    k = 1
                    for i in replicates: # Populate w/ each replicate.

                        if replicates.index(i) == 0:
                            total_XML += """
                <div class='forminput'>
                    <input class='channelgroupwidtho' name='channelgroupwidtho' data-help-text='groupwidth' value='""" + i + """'/>
                </div>"""
                            k += 1
                        else:    
                            total_XML += """
                <div class='forminput'>
                    <input class='channelgroupwidth""" + str(k) + "' name='channelgroupwidth""" + str(k) + "' data-help-text='groupwidth' value='""" + i + """'/>
                </div>"""
                            k += 1

# Add in the remaining empty replicates.
                    j = k
                    for x in range(len(replicates), 5):

                        total_XML += """
                <div class='forminput'>
                    <input class='channelgroupwidth""" + str(j) + "' name='channelgroupwidth""" + str(j) + """' data-help-text='groupwidth' value=''/>
                </div>"""
                        j += 1


            elif x == 11:
                 total_XML += """
                <div class='forminput'>
                    <input class='channeldescription' name='channeldescription' data-help-text='description' value='""" + ccell + """'/>
                </div>"""

    total_XML += """
        </fieldset>
    </form>
</div>
"""


total_XML += """
</div>
<div id="Cloning" class="button_fixed">
    <p>
        <button id="SubmitButton">Generate XML</button>
    </p>
</div>
<div id="generated" style="display:none">
  <h2>bamdata.xml</h2>
  <a href="#" id="DownloadLink">Download XML</a>
  <textarea id="ResultXml" style="width: 100%; height: 30em" readonly="readonly"></textarea>
</div>
</html>"""

print (total_XML) # Testing purposes

f.write(total_XML)
f.close()




import csv
writer = csv.writer(open("site_address_done.csv", "wb"), quoting=csv.QUOTE_NONE)
reader = csv.reader(open("site_address_squeeze.csv", "rb"), skipinitialspace=True)
writer.writerows(reader)

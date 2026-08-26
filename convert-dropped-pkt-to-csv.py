import re
import csv

input_file = "/home/lalan/Desktop/WorkingD/AdHoc-R/AdHoc-RelNT-Server/Reno/Buffer/qdis/Throu/1M/Reno_1M_Throu_qdisc_15.txt"   # your .txt file
output_file = "/home/lalan/Desktop/WorkingD/AdHoc-R/AdHoc-RelNT-Server/Reno/Buffer/qdis/Throu/1M/Reno_1M_Throu_qdisc_15.csv"

# Regex to capture dropped values
pattern = re.compile(r"dropped\s+(\d+)")

dropped_values = []

# Read file and extract values
with open(input_file, "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            dropped_values.append(int(match.group(1)))

# Write to CSV
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Dropped"])  # header
    for value in dropped_values:
        writer.writerow([value])

print("Extraction complete. Data saved to output.csv")

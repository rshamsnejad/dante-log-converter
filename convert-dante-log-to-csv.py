import os.path
import csv
import re
import sys

if len(sys.argv) != 2:
    print("Wrong arguments !")
    sys.exit(1)

log_filename = sys.argv[1]
csv_filename = os.path.splitext(log_filename)[0] + ".csv"

try:

    log_file = open(log_filename, 'r')
    csv_file = open(csv_filename, 'w', newline='')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Date", "Timezone", "Timestamp", "Log Level", "Device", "Message"])

    for line in log_file:

        # Skip the useless first line
        if line.startswith("Dante Controller Event Log"):
            continue

        row_split = re.split(r'\s', line.strip(), maxsplit=6)
        
        row = [
            f"{row_split[0]} {row_split[1]}",
            row_split[2],
            row_split[3],
            row_split[4],
            row_split[5].strip('"'),
            row_split[6].strip('"'),
        ]

        # In case the device field is empty, fill it with the MAC address from the message
        if not row[4]:
            message_split = re.split(r'(device name not known)',row[5])[0].strip()

            row[4] = message_split.split(' ')[1]

        csv_writer.writerow(row)

    log_file.close()
    csv_file.close()

except Exception as e:
    print(e)
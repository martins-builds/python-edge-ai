import csv

min_lat, max_lat = float('inf'), float('-inf')
min_lon, max_lon = float('inf'), float('-inf')
sn = 1

with open("gps_log_2026-10-08.txt", "r") as file, open("gps_data.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["time_str", "decimal_degrees", "decimal_longitude"])

    count = 0
    total_lines = 0
    valid_lines = 0
    corrupted_lines = 0
    for line in file:
        total_lines += 1
        clean_line = line.strip()
        if clean_line.startswith("$GPRMC"):
            fields = clean_line.split(",")
            if len(fields) < 7 or fields[2] == "V":
                continue
            valid_lines += 1
            time_str = fields[1]
            status_str = fields[2]
            latitude_str = fields[3]
            hemisphere1_str = fields[4]
            longitude_str = fields[5]
            hemisphere2_str = fields[6]

            degrees_str = latitude_str[:2]
            minutes_str = latitude_str[2:]
            decimal_degrees = float(degrees_str) + (float(minutes_str) / 60.0)
            if hemisphere1_str == "S":
                decimal_degrees = -decimal_degrees

            degrees = float(longitude_str[:3])
            minutes = float(longitude_str[3:])
            decimal_longitude = degrees + (minutes / 60.0)
            if hemisphere2_str == "W":
                decimal_longitude = -decimal_longitude

            min_lat = min(min_lat, decimal_degrees)
            max_lat = max(max_lat, decimal_degrees)
            min_lon = min(min_lon, decimal_longitude)
            max_lon = max(max_lon, decimal_longitude)

            writer.writerow([time_str, decimal_degrees, decimal_longitude])
            count += 1

with open("data_validity.csv", mode="+a", newline="") as vFile:
    writer = csv.writer(vFile)
    vFile.seek(0, 2)
    if vFile.tell() == 0:
        writer.writerow(["S/N", "Total lines", "Valid lines", "Corrupted lines"])
    corrupted_lines = total_lines - valid_lines
    writer.writerow([sn, total_lines, valid_lines, corrupted_lines])
    sn += 1

print(f"Successfully processed {count} records.")
if valid_lines > 0:
    print(f"Latitude bounds:   {min_lat:.6f} to {max_lat:.6f}")
    print(f"Longitude bounds:  {min_lon:.6f} to {max_lon:.6f}")
print(count)

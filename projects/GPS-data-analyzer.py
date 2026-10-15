with open("gps_log_2026-10-08.txt", "r") as file:
    count = 0
    for line in file:
        clean_line = line.strip()
        if clean_line.startswith("$GPRMC"):
            fields = clean_line.split(",")
            if len(fields) < 7 or fields[2] == "V":
                continue
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

            print(clean_line)
            count = count + 1
print(count)
with open("gps_log_2026-10-08.txt", "r") as file:
    count = 0
    for line in file:
        clean_line = line.strip()
        if clean_line.startswith("$GPRMC"):
            print(clean_line)
            count = count + 1
        print(count)

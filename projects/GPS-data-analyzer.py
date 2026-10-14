with open("gps_log_2026-10-08.txt", "r") as file:
    for line in file:
        clean_line = line.strip()
        #scan for bad lines
        print(clean_line)
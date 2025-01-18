with open("symbols.json", "w") as file:
    file.write("[\n")
    for i in range(16):
        file.write("\t{\n\t\t\"symbol\": \"R" + str(i) + "\",\n\t\t\"value\": " + str(i) + "\n\t},\n")
    file.write("\t{\n\t\t\"symbol\": \"SCREEN\",\n\t\t\"value\": 16384\n\t},\n")
    file.write("\t{\n\t\t\"symbol\": \"KBD\",\n\t\t\"value\": 24576\n\t}\n")
    file.write("]")
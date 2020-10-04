import requests, csv, urllib.parse, time

with open('schools_out.csv', 'r') as readerfile, open('locations_out.csv', 'w', newline='') as writerfile:
    reader = csv.reader(readerfile)
    writer = csv.writer(writerfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['wisid','school','location', 'latitude', 'longitude'])
    next(reader)
    counter = 0
    for row in reader:
        counter += 1
        address = row[1]
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
        response = requests.get(url).json()
        #print(response[0]["lat"])
        #print(response[0]["lon"])
        try:
            writer.writerow([row[0], row[1], row[2], response[0]["lat"], response[0]["lon"]])
        except Exception as e:
            print(f"{row[1]}: {e}")
        print(counter)
        time.sleep(1)
        if int(row[0]) == 49016:
            break
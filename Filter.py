from mrjob.job import MRJob
import re
import time
#Obtain the top 10 donors over the whole dataset for the Wikileaks bitcoin address
#first filter /data/bitcoin/vout.csv to only rows containing the wallet of interest
class Lab2(MRJob):
#hash, value, n, public_key
    def mapper(self, _, line):
        fields = line.split(",")
        try:
            if (len(fields)==4):
                public_key = fields[3]
                address = "{1HB5XMLmzFVj8ALj6mfBsbifRoD4miY36v}"
                if (public_key==address):
                    yield ("", line)
        except:
            pass

if __name__ == '__main__':
    Lab2.run()

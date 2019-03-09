from mrjob.step import MRStep
from mrjob.job import MRJob
import re
import time
#Obtain the top 10 donors over the whole dataset for the Wikileaks bitcoin address
#first filter /data/bitcoin/vout.csv to only rows containing the wallet of interest
class Lab2(MRJob):
#hash, value, n, public_key :vout
#txid, tx_hash, vout : vin
    sector_table = {}
    def mapper_join_init(self):
        with open("partBfilter.txt") as f:
            for line in f:
                fields = line.split("\t")
                lines = fields[1]
                lines_stripped = lines[1:-1]
                entries = lines_stripped.split(",")
                key = entries[0]#hash
                val = entries[1]#value/amount
                self.sector_table[key] = val

    def mapper_repl_join(self, _, line):
        fields = line.split(",")
        try:
            if (len(fields)==3):
                txid = fields[0]
                tx_hash = fields[1]
                vout = fields[2]
                if txid in self.sector_table:
                    amount = self.sector_table[txid]
                    yield (None,(txid,tx_hash,vout,amount))
        except:
            pass

    def steps(self):
        return [MRStep(mapper_init=self.mapper_join_init,
                        mapper=self.mapper_repl_join)]
#this part of the python script tells to actually run the defined MapReduce job. Note that Lab2 is the name of the class
if __name__ == '__main__':
    Lab2.run()

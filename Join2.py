from mrjob.step import MRStep
from mrjob.job import MRJob
import re
import time

class Lab2(MRJob):
#hash, value, n, public_key :vout
#txid, tx_hash, vout : vin
#tx_hash=hash, vout=n
#txid,tx_hash,vout,amount :partBjoin1.txt
    sector_table = {}
    def mapper_join_init(self):
        with open("partBjoin1.txt") as f:
            for line in f:
                fields = line.split("\t")
                lines = fields[1]
                entries = lines.split(",")
                key = entries[1][2:-1]#tx_hash
                val = entries[2][2:-1]#vout
                self.sector_table[key] = val

    def mapper_repl_join(self, _, line):
        fields = line.split(",")
        try:
            if (len(fields)==4):
                hash = fields[0]
                value = float(fields[1])
                n = fields[2]
                public_key = fields[3]
                if hash in self.sector_table:
                    if (n == self.sector_table[hash]):
                        yield (None,(public_key,value))
        except:
            pass

    def steps(self):
        return [MRStep(mapper_init=self.mapper_join_init,
                        mapper=self.mapper_repl_join)]
#this part of the python script tells to actually run the defined MapReduce job. Note that Lab2 is the name of the class
if __name__ == '__main__':
    Lab2.run()

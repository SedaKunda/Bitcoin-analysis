from mrjob.step import MRStep
from mrjob.job import MRJob
import re
import time

class top10(MRJob):
#hash, value, n, public_key :vout
#txid, tx_hash, vout : vin
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
                        yield (public_key, value)
        except:
            pass

    def reducer(self, feature, value):
        yield(feature, sum(value))
        
#make it a tuple again
    def mapper_tuple(self, feature, value):
        yield(None, (feature, value))

    def reducer_top10(self, feature, values):
        sorted_values = sorted(values, reverse=True, key=lambda x: x[1])[:10]
        for value in sorted_values:
            yield(feature, value)

    def steps(self):
        return [MRStep(mapper_init=self.mapper_join_init,
                       mapper=self.mapper_repl_join,
                       reducer=self.reducer),
                MRStep(mapper=self.mapper_tuple,
                       reducer=self.reducer_top10)]

if __name__ == '__main__':
    top10.run()

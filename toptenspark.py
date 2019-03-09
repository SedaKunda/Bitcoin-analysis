#get top ten using spark only
import pyspark
import re

sc = pyspark.SparkContext()
#tx_hash=hash, vout=n
#hash, value, n, public_key :vout
#txid, tx_hash, vout:vin
def is_good_line_vin(line):
    try:
        fields = line.split(',')
        if len(fields)!=3:
            return False
        return True
    except:
        return False

def is_good_line_vout(line):
    try:
        fields = line.split(',')
        if len(fields)!=4:
            return False
        return True
    except:
        return False

def is_required_key(line):
    try:
        fields = line.split(',')
        public_key = fields[3]
        address = "{1HB5XMLmzFVj8ALj6mfBsbifRoD4miY36v}"
        if (public_key!=address):
            return False
        return True
    except:
        return False

#filter
vout_lines = sc.textFile("/data/bitcoin/vout.csv")#hash, value, n, public_key
clean_vout_lines = vout_lines.filter(is_good_line_vout)#check if vout has correct columns
new_vout_lines = clean_vout_lines.filter(is_required_key)#filter required wikileaks key
filter=new_vout_lines.map(lambda l: (l.split(',')[0],l.split(',')[1]))#hash,value

#join1
vin_lines = sc.textFile("/data/bitcoin/vin.csv")
clean_vin_lines = vin_lines.filter(is_good_line_vin)
vin=clean_vin_lines.map(lambda l: (l.split(',')[0],(l.split(',')[1], l.split(',')[2])))#txid, txhash, vout
join1 = vin.join(filter)#(hash/txid,((vout,txhash),value))

#join2
join1_clean=join1.map(lambda l: (l[1]))#((tx_hash, vout), value)
vout=clean_vout_lines.map(lambda l: ((l.split(',')[0], l.split(',')[2]), (l.split(',')[3],l.split(',')[1])))#((hash, n), (public_key,value)))
join2 = vout.join(join1_clean)#((txhash/hash,n/vout), ((public_key, value), value))

#top10
clean_inner_join = join2.map(lambda l : (l[1][0][0],float(l[1][0][1])))#(public_key, value)
top_ten = clean_inner_join.takeOrdered(10, key = lambda l: -l[1])
top_ten_ans = sc.parallelize(top_ten)
top_ten_ans.saveAsTextFile("topten")
#print(top_ten)

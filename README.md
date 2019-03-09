# Bitcoin-analysis
Analyse a subset of the bitcoin blockchain, ranging from the first mined bitcoin in 2009 to December 2014
#full data sets available online

DATASET OVERVIEW
Bitcoin is a decentralised digital currency that enables instant payments to anyone, anywhere in the world. Bitcoin uses public-key cryptography, peer-to-peer networking, and proof-of-work to process and verify payments. Bitcoins are sent from one address (wallet) to another, with each transaction broadcast to the network and included in the blockchain so that the bitcoins cannot be spent twice. A subset of the blockchain (Blocks 1 to ~330000) has been collected and saved to HDFS at /data/bitcoin. These blocks have been changed from their original raw json format by splitting them into five comma delimited csv files: blocks.csv; transactions.csv; coingen.csv (Coin Generations/Mined coins); vin.csv; and vout.csv. To explain what these files contain a description and schema can be found below:

DATASET DESCRIPTION
At any one point in time one bitcoin block exists, linked to a mathematical problem. While miners race to solve this problem the block records all transactions taking place while it remains unsolved (transactions.csv). Each time a block is completed it becomes a permanent record of these past transactions and gives way to a new block in the blockchain (blocks.csv).

When a winning miner solves a block's problem, the answer is shared with other mining nodes and validated. Every time a miner solves a problem a set amount of BTC (Bitcoin currency symbol) is awarded to the miner and enters circulation (coingen.csv). The first record in the next block is a transaction that awards the winning miner this newly minted BTC.

Each transaction tracks the bitcoin amounts being transferred, the source transaction(s) of the coins (vin.csv) and the destination wallet(s) (vout.csv). This allows each BTC to be tracked from the latest transaction it was involved in, right back to when it was minted.

Sample files for transactions.csv, vin.csv and vout.csv can be found on the module homepage. These may be used to test your code for the first two parts of the coursework.

DATASET SCHEMA
BLOCKS.CSV
height: The block number
hash: The unique ID for the block
time: The time at which the block was created (Unix Timestamp in seconds)
difficulty: The complexity of the math problem associated with the block
Sample entry:
    0, 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f,  1231006505,  1

TRANSACTIONS
tx_hash: The unique id for the transaction
blockhash: The block this transaction belongs to
time: The time when the transaction occurred
tx_in_count: The number of transactions with outputs coming into this transaction
tx_out_count: The number of wallets receiving bitcoins from this transaction
Sample entry: 0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098,00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048,1231469665,1,1

COINGEN
db_id: The block the coin generation was found within (maps to block height not hash)
tx_hash: Transaction id for the Coin Generation
coinbase: Input of a generation transaction. As a generation transaction has no parent and creates new coins from nothing, the coinbase can contain any arbitrary data (or perhaps a hidden meaning).
sequence: Allows unconfirmed time-locked transactions to be updated before being finalised
Sample entry:
    1,  0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098,  04ffff001d0104,  4294967295

VIN
txid: The associated transaction the coins are going into
tx_hash: The transaction the coins are coming from
vout: The ID of the output from the previous transaction - the value equals n in vout below
Sample entry:
    f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16,0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9,0

VOUT
hash: The associated transaction
value: The amount of bitcoins sent
n: The id for this output within the transaction. This will equal the vout field within the vin table above, if the coins have been respent
publicKey: The id for the wallet where the coins are being sent
Sample entry:
    0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098, 50, 0, {12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX}

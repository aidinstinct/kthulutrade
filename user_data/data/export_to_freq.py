
import sys, os, glob, asyncio, pymongo, gridfs, json, re, pandas, logging
from csv import reader

#Get rid of scientific notation for freqtrade
#Second unix timestamp => Millisecond

#floating point notation is 8 digits for volume column
def pretty_float_json_dumps(json_obj):
    dumps_str = ""
    if isinstance(json_obj, dict): 
        dumps_str += "{"
        for k,v in json_obj.items():
            dumps_str += json.dumps(k)+":"
            if isinstance(v, float): 
                float_tmp_str = ("%.8f" % v).rstrip("0")
                dumps_str += (float_tmp_str+'0' if float_tmp_str.endswith('.') else float_tmp_str) + ','
            elif isinstance(v, list) or isinstance(v, dict): 
                dumps_str += pretty_float_json_dumps(v)+','
            else:
                dumps_str += pretty_float_json_dumps(v)+','
        if dumps_str.endswith(','):
            dumps_str = dumps_str[:-1]
        dumps_str += "}"
    elif isinstance(json_obj, list): 
        dumps_str += "["
        for v in json_obj:
            if isinstance(v, float): 
                float_tmp_str = ("%.8f" % v).rstrip("0")
                dumps_str += (float_tmp_str+'0' if float_tmp_str.endswith('.') else float_tmp_str) + ','
            elif isinstance(v, list) or isinstance(v, dict): 
                dumps_str += pretty_float_json_dumps(v)+','
            else:
                dumps_str += pretty_float_json_dumps(v)+','
        if dumps_str.endswith(','):
            dumps_str = dumps_str[:-1]
        dumps_str += "]"
    else:
        dumps_str += json.dumps(json_obj)
    return dumps_str

def floatify(thisdir):
    with open(f'{thisdir}/tmp/{sys.argv[2]}', 'r') as read_obj:
        try:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            for row in csv_reader:
                yield [float(i) for i in row]

            # Pass reader object to list() to get a list of lists
            #print(list_of_rows)
            #convert from seconds to milliseconds Unix Timestamp
        except Exception as e:
            print(e)

def buildJson():
    thisdir = sys.argv[4]

    #get_coins = ['XBT', 'ETH', 'ADA', 'MLN', 'EWT', 'AAVE', 'ALGO', 'ATOM', 'BCH', 'EOS', 'ETC', 'KAVA', 'KSM', 'LINK', 'LTC', 'MANA', 'MLN', 'QTUM', 'STORJ', 'WAVES', 'XTZ', 'USDT']
    get_coins = ['XBT', 'ETH', 'ADA', 'MLN', 'EWT', 'AAVE', 'ALGO', 'ATOM', 'BCH', 'EOS', 'ETC', 'KAVA', 'KSM', 'LINK', 'LTC', 'MANA', 'MLN', 'QTUM', 'STORJ', 'WAVES', 'XTZ', 'USDT']
    #coin = sys.argv[3]
    # read csv file as a list of lists
    #Kraken data has unix timestamp from second but it needs to be milliseconds, you add three trailing zeros to timestamp column value
    out = []
    coin = sys.argv[3]
    name = sys.argv[1]
    
    obj = floatify(thisdir)
    for index in obj:
        index[0]=int(index[0]*1000)
        out.append(index)

    export = json.dumps(pretty_float_json_dumps(out), separators=(',', ':')).replace('"', '')
    export.replace(' ', '')
    before, during, after = sys.argv[1].partition(coin)
    one_ = coin

    this = after.split('_')
    two_ = this[0]
    if one_ == 'XBT':
        one_ = 'BTC'
    #coin2 = re.search(j+r'\w+(?<=_)', sys.argv[1])

    e = re.split(r'[A-z]+', name)

    #get the nameing convention for freqtrade data sets
    if((1440 > int(e[1].replace('.', '')) >= 60)):
        interval = str(int(int(e[1].replace('.', ''))/60))+'h'
    elif((int(e[1].replace('.', ''))<60)):
        interval = str(int(int(e[1].replace('.', ''))))+ 'm'
    elif((int(e[1].replace('.', ''))==1440)):
        interval =  '1d'


    f = open(f"{thisdir}/kraken/{one_}_{two_}-{interval}.json", 'w')
    #pair = f'{one_}_{two_}'
    #set_ = {pair : out}
    f.write(export)
    
    f.close()  
    with open(f"{thisdir}/kraken/{one_}_{two_}-{interval}.json") as f:
        #mongoDB support
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["freq_kraken"]
        fs = gridfs.GridFS(mydb, collection=f'{one_}/{two_}')
        fs.put(f.read(), encoding='utf-8') 
        
        

buildJson()

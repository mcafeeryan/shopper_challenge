import datetime as dt
import os.path
import csv

data_dir = os.path.join('..','data_files')
offer_fname = 'offers.csv'
transaction_fname = 'reduced.csv'
trainHistory_fname = 'trainHistory.csv'

transactions = csv.DictReader( open(os.path.join(data_dir,transaction_fname), 'rb'))
trainHistory = csv.DictReader( open(os.path.join(data_dir,trainHistory_fname), 'rb'))
offers = csv.DictReader( open(os.path.join(data_dir, offer_fname), 'rb') )

out_fname = 'shopper_data.csv'
outfile = open(os.path.join( data_dir, out_fname ), 'wb')

# ----- Read in offers -----
offer_dict = {}
for row in offers:
    offer_dict[row['offer']] = row

# ----- Merge offers with shoppers -----
shopper_dict = {}
for row in trainHistory:
    offer = offer_dict[row['offer']]
    shopper_dict[row['id']] = dict( row.items() + offer.items() )

# ----- Extract features from transaction history -----
row = transactions.next()
complete = False
while not complete:
    row_id = row['id']
    new_id = row_id

    try:
        shopper_data = shopper_dict[row_id]
    except KeyError:
        try:
            row = transactions.next()
            i += 1
            new_id = row['id']
        except StopIteration:
            break
    else:
        offer_date = dt.datetime.strptime( shopper_data['offerdate'] , '%Y-%m-%d').date()
        levels = ['company', 'brand', 'category']
        metrics = ['_recency','_frequency', '_monetary']

        while new_id == row_id:
            date = row['date']
            trans_date = dt.datetime.strptime( date , '%Y-%m-%d').date()

            # Filter out 
            if (offer_date - trans_date) < dt.timedelta(days = 365) and (offer_date - trans_date) > 0:
                # Average basket size
                        shopper_data[ 

                        # Homogeneity of type

                for lvl in levels:
                    if row[lvl] == shopper_data[lvl] and offer_date != trans_date:
                        # Recency
                        recency = offer_date - trans_date
                        shopper_data[ lvl + '_recency' ] = min( shopper_data.get(lvl + '_recency', float('Inf')), recency.days)

                        # Frequency
                        shopper_data[ lvl + '_frequency' ] = shopper_data.get(lvl + '_frequency', 0) + 1

                        # Monetary
                        shopper_data[ lvl + '_monetary' ] = shopper_data.get(lvl + '_monetary', 0) + float(row['purchaseamount'])




            try:
                row = transactions.next()
                i += 1
                new_id = row['id']
            except StopIteration:
                complete = True
                break

header = list(set(shopper_dict.values()[0].keys()
                  + [lvl + metric
                     for lvl in levels
                     for metric in metrics]))

dw = csv.DictWriter(outfile, fieldnames = header)
dw.writeheader()
dw.writerows([y for (x,y) in shopper_dict.items()])

    
        
        

         

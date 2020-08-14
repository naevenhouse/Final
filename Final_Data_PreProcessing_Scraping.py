# -*- coding: utf-8 -*-
"""
ECE 5831
Final
Nathaniel Evenhouse
"""
import time
import pandas as pd
from goodreads import client

restart = False
write = True
classify_count = 50000
backup_cycle = 1000
start_index = 49555

#current time, used to track run time.
t0 = time.time()

#initialize client for goodreads
gc = client.GoodreadsClient('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')
gc.authenticate('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')

#load in datafiles
df = pd.read_csv('Compiled_Data.csv', low_memory = False)
settings  = pd.read_csv('Settings.csv',error_bad_lines = False, low_memory = False)

if restart:
    for genre in settings['Genres']:
        df[genre]=False
    df['Classified'] = False
    
#pulls data from goodreads website
i=start_index
currently_classified = 0
newly_classified = 0
t_start = time.time()
for ID in df['Id']:
    try:
        if df.get_value(i,'Classified')==False:
            book = gc.book(ID)
            genres_of_book = book.popular_shelves
            print("Read time for book " + str(i) + " : " + str(time.time()-t_start) + " seconds")
            read_book_time = time.time()
            
            if genres_of_book:
                for genre in settings['Genres']:
                    is_target_in_list = False
                    for item in genres_of_book:
                        is_target_in_list = is_target_in_list or (genre.lower() == str(item).lower())
                        df.at[i, genre] = is_target_in_list
                df.at[i, 'Classified'] = True
                print("Classification time of book " + str(i) + " : " + str(time.time()-read_book_time) + " seconds")
                
            if newly_classified%backup_cycle == 0 and newly_classified!=0:
                if write:
                    print('Backing up progress...')
                    t_back_0 = time.time()
                    df.to_csv('Compiled_Data.csv', index=False)
                    print('Backup Complete, time: ' + str(time.time() - t_back_0))
            if newly_classified>classify_count:
                break
            newly_classified+=1
            if (time.time()-t_start)<1:
                time.sleep(1-(time.time()-t_start))
        else:
            currently_classified+=1
    except:
        print("error in ID: " + str(ID))
    i+=1
    if newly_classified>0:
        print("Looptime: " + str(time.time() - t_start) + "seconds")
    t_start = time.time()

time.sleep(30)
if write:
    print('Saving File...')
    df.to_csv('Compiled_Data.csv', index=False)
    print('Data saved')

#processing time overall
print("Classified books: " + str(i))
print("total runtime: " + str(time.time()-t0) + " seconds")


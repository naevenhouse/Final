# -*- coding: utf-8 -*-
"""
ECE 5831
Final
Nathaniel Evenhouse
"""
import time
import pandas as pd
from goodreads import client

#Settings for data scrapping
restart = False
write = True
classify_count = 25
backup_cycle = 1000
start_index = 250000

#current time, used to track run time.
t0 = time.time()

#initialize client for goodreads
gc = client.GoodreadsClient('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')
gc.authenticate('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')

#load in datafiles
df = pd.read_csv('Compiled_Data.csv', low_memory = False)
settings  = pd.read_csv('Settings.csv',error_bad_lines = False, low_memory = False)

#restart classification data if desired
if restart:
    for genre in settings['Genres']:
        df[genre]=False
    df['Classified'] = False
    
#pulls data from goodreads website
#starting settings
i=start_index
currently_classified = 0
newly_classified = 0
t_start = time.time()

#classification loop
for ID in df['Id']:
    #reports errors, but continues even if an error occured
    try:
        #stops program from re-classifying data
        if df.get_value(i,'Classified')==False:
            #gets "shelf" data from goodreads, this is the only place that the book genre shows up from their API
            book = gc.book(i)
            genres_of_book = book.popular_shelves
            
            #time reporting
            print("Read time for book " + str(i) + " : " + str(time.time()-t_start) + " seconds")
            read_book_time = time.time()
            
            #only completes classification if there was successful shelf data for the book
            if genres_of_book:
                #iterates through all of the genres from the settings and marks them in the dataframe
                for genre in settings['Genres']:
                    is_target_in_list = False
                    for item in genres_of_book:
                        is_target_in_list = is_target_in_list or (genre.lower() == str(item).lower())
                        df.at[i, genre] = is_target_in_list
                #marks the row as classified
                df.at[i, 'Classified'] = True
                #reports classification time
                print("Classification time of book " + str(i) + " : " + str(time.time()-read_book_time) + " seconds")
            
            #periodically backs up the data
            if newly_classified%backup_cycle == 0 and newly_classified!=0:
                if write:
                    print('Backing up progress...')
                    t_back_0 = time.time()
                    df.to_csv('Compiled_Data.csv', index=False)
                    print('Backup Complete, time: ' + str(time.time() - t_back_0))
            
            #counts the number of newly classified books
            if newly_classified>classify_count:
                break
            newly_classified+=1
            
            #Limits function calls to 1 second due to good reads terms of service
            if (time.time()-t_start)<1:
                time.sleep(1-(time.time()-t_start))
        else:
            currently_classified+=1
    except:
        #informs the user where errors occured
        print("error in ID: " + str(i))
    
    #reports the final loop parameters
    i+=1
    if newly_classified>0:
        print("Looptime: " + str(time.time() - t_start) + "seconds")
    t_start = time.time()

#writes the data to the csv file once completed
if write:
    print('Saving File...')
    df.to_csv('Compiled_Data.csv', index=False)
    print('Data saved')

#processing time overall
print("Classified books: " + str(i))
print("total runtime: " + str(time.time()-t0) + " seconds")


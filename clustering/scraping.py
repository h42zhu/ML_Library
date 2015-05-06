from bs4 import BeautifulSoup
import urllib2
import re
import csv

# Global Var
chare = re.compile(r'[!-\.&]')

drop_words = ['a', 'new', 'some', 'more', 'the', 'my', 'own', 'many', 'other',
              'another', 'while', 'once']

            
# url = ["https://www.google.ca/finance?hl=en&gl=ca"]
# print scraping_url_table(url, ('quote',), ('symbol',))

def scraping_url_table_csv(url, table_attr, cell_attr, csv_file):
    with open(csv_file, 'wb') as csvfile:
        # datasets = []
        c = urllib2.urlopen(url)
        soup = BeautifulSoup(c.read())    
        tables = soup.find_all("table", attrs={"class":table_attr})
        
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter= ',')
       
        for table in tables:
            # print table.find('tr')
            # headings = [td.get_text().strip() for td in table.find_all("td")]
            # print headings
            

            for a, span in zip(table.find_all("a"), table.find_all("span", attrs={"class":None})):
                
                line = [a.get_text().strip(), span.get_text().strip()]
                # print line
                spamwriter.writerow(line)
                # print td.get_text()
            break
            



url = "https://www.google.ca/finance?hl=en&gl=ca"
scraping_url_table_csv(url, 'quotes', 'symbol', 'finance_data.csv')
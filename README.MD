The program was created in order to simplify the search for the geographical coordinates of factories at their address.

The program receives an Excel file with the names and addresses of factories as input. The program takes out the address values from there and, opening Google Chrome, searches for this address. The program finds the coordinates from the html markup of the open tab by tags and writes them to the excel file. Closes google chrome.

From the features of the work:
- The program can report how much time is spent searching for all coordinates.
- The program loads a page without images and css files to speed up loading.
- An attempt was made to make the work of the program multi-threaded. The program works, but is slower than the original version, due to python limitations.

The program is designed to help the daily work of the sales department of the company.

Developed by Igor Drogaitsev.
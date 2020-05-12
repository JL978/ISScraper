# ISScraper

A practice project that utilizes selenium and beautiful soup to scrape data from a website and store them in csv format

The main function of the project is to log into the website, navigate the mouse to the right links to click on and use the mouse to scroll in a scroll area with the wanted data. While scrolling, the javascript on the page updates the table and so beautifulsoup was used to read changing html element to figure out when to scrape new data displayed on the table. 

The final script only work partially since the web page does not seem to allow for mouse click right after login - therefore the script was modified to promt the human user of which element to click. Another issue arise when scrolling the scroll area, the scroll area seem to scroll backwards every so often and make the scrolling stuck in a loop - the issue was overcomed with the help of a human user to pull the scroll bar down past the point where the scroll back happen. 

![demo](demo.gif)


># **Witcher_Project**

The purpose of this project is to extract relationship among characters in the Witcher book series, perform network analysis and evaluate character importance. To achieve this:

* The first notebook, `Character_Web_Scraping.ipynb`, scraps the characters name from all the Witcher books and saves them in relation to which book they are present in as a `.csv` file.

* `Relationship_Extraction_and_Newtwork_Analysis.ipynb` creates relationships among characters based on the proximity of their presence in sentence within a given window size. This relationship is then weighted and graphically visualized for analysis. Degree, Betweenness and Closeness Centralities are perfomed and plotted to analyze the importance level of charactes. A Community Detection along with its PyVis visualization is later perfomed which gives a critical insight to catagorize characters' importance within their respective communities.

* `Character_Importance_Evolution.ipynb` makes further analysis on characters' importance, and includes a breakdown of the observation made on the time-series plot depicting the evolution of characters' importance throughout the eight books.

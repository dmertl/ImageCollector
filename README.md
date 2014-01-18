ImageCollector
==============

Scrape website to collect images. Display and filter images using metadata.

- Create classes which can be used to easily target source data.
- Include reporting for detailed information on what parsing engine is doing.
- Log any instances of expected data not found, could indicate a change in page structure that would require new scraping.
- Have the page-level collector classes include a URL regex for what pages they apply to. They you can re-use the collectors dynamically.
- Create a front-end web page for viewing collected images. Ability to filter, search, flag as viewed.
- Script to automate scraping on timed intervals.
- Smart caching system to eliminate duplicate requests. Each resource should have it's own retrieve method, but utilize some kind of global registry class for caching.
 - Index pages will need fast caching timeout vs. image pages.
- Class separation for index pages vs. image pages. Index pages are lists of links to image pages. Image pages represent one image, but may have links to varying qualities.

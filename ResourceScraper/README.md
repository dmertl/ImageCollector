Concepts
========

- Accept a filename or URL of page to scrape
- Retrieve contents (string) of page
- Convert contents to appropriate handler (beautiful soup)
- Search handler for resources
- Search handler for links to additional pages to scrape

For each resource found
- Massage resource into usable format
- Determine if resource should be downloaded
- If so, download resource
- Store resource

For each additional page found
- Determine if page should be scraped
- If so, call scrape again with page URI

Definitions
===========

- Page: A file that contains links to resources and/or other pages. Examples: web page HTML.
- Resource: A file that we wish to download a store a copy of. Examples: image, mp3.
- Resource Link: Some information parsed by scraper that identifies a resource.
- Resource Data: The raw resource data.

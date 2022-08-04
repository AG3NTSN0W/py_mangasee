# py_mangasee
Download all chapter from mangasee.

## Requirements
- docker
- RSS url or chapter url

Files will be saved to /tmp/downloads

## How to use 

Arguments | Function | default | notes
------------ | ------------ | ------------ | ------------
`-u --url` | Rss url or chapter url | | 
`-f --format` | Save as pdf or png | png | PDF Maximum supported image dimension is 65500 pixels
`-p --pool` |  Multi-processing Pool size  | 2 | 
`-s --splite` | Save chapter image in separate file | False | By default a chapter will be save in on file

- Download all chapter
    ```
    bash run.sh -u https://mangasee123.com/rss/<manga_name>.xml
    ```   

- Download one chapter
    ```
    bash run.sh -u https://mangasee123.com/read-online/<manga_name>-chapter-85.html
    ```





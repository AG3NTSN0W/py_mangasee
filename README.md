# py_mangasee
Download all chapter from mangasee.

## Requirements
- docker
- RSS url

Files will be saved to /tmp/downloads

## How to use 

Arguments | Function | default | notes
------------ | ------------ | ------------ | ------------
`-u --url` | Rss url or chapter url | | 
`-f --format` | Save as pdf or png | pdf | 
`-c --chapter` | Download one chapter |  | 
`-p --pool` |  Multi-processing Pool size  | 2 | 
`-s --splite` | Save chapter image in separate file | False | By default a chapter will be save in one file <br> Pdf format will save manga over mutiple pages


- Download all chapter
    ```
    bash run.sh -u https://mangasee123.com/rss/<manga_name>.xml
    ```   

- Download one chapter
    ```
    bash run.sh -u https://mangasee123.com/rss/<manga_name>.xml -c 5
    ```





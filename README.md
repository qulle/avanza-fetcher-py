# Avanza Fetcher
### A small script that fetches the current stock values from the specified endpoints in the json-file

## Screenshot
![Screenshot of the program](images/result.png?raw=true "Screenshot of the program")

The script was run after hours, that's why 'buy' and 'sell' columns are empty.

## Runtime
```
$ python avanza-fetcher.py urls.json
```

You can change the default output and pipe the result to a file
```
$ python avanza-fetcher.py urls.json > output.txt
```

## External dependencies
Using package requests, install using PIP
```
$ pip install requests
```

## Tested
The code have been tested on:
- Windows 10 machine running Python 3.9.0

## Note
If the code gives unexpected or no result, it's probably because the website has altered their HTML. \
Rewriting the regex expressions should fix that.

## Author
[Qulle](https://github.com/qulle/)
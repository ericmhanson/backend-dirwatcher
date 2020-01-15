# Dirwatcher!

This is a program intended to run continuously and to pull information at timed intervals. It will watch a directory of files. When the text string that is given in the arguments is found, the program will log what line the string was found on and at what time it was found. It can also handle files being added or deleted from the directory. Make sure to add a directory with files to watch.


How to run:
```$ python3 dirwatcher.py [optional: file extension(e.g. '.txt')] [optional: integer interval] [path] [magic text]```

Example: ```$ python3 dirwatcher.py watchdir eric```

Example 2: ```$ python3 dirwatcher.py .txt 1.0 watchdir eric```
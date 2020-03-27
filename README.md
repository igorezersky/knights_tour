Knights tour
============

This simple project can be used to simulate knights tour on chess board

Usage
-----

```text
python knights_tour.py [-h] [--color {white,black}] [--position {right,left}]

optional arguments:
  -h, --help            show this help message and exit   
  --color {white,black}
                        Knight color
  --position {right,left}
                        Knight position (relative to king)
```

Quickstart
----------

Open terminal and execute following:

```shell script
python knights_tour.py
```

Script will simulate knights tour and display something like this:

```text
Knight start position is G6. Knights tour:

         A  B  C  D  E  F  G  H

8       33 30 19  4 23 28 17  2         8
7       20  5 32 29 18  3 24 27         7
6       31 34 39 22 45 26  1 16         6
5        6 21 44 53 38 47 58 25         5
4       35 40 37 46 59 54 15 48         4
3       10  7 60 43 52 49 64 57         3
2       41 36  9 12 55 62 51 14         2
1        8 11 42 61 50 13 56 63         1

         A  B  C  D  E  F  G  H
```
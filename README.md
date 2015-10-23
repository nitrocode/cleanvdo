# cleanvdo
Consolidates the output of vncdotool's [vnclog](https://help.github.com/articles/markdown-basics/)

1. First record a vdo file using the vncdotool

```bash
$ vnclog -s 1.1.1.1::5997 --viewer vncviewer > wireless.vdo
```

2. Run the consolidate vdo script

```bash
$ ./convdo.py -h
usage: convdo.py [-h] [--typekeys] [--insertcap INSERTCAP]
                 [--roundpause ROUNDPAUSE] [--remove REMOVE] [--backspace]
                 [--debug] [--version]
                 [input]

Consolidate vdo files for readability

positional arguments:
  input                 File to convert

optional arguments:
  -h, --help            show this help message and exit
  --typekeys, -t        consolidates keyup / keydowns for sequential ascii
                        chars to one type statement
  --insertcap INSERTCAP, -c INSERTCAP
                        inserts a capture after each line and saves to dir
  --roundpause ROUNDPAUSE, -R ROUNDPAUSE
                        roundsup the pause to the nearest hundredths
  --remove REMOVE, -r REMOVE
                        removes as many commands as you like
  --backspace, -b       removes the backspace commands and the previously
                        typed character
  --debug, -d           shows debug messages
  --version, -v         show program's version number and exit
```

Example

```bash
$ ./convdo.py examples/wireless.vdo
```

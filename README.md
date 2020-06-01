# entropy-calculator

Small command line utility to calculate entropy of discrete distributions.
Works for normalised or unnormalised distributions, and accepts input from files or standard input (`stdin`).
Remember you can send indicate the end of `stdin` by pressing `<C-d>` on a new line!

```
usage: entropy.py [-h] [--no-filenames] [-c] [--precision PREC] [--base BASE]
                  [FILES [FILES ...]]

Utility for calculating entropy of (un)normalised probability distributions.

positional arguments:
  FILES                 Files to read. One value per line. Blank lines
                        ignored. - is stdin. If no files given read from
                        stdin. (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --no-filenames        Don't print filenames. (default: False)
  -c, --check-normalised
                        Don't print filenames. (default: False)
  --precision PREC      Precision for printing. (default: 3)
  --base BASE           Base for logarithm. (default: 2.718281828459045)
```

nc2mp4
======

```
usage: nc2mp4.py [-h] [--out OUT] [--fps FPS] [--dpi DPI] [--ppdp PPDP]
                 [--k K] [--jrange JRANGE JRANGE] [--irange IRANGE IRANGE]
                 [--vlim VLIM] [--colormap COLORMAP] [--begin BEGIN]
                 [--end END] [--stride STRIDE] [--progress] [--fpf FPF]
                 [--testview] [--keep] [--label LABEL LABEL]
                 [--multiply MULTIPLY] [--quiet] [--debug]
                 variable [files [files ...]]

positional arguments:
  variable              Name of variable in netCDF files
  files                 netCDF files to be read

optional arguments:
  -h, --help            show this help message and exit
  --out OUT, -o OUT     Name of mpeg file
  --fps FPS, -f FPS     Frames per second
  --dpi DPI, -d DPI     Dots per inch (sets font size wrt image)
  --ppdp PPDP, -P PPDP  Pixels per data point (sets frame size)
  --k K, -k K           Second dimension, if any
  --jrange JRANGE JRANGE, -j JRANGE JRANGE
                        j-range
  --irange IRANGE IRANGE, -i IRANGE IRANGE
                        i-range
  --vlim VLIM, -v VLIM  vmin vmax
  --colormap COLORMAP, -c COLORMAP
                        Colormap
  --begin BEGIN, -b BEGIN
                        Beginning record
  --end END, -e END     Ending record
  --stride STRIDE, -s STRIDE
                        Record stride
  --progress, -p        Display progress stats
  --fpf FPF             Frames per file
  --testview, -t        Test view by showing the last frame
  --keep                Keep intermediate files
  --label LABEL LABEL   Position of text
  --multiply MULTIPLY, -x MULTIPLY
                        Multiplier
  --quiet, -q           Less output
  --debug, -D           Debugging info
```

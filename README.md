nc2mp4
======

```
usage: nc2mp4.py [-h] [--out OUT] [--fps FPS] [--k K] [--vlim VLIM]
                 [--colormap COLORMAP] [--begin BEGIN] [--end END]
                 [--stride STRIDE] [--progress] [--fpf FPF] [--visualize]
                 [--keep]
                 variable [files [files ...]]

positional arguments:
  variable              Name of variable in netCDF files
  files                 netCDF files to be read

optional arguments:
  -h, --help            show this help message and exit
  --out OUT, -o OUT     Name of mpeg file
  --fps FPS, -f FPS     Frames per second
  --k K, -k K           Second dimension, if any
  --vlim VLIM, -l VLIM  vmin vmax
  --colormap COLORMAP, -c COLORMAP
                        Colormap
  --begin BEGIN, -b BEGIN
                        Beginning record
  --end END, -e END     Ending record
  --stride STRIDE, -s STRIDE
                        Record stride
  --progress, -p        Display progress stats
  --fpf FPF             Frames per file
  --visualize, -v       Show the sample frame
  --keep                Keep intermediate files
```

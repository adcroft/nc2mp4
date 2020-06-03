#!/usr/bin/env python3

import argparse
import netCDF4
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy
import os
import subprocess
import time

def two_floats(value):
    values = value.split()
    if len(values) != 2:
        raise argparse.ArgumentError
    return float(values[0]), float(values[1])

parser = argparse.ArgumentParser()
parser.add_argument("variable", help="Name of variable in netCDF files")
parser.add_argument("files", nargs="*", help="netCDF files to be read")
parser.add_argument("--out", "-o", default='anim', help="Name of mpeg file")
parser.add_argument("--fps", "-f", default=15, help="Frames per second")
parser.add_argument("--dpi", "-d", default=100, type=int, help="Dots per inch")
parser.add_argument("--k", "-k", default=None, type=int, help="Second dimension, if any")
parser.add_argument("--jrange", "-j", nargs=2, default=None, type=int, help="j-range")
parser.add_argument("--irange", "-i", nargs=2, default=None, type=int, help="i-range")
parser.add_argument("--vlim", "-l",  action='store', type=two_floats, default="0 0", help="vmin vmax")
parser.add_argument("--colormap", "-c",  default='wbgr', help="Colormap")
parser.add_argument("--begin", "-b", default=0, type=int, help="Beginning record")
parser.add_argument("--end", "-e", default=0, type=int, help="Ending record")
parser.add_argument("--stride", "-s", default=1, type=int, help="Record stride")
parser.add_argument("--progress", "-p", action='store_true', help="Display progress stats")
parser.add_argument("--fpf", default=60, type=int, help="Frames per file")
parser.add_argument("--visualize","-v", action='store_true', help="Show the sample frame")
parser.add_argument("--keep", action='store_true', help="Keep intermediate files")
parser.add_argument("--label", nargs=2, type=float, default=None, help="Position of text")

args = parser.parse_args()
print('Arguments:', args)

timer_init = time.perf_counter()
nc = netCDF4.MFDataset(args.files)
var = nc.variables[args.variable]
if args.k is None:
    k = ...
else:
    k = args.k
if args.jrange is None:
    jslice = ...
else:
    jslice = slice(args.jrange[0], args.jrange[1])
if args.irange is None:
    islice = ...
else:
    islice = slice(args.irange[0], args.irange[1])

if args.begin<0: # 0 means the beginning
    nbegin = var.shape[0]+args.begin
else:
    nbegin = args.begin
if args.end<=0: # 0 means the end
    nend = var.shape[0]+args.end
else:
    nend = args.end
nrange_full = list( range(nbegin, nend, args.stride) )

data = var[nend-args.stride,k][jslice][:,islice]
nj,ni = data.shape

vmin, vmax = args.vlim[0], args.vlim[1]
if vmax==vmin:
    vmin, vmax = data.min(), data.max()
    print("Plotting data range %g .. %g"%(vmin,vmax))

metadata = dict(title=args.variable)
writer = FFMpegWriter(fps=args.fps, metadata=metadata,
    codec='libx264', extra_args=['-s', '%ix%i'%(ni,nj),
                        '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-tune', 'animation', '-crf', '4',
                        '-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2'])
   # -vf option added because the frame sometimes changes size !?

if args.colormap=='wbgr':
    cdict = {'red':   [[0.0,  0.5, 0.5], [0.2,  1.0, 1.0], [0.4,  0.1, 0.1], [0.6,  0.9, 0.9], [0.8,  0.0, 0.1], [1.0,  0.8, 0.8]],
             'green': [[0.0,  0.2, 0.2], [0.2,  1.0, 1.0], [0.4,  0.3, 0.3], [0.6,  1.0, 1.0], [0.8,  0.2, 0.2], [1.0,  0.9, 0.9]],
             'blue':  [[0.0,  0.2, 0.2], [0.2,  0.8, 0.8], [0.4,  0.0, 0.0], [0.6,  0.9, 0.9], [0.8,  0.3, 0.3], [1.0,  0.9, 0.9]]}
    args.colormap = matplotlib.colors.LinearSegmentedColormap('test', segmentdata=cdict, N=256)

if args.visualize:
    matplotlib.use('TKAgg')

fig = plt.figure( figsize=(2*ni/args.dpi,2*nj/args.dpi), dpi=args.dpi )
ax = fig.add_axes([0,0,1,1])
im = ax.imshow(data, interpolation='none', cmap=args.colormap, vmin=vmin, vmax=vmax)

if args.label is not None:
    label = ax.text(args.label[0]*ni, args.label[1]*nj, '')

if args.visualize:
    plt.show()
    exit()

if args.progress:
    print('Opening files took %.3f secs'%(time.perf_counter()-timer_init))

tmpfiles = ['animlist.txt']
with open("animlist.txt", "w") as listfile:
    nframes, stage, frame = len(nrange_full), -1, 0
    nstages = (len(nrange_full)+args.fpf-1)//args.fpf
    timer_write = time.perf_counter()
    while len(nrange_full)>0:
        stage += 1
        filename = '%s.%3.3i.mp4'%(args.out,stage)
        tmpfiles.append(filename)
        listfile.write("file '%s'\n"%(filename))
        j = len(nrange_full)
        if len(nrange_full)>1.5*args.fpf:
            j = min(args.fpf, j)
        nrange = nrange_full[:j]
        nrange_full = nrange_full[j:]
        these_frames = len(nrange)
        with writer.saving(fig, filename, these_frames):
            for n in nrange:
                frame += 1
                print('\r%s %i/%i (%.1f%%) '%(filename,frame,nframes,100.*frame/nframes), end='')
                data = var[n,k][jslice][:,islice]
                im.set_data(data[-1::-1,:])
                if args.label is not None:
                    label.set_text('%s r:%i f:%i/%i clim:%g,%g'%(
                                   args.variable, n, frame, nframes, vmin, vmax))
                writer.grab_frame()
                if args.progress:
                    t = time.perf_counter() - timer_write
                    dt = t/frame
                    ttot, trem = nframes*dt, (nframes-frame)*dt
                    print('%.3fs elapsed, %.3fs/frame, %.1fs total, %.1fs remaining'%(t,dt,ttot,trem),
                          end='')
        if args.progress:
            t = time.perf_counter() - timer_write
            dt = t/frame
            ttot, trem = nframes*dt, len(nrange_full)*dt
            print('\r%s created, %i/%i (%.1f%%) %.1fs elapsed, %.3fs/frame, %.1fs total, %.1fs remaining'%(
                  filename,frame,nframes,100.*frame/nframes,t,dt,ttot,trem))

print(['ffmpeg','-f','concat','-safe','0','-i','animlist.txt','-y','-c','copy','%s.mp4'%(args.out)])
subprocess.run(['ffmpeg','-f','concat','-safe','0','-i','animlist.txt','-y','-c','copy','%s.mp4'%(args.out)])
if not args.keep:
    for f in tmpfiles:
        os.remove(f)

# A simple python script to test a disk

## Notes
- As the licence states, I have no reposibility of what you do with this script.
  If you end up with a failing disk after using it, lose data or anything like
  that, sorry but that's your problem. You have accepted the license when you
  decided to use it it states the no warranty is provided.
- It has been tested in Linux with EXT4. I don't know about Mac or Windows.
- You can use this in a disk you have files in it, but I do not adivse to do it.
- If you believe your disk is about to die, make a backup and run SMART tests.
  DO NOT USE THIS TOOL as it can finish killing your disk, Unless you want to
  end with it.
- Regardless of the result, do an online backup of the important stuff and use
  an automatic synchronization service (I use OneDrive, it works well).
- This is a simple and dirty script made to address a personal need, has been
  written in two hours and that process has been documented here:
  https://www.youtube.com/watch?v=VPRPirtmWdI (audio in brazilian portuguese
  HUEHUEHUE BR É NOIS)

## Description
This python script will fill a disk with a given file and do the following for
each file it writes:
- Calculates the sha256 hash of the file that has been written;
- Check if the file that has been written has the same hash as the original
  file;
- In case the script fails 5 times to write a given file, it will fail and abort
  the execution.
- If the script is able to fill up the disk, it will generate a report like the
  one below:

```
THE AWESOME HD TESTER OUTPUT REPORT
Did it finish? No, it has aborted.Amount of file created: 1000
Amount of hashes failed: 10 / 0.01
IO/Disk Errors: 0 / 0.0
Other errors: 0 / 0.0
Breakdown of IO/Disk Errors:
...
Detailed log:
Tue Sep 15 12:30:54 2020-HASH ERROR-Hash check for file dummy_file_1.tst has failed. Will (probably) delete the file and try again.
...
```

## Usage
Make sure you have python 3  and pipenv installed.

```
$ pipenv install
$ pipenv shell
(hd-tester) $ python3 hdtester.py 
usage: hdtester.py [-h]
                   <file path> <output file> <path to folder inside block
                   device>
hdtester.py: error: the following arguments are required: <file path>, <output file>, <path to folder inside block device>
```

Download a file you want to use to fill the disk. I have used a xubuntu iso that
has around 1,5gb to fill up a 2tb disk. You can use anything you prefer, but I
suggest files of around 1gb. The script will load this file in memory, so make
sure you have enough free ram memory in your system to have two copies of this
file in memory (if you use a 1,5gb iso, make sure you have 3gb of free memory).

Example command line:
```
(hd-tester) $ python3 ./hdtester.py xubuntu-20.04-desktop-amd64.iso ./the_report.txt /media/danodic/bla.../
```

It takes time, so please be patient. In my case I have left it overnight.

## Why
I bought a hard disk that was passing the SMART tests but it was not working
well. When idle, it would often start making noises and hiting the read heads
into the limiter. Still, that was ocasional and the SMART tests were passing
even though I could see a lot of garbage showing up in the `dmesg` output.

I decided to create this script to make sure I was able to fill the disk and
read the data that has been written. While doing that, I wanted to know what
was the failure rate and which errors I was getting.

I did not had the intention to benchmark it and to measure read/read speeds, I
just wanted to make sure I was not running the imminent risk of losing important
data when reaching the depths of the disk when I was out of warranty. This is
the reason there is no multi-threading or any other features to saturate the
SATA bus. This is a test any disk in good state should be able to pass. I have
tested in my 1tb disk (same brand and model) and it has passed without any
error.

It is common in bad disks that you are able to write the file but the copy
is messed up. This is the reason I decided to include the hash check, because
that assures the bytes written are (very likely) the expected ones.

It ends up the disk had a high failure rate but SMART would say the disk was
healthy, even because it was new. Anyway, seeing is believing and this has
helped me assuring the disk was bad and a had to RMA it.

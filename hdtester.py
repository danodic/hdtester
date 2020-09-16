#!/usr/bin/env python
"""
MIT License

Copyright (c) 2020 danodic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import hashlib
import os
import pdb

from datetime import datetime

# Command line arguments
parser = argparse.ArgumentParser(description='Will test an HD or any other'
                                             'block device by filling it up'
                                             'with files.')

parser.add_argument('input_file', metavar='<file path>',
                    help='File that will be used to fill up the disk.')

parser.add_argument('output', metavar='<output file>',
                    help='Place where the output report will be placed.')

parser.add_argument('folder', metavar='<path to folder inside block device>',
                    type=str, help='Path to a folder inside the block device'
                    'that has to be tested.')

args = parser.parse_args()

# A list of error codes that can be returned when trying to write to the disk.
# Extracted from `errno -l` output.
errnos = {
    1: 'EPERM: Operation not permitted',
    2: 'ENOENT: No such file or directory',
    3: 'ESRCH: No such process',
    4: 'EINTR: Interrupted system call',
    5: 'EIO: Input/output error',
    6: 'ENXIO: No such device or address',
    7: 'E2BIG: Argument list too long',
    8: 'ENOEXEC: Exec format error',
    9: 'EBADF: Bad file descriptor',
    10: 'ECHILD: No child processes',
    11: 'EAGAIN: Resource temporarily unavailable',
    12: 'ENOMEM: Cannot allocate memory',
    13: 'EACCES: Permission denied',
    14: 'EFAULT: Bad address',
    15: 'ENOTBLK: Block device required',
    16: 'EBUSY: Device or resource busy',
    17: 'EEXIST: File exists',
    18: 'EXDEV: Invalid cross-device link',
    19: 'ENODEV: No such device',
    20: 'ENOTDIR: Not a directory',
    21: 'EISDIR: Is a directory',
    22: 'EINVAL: Invalid argument',
    23: 'ENFILE: Too many open files in system',
    24: 'EMFILE: Too many open files',
    25: 'ENOTTY: Inappropriate ioctl for device',
    26: 'ETXTBSY: Text file busy',
    27: 'EFBIG: File too large',
    28: 'ENOSPC: No space left on device',
    29: 'ESPIPE: Illegal seek',
    30: 'EROFS: Read-only file system',
    31: 'EMLINK: Too many links',
    32: 'EPIPE: Broken pipe',
    33: 'EDOM: Numerical argument out of domain',
    34: 'ERANGE: Numerical result out of range',
    35: 'EDEADLK: Resource deadlock avoided',
    36: 'ENAMETOOLONG: File name too long',
    37: 'ENOLCK: No locks available',
    38: 'ENOSYS: Function not implemented',
    39: 'ENOTEMPTY: Directory not empty',
    40: 'ELOOP: Too many levels of symbolic links',
    42: 'ENOMSG: No message of desired type',
    43: 'EIDRM: Identifier removed',
    44: 'ECHRNG: Channel number out of range',
    45: 'EL2NSYNC: Level 2 not synchronized',
    46: 'EL3HLT: Level 3 halted',
    47: 'EL3RST: Level 3 reset',
    48: 'ELNRNG: Link number out of range',
    49: 'EUNATCH: Protocol driver not attached',
    50: 'ENOCSI: No CSI structure available',
    51: 'EL2HLT: Level 2 halted',
    52: 'EBADE: Invalid exchange',
    53: 'EBADR: Invalid request descriptor',
    54: 'EXFULL: Exchange full',
    55: 'ENOANO: No anode',
    56: 'EBADRQC: Invalid request code',
    57: 'EBADSLT: Invalid slot',
    59: 'EBFONT: Bad font file format',
    60: 'ENOSTR: Device not a stream',
    61: 'ENODATA: No data available',
    62: 'ETIME: Timer expired',
    63: 'ENOSR: Out of streams resources',
    64: 'ENONET: Machine is not on the network',
    65: 'ENOPKG: Package not installed',
    66: 'EREMOTE: Object is remote',
    67: 'ENOLINK: Link has been severed',
    68: 'EADV: Advertise error',
    69: 'ESRMNT: Srmount error',
    70: 'ECOMM: Communication error on send',
    71: 'EPROTO: Protocol error',
    72: 'EMULTIHOP: Multihop attempted',
    73: 'EDOTDOT: RFS specific error',
    74: 'EBADMSG: Bad message',
    75: 'EOVERFLOW: Value too large for defined data type',
    76: 'ENOTUNIQ: Name not unique on network',
    77: 'EBADFD: File descriptor in bad state',
    78: 'EREMCHG: Remote address changed',
    79: 'ELIBACC: Can not access a needed shared library',
    80: 'ELIBBAD: Accessing a corrupted shared library',
    81: 'ELIBSCN: .lib section in a.out corrupted',
    82: 'ELIBMAX: Attempting to link in too many shared libraries',
    83: 'ELIBEXEC: Cannot exec a shared library directly',
    84: 'EILSEQ: Invalid or incomplete multibyte or wide character',
    85: 'ERESTART: Interrupted system call should be restarted',
    86: 'ESTRPIPE: Streams pipe error',
    87: 'EUSERS: Too many users',
    88: 'ENOTSOCK: Socket operation on non-socket',
    89: 'EDESTADDRREQ: Destination address required',
    90: 'EMSGSIZE: Message too long',
    91: 'EPROTOTYPE: Protocol wrong type for socket',
    92: 'ENOPROTOOPT: Protocol not available',
    93: 'EPROTONOSUPPORT: Protocol not supported',
    94: 'ESOCKTNOSUPPORT: Socket type not supported',
    95: 'EOPNOTSUPP: Operation not supported',
    96: 'EPFNOSUPPORT: Protocol family not supported',
    97: 'EAFNOSUPPORT: Address family not supported by protocol',
    98: 'EADDRINUSE: Address already in use',
    99: 'EADDRNOTAVAIL: Cannot assign requested address',
    100: 'ENETDOWN: Network is down',
    101: 'ENETUNREACH: Network is unreachable',
    102: 'ENETRESET: Network dropped connection on reset',
    103: 'ECONNABORTED: Software caused connection abort',
    104: 'ECONNRESET: Connection reset by peer',
    105: 'ENOBUFS: No buffer space available',
    106: 'EISCONN: Transport endpoint is already connected',
    107: 'ENOTCONN: Transport endpoint is not connected',
    108: 'ESHUTDOWN: Cannot send after transport endpoint shutdown',
    109: 'ETOOMANYREFS: Too many references: cannot splice',
    110: 'ETIMEDOUT: Connection timed out',
    111: 'ECONNREFUSED: Connection refused',
    112: 'EHOSTDOWN: Host is down',
    113: 'EHOSTUNREACH: No route to host',
    114: 'EALREADY: Operation already in progress',
    115: 'EINPROGRESS: Operation now in progress',
    116: 'ESTALE: Stale file handle',
    117: 'EUCLEAN: Structure needs cleaning',
    118: 'ENOTNAM: Not a XENIX named type file',
    119: 'ENAVAIL: No XENIX semaphores available',
    120: 'EISNAM: Is a named type file',
    121: 'EREMOTEIO: Remote I/O error',
    122: 'EDQUOT: Disk quota exceeded',
    123: 'ENOMEDIUM: No medium found',
    124: 'EMEDIUMTYPE: Wrong medium type',
    125: 'ECANCELED: Operation canceled',
    126: 'ENOKEY: Required key not available',
    127: 'EKEYEXPIRED: Key has expired',
    128: 'EKEYREVOKED: Key has been revoked',
    129: 'EKEYREJECTED: Key was rejected by service',
    130: 'EOWNERDEAD: Owner died',
    131: 'ENOTRECOVERABLE: State not recoverable',
    132: 'ERFKILL: Operation not possible due to RF-kill',
    133: 'EHWPOISON: Memory page has hardware error',
}

# Some control variables, used to measure error statistics
file_counter = 0
hash_count = 0
failed_hashes = 0
io_errors = 0
try_count = 0
other_errors = 0
io_error_list = {}

# Used later to define if the script has been aborted.
aborted = False

# The lit of log entries
log = []

def get_file_name():
    """ Return the name of the next file to be created """
    global file_counter
    file_counter += 1
    return f'dummy_file_{file_counter}.tst'

def calculate_hash(file_bytes):
    """ Will calculate the sha256 digest of the bytes provided. """
    m = hashlib.sha256()
    m.update(file_bytes)
    return m.digest()

def get_file_bytes(file_path):
    """ Will return the bytes of the file provided. """
    with open(file_path, 'rb') as f:
        return f.read()

def write_file_bytes(bytes, filename, filepath):
    """ Will write the file in the disk. """
    with open(os.path.join(filepath, filename), 'wb') as f:
        f.write(bytes)

def delete_file(filename, filepath):
    """ Delete a file from the disk. """
    os.remove(os.path.join(filepath, filename))

def get_file_hash(filename, filepath):
    """ Will return the sha256 hash of the filename provided. """
    return calculate_hash(get_file_bytes(os.path.join(filepath, filename)))

def compare_hashes(target_hash, file_hash):
    """ Will compare the hash of two files. """
    return target_hash == file_hash

def add_log(value, type):
    """ Add an entry to the log """
    global log
    log.append(f'{datetime.now().strftime("%c")}-{type}-{value}')

def create_report(filename):
    
    disk_error_breakdown = '\n'.join([f'{errnos[key]}: {value}' \
                                       for key, value in io_error_list.items()])

    detailed_log = '\n'.join(log)

    aborted_text = {True: 'No, it has aborted.', False: 'Yes.'}[aborted]

    report = \
    f"""*** THE AWESOME HD TESTER OUTPUT REPORT ***
Did it finish? {aborted_text}
Amount of files created: {file_counter}
Amount of hashes failed: {failed_hashes} / {failed_hashes / hash_count}
IO/Disk Errors: {io_errors} / {io_errors / try_count}
Other errors: {other_errors} / {other_errors / try_count}
Breakdown of IO/Disk Errors:
{disk_error_breakdown}
Detailed log:
{detailed_log}
    """

    try:
        with open(filename, 'w') as f:
            f.write(report)

        print(f'Report created at {filename}.')

    except:
        print(report)

# Initialize the script by calculating the hash of the file provided.
print(f'Calculating the hash of the file {args.input_file}.')
original_file_bytes = get_file_bytes(args.input_file)
original_hash = calculate_hash(original_file_bytes)

target_folder = args.folder
print(f'Will start filling up the disk with files at folder {target_folder}')

# Initialize the main loop
try:

    done = False
    while not done:

        # Get the new filename and update the amount of trials for this file.
        filename = get_file_name()
        trials = 3

        while trials > 0:

            try:
                try_count += 1

                print(f'Will write {filename}...')
                write_file_bytes(original_file_bytes, filename, target_folder)

                # In case no errors have happened while writing the file, count
                # as a hash write.
                hash_count += 1
                new_file_hash = get_file_hash(filename, target_folder)

                print(f'Comparing hashes...')
                if compare_hashes(original_hash, new_file_hash):
                    break

                # When a hash error happens, increase the stats count and try to
                # delete the incomplete file.
                print(f'Hash Error...')
                add_log(f'Hash check for file {filename} has failed. Will '
                         '(probably) delete the file and try again.', 'HASH '
                         'ERROR')
                delete_file(filename, target_folder)
                failed_hashes += 1
                trials -= 1

            except OSError as e:
                # OSError is the exception that happens when having trouble to
                # write to the disk (not a software issue). Those are the cases
                # we mainly want to catch.

                print(f'OS Error {e.errno}...')
                message = {
                    5: 'I/O Error.',
                    20: 'No space left in device, we are done.'
                }.get(e.errno, f'Error {e.errno} writing to disk, will '
                                '(probably) try again.')
                add_log(message, 'OS EXCEPTION')

                # 28 is disk filled, so we end when this one happens.
                if e.errno == 28:
                    print('Disk is full, finishing!')
                    done = True
                    break

                # Just add the error to a dictionary with statistics.
                else:
                    if e.errno not in io_error_list:
                        io_error_list[e.errno] = 0
                    io_error_list[e.errno] += 1
                    io_errors += 1

                trials -= 1

            except Exception as e:
                # This is to catch any other exception that may happen.
                print(f'Exception...')
                add_log(str(e), 'OTHER EXCEPTION')
                other_errors += 1
                trials -= 1

            else:
                # In case of any exception, try to delete the last file created.
                try:
                    delete_file(filename, target_folder)
                except:
                    add_log(f'Could not delete file {filename} or file does not'
                             ' exist. Moving on with life.', 'NOT AN ERROR')

        else:
            # The error we don't want to see ToT
            add_log("Have tried to write on disk 5 times with error, giving"
                    "up.", 'ERROR')
            aborted = True
            break

finally:
    # Generates the report
    create_report(args.output)

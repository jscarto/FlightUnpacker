## FlightUnpacker v1 #################################################
# Author: Joshua Stevens
# Contact: josh.stevens@psu.edu | www.joshuastevens.net
######################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
######################################################################
import zlib

# FILL IN: ZHEAD is two bytes with the actual ZLIB settings in the input
ZHEAD = '' # optional

def findstart(header, buf, source):
    """Find `header` in str `buf`, reading more from `source` if necessary"""

    while buf.find(header) == -1:
        more = source.read(2**12)
        if len(more) == 0:  # EOF without finding the header
            return ''
        buf += more

    offset = buf.find(header)
    return buf[offset:]

datafile = 'asdix-2013-04-05'

source = open(datafile, 'rb')
skip_ = source.read(32) # Skip non-zlib header

outfile = open('rawOutput.xml', 'w')

buf = ''
while True:
    decomp = zlib.decompressobj()
    # Find the start of the next stream
    buf = findstart(ZHEAD, buf, source)
    try:    
        stream = decomp.decompress(buf)
    except zlib.error:
        print "Spurious match(?) at output offset %d." % outfile.tell(),
        print "Skipping 32 bytes..."
        buf = buf[32:]
        continue

    # Read until zlib decides it's seen a complete file
    while decomp.unused_data == '':
        block = source.read(2**31-1)
        if len(block) > 0:       
            stream += decomp.decompress(block)
        else:
            break # We've reached EOF

    
    buf = decomp.unused_data # Save for the next stream
    # if len(block) == 0:
    #     break  # EOF
    outfile.write(stream)
outfile.close()
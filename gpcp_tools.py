# -*- coding: utf-8 -*-
# MIT license 2016 Ethan Nelson

import struct
import numpy as np

def read_monthly_data(file_dir, years):
    """Reads GPCP monthly data into a combined array.

    Parameters
    ----------
    file_dir : str
        Base directory structure where files are located with trailing slash.

    years : arr of int or str
        List of file years to read in.

    Returns
    -------
    data : arr with shape [nyear, 12, 72, 144]
        Array of rainfall values for each year and month in [mm/day].

    References
    ----------
    Header and grid size information taken from GPCP documentation [1].

    .. [1] Huffman, G. J. and Bolvin, D. T., 2013: GPCP Version 2.2 SG
       Combined Precipitation Data Set Documentation. Taken from: 
       ftp://precip.gsfc.nasa.gov/pub/gpcp-v2.2/doc/V2.2_doc.pdf.
    """

    filenames = [file_dir + 'gpcp_v2.2_psg.' + str(x) for x in years]

    data = np.zeros([len(years), 12, 72, 144])
    lats = np.arange(88.75, -90, -2.5)
    lons = np.arange(1.25, 360, 2.5)

    grid_size = 144 * 72  # size of grid to read one month
    read_size = grid_size * 4  # bit count for grid_size to advance one month
    structure = ">" + ('f' * grid_size)  

    for i,fname in enumerate(filenames):
        f = open(fname,'r')
        f.seek(0)

        header = f.read(576)

        for m in range(12):
            read_data = f.read(read_size)

            data_unpack = struct.unpack(structure, read_data)
            data_unpack = np.reshape(data_unpack, [72,144])
            data[i,m,:,:] = data_unpack

    return data

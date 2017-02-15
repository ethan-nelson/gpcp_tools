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


def read_daily_data(file_dir, year, month):
    """Reads GPCP daily data into an array.

    Parameters
    ----------
    file_dir : str
        Base directory structure where files are located with trailing slash.

    year : int or str
        File year to read in.
        
    month : int or str
        File month to read in.

    Returns
    -------
    data : arr with shape [31, 72, 144]
        Array of rainfall values for each day in [mm/day]. Months that are
        not 31 days long are padded with zeroes on the end and the user is
        alerted to this early termination.

    References
    ----------
    Header and grid size information taken from GPCP documentation [1].

    .. [1] Huffman, G. J. and Bolvin, D. T., 2013: GPCP Version 1.2 One-
       Degree Daily Precipitation Data Set Documentation. Taken from:
       ftp://meso.gsfc.nasa.gov/pub/1dd-v1.2/1DD_v1.2_doc.pdf.
    """

    data = np.zeros([31, 180, 360])
    lats = np.arange(89.5, -90, -1)
    lons = np.arange(0.5, 360, 1)

    grid_size = 360 * 180  # size of grid to read one day
    read_size = grid_size * 4  # bit count for grid_size to advance one day
    structure = ">" + ('f' * grid_size)

    fname = file_dir + 'gpcp_1dd_v1.2_p1d.' + year + month.zfill(2)
    f = open(fname,'r')
    f.seek(0)

    header = f.read(1440)

    for m in range(31):
        try:
            read_data = f.read(read_size)

            data_unpack = struct.unpack(structure, read_data)
            data_unpack = np.reshape(data_unpack, [180,360])
            data[m,:,:] = data_unpack
        except:
            print 'Month has finished at %i.' % (m,)
            break

    return data

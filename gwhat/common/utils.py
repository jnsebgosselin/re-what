# -*- coding: utf-8 -*-

# Copyright © 2014-2018 GWHAT Project Contributors
# https://github.com/jnsebgosselin/gwhat
#
# This file is part of GWHAT (Ground-Water Hydrograph Analysis Toolbox).
# Licensed under the terms of the GNU General Public License.


# ---- Standard lirary imports
import csv
import os
import os.path as osp
from shutil import rmtree


# ---- Third party imports
import numpy as np
import xlsxwriter
import xlwt


def calc_dist_from_coord(lat1, lon1, lat2, lon2):
    """
    Compute the  horizontal distance in km between a location given in
    decimal degrees and a set of locations also given in decimal degrees.
    """
    lat1, lon1 = np.radians(lat1), np.radians(lon1)
    lat2, lon2 = np.radians(lat2), np.radians(lon2)

    r = 6373  # r is the Earth radius in km

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    return r * c


def find_unique_filename(filename):
    """
    Add an integer between () to the filename until a unique filename is found.
    """
    root, ext = osp.splitext(filename)
    i = 1
    while True:
        if osp.exists(filename):
            filename = root + ' (%d)' % i + ext
            i += 1
        else:
            return filename


def save_content_to_file(fname, fcontent):
    """
    Smart function that checks the extension and save the content in the
    appropriate file format.
    """
    root, ext = osp.splitext(fname)
    if ext in ['.xlsx', '.xls']:
        save_content_to_excel(fname, fcontent)
    elif ext == '.tsv':
        save_content_to_csv(fname, fcontent, delimiter='\t')
    else:
        save_content_to_csv(fname, fcontent)


def save_content_to_csv(fname, fcontent, mode='w', delimiter=',',
                        encoding='utf8'):
    """
    Save content in a csv file with the specifications provided
    in arguments.
    """
    create_dirname(fname)
    with open(fname, mode, encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, lineterminator='\n')
        writer.writerows(fcontent)


def save_content_to_excel(fname, fcontent):
    """Save content in a xls or xlsx file."""
    create_dirname(fname)
    root, ext = os.path.splitext(fname)
    if ext == '.xls':
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Data')
        for i, row in enumerate(fcontent):
            for j, cell in enumerate(row):
                ws.write(i, j, cell)
        wb.save(root+'.xls')
    else:
        try:
            with xlsxwriter.Workbook(root + '.xlsx') as wb:
                ws = wb.add_worksheet('Data')
                for i, row in enumerate(fcontent):
                    ws.write_row(i, 0, row)
        except xlsxwriter.exceptions.FileCreateError:
            raise PermissionError


def create_dirname(fname):
    """Create the dirname of a file if it doesn't exists."""
    dirname = osp.dirname(fname)
    if dirname and not osp.exists(dirname):
        os.makedirs(dirname)


def delete_file(filename):
    """Try to delete a file on the disk and return the error if any."""
    try:
        os.remove(filename)
        return None
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        return e.strerror


def delete_folder_recursively(dirpath):
    """Try to delete all files and sub-folders below the given dirpath."""
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            rmtree(filepath)
        except OSError:
            os.remove(filepath)

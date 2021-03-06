# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © GWHAT Project Contributors
# https://github.com/jnsebgosselin/gwhat
#
# This file is part of GWHAT (Ground-Water Hydrograph Analysis Toolbox).
# Licensed under the terms of the GNU General Public License.
# -----------------------------------------------------------------------------

# ---- Standard imports
import os
import os.path as osp

# ---- Third party imports
from appconfigs.base import get_home_dir

# ---- Local imports
from gwhat.config.main import CONF
from gwhat import __rootdir__


def get_select_file_dialog_dir():
    """"
    Return the directory that should be displayed by default
    in file dialogs.
    """
    directory = CONF.get('main', 'select_file_dialog_dir', get_home_dir())
    directory = directory if osp.exists(directory) else get_home_dir()
    return directory


def set_select_file_dialog_dir(directory):
    """"
    Save in the user configs the directory that should be displayed
    by default in file dialogs.
    """
    if directory is None or not osp.exists(directory):
        directory = get_home_dir()
    CONF.set('main', 'select_file_dialog_dir', directory)


def save_path_to_configs(section, option, path):
    """
    Save a path in the config file for the specified section and option.
    """
    path = osp.abspath(path)
    CONF.set(section, option, path)


def get_path_from_configs(section, option):
    """
    Return a path saved in the config file at the specified section and option.
    """
    # We need to change the working directory in case this function is not
    # called from mainwindow.py.
    cwd = os.getcwd()
    os.chdir(__rootdir__)
    path = osp.abspath(CONF.get(section, option))
    os.chdir(cwd)
    return path

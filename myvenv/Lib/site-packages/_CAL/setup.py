#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016-2020 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria.
# Web: http://www.c-tanzer.at/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    _CAL.setup
#
# Purpose
#    Setup file for package namespace CAL
#
# Revision Dates
#    11-Oct-2016 (CT) Creation
#    13-Oct-2016 (CT) Use `find_packages`, `_TFL.fs_find`, not home-grown code
#    22-Feb-2017 (CT) Use `TFL_STP`, not home-grown code
#    27-Feb-2017 (CT) Add Python 3.6 to `classifiers`
#    25-Mar-2020 (CT) Restrict Python versions to >=3.7
#    ««revision-date»»···
#--

from   setuptools               import setup

import TFL_STP as STP

STP.change_to_dir (__file__)

license = "BSD License"
name    = "CAL"
p_name  = "_CAL"

version              = STP.package_version ()
long_description     = STP.long_description ()
packages, data_files = STP.packages_plus_data_files (p_name)
Test_Command         = STP.Test_Command

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = version
    , description          =
        "Package dealing with date, time, and calendars."
    , long_description     = long_description
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://github.com/Tapyr/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = "Any"
    , classifiers          = \
        [ "Development Status :: 5 - Production/Stable"
        , "License :: OSI Approved :: " + license
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Intended Audience :: Developers"
        , "Topic :: Software Development :: Libraries :: Python Modules"
        ]
    , python_requires      = ">=3.7"
    , setup_requires       = ["TFL_STP>=3"]
    , install_requires     = ["TFL>=3", "python-dateutil"]
    , extras_require       = dict
        ( icalendar            = ["icalendar"]
        , pdf                  = ["reportlab"]
        )
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )

### __END__ _CAL.setup

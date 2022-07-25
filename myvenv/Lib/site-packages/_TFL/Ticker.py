# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Ticker
#
# Purpose
#    Provide classes to determine tick-marks for data plots
#
# Revision Dates
#     5-Jun-2017 (CT) Creation
#    12-Jul-2018 (CT) Add `** kwds`, `labels` to `_Axis_`
#    29-Nov-2018 (CT) Add divisors to `scaled_deltas` in `Base.scaled`
#     2-Dec-2018 (CT) Improve computation of `sub_ticks`
#                     + Move computation of `major_delta`, `sub_ticks` to `Base`
#     5-Dec-2018 (CT) Add `label_delta`
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _TFL.Divisor_Dag           import Divisor_Dag
from   _TFL.formatted_repr        import formatted_repr
from   _TFL.Math_Func             import log, log2, log10, sign
from   _TFL.portable_repr         import portable_repr
from   _TFL.predicate             import \
    is_int, pairwise, rounded_down, rounded_to, rounded_up, uniq
from   _TFL.pyk                   import pyk
from   _TFL.Range                 import Float_Range_Discrete as F_Range

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._Meta.Property        import Optional_Computed_Once_Property

import _TFL._Meta.Object

import itertools
import operator

class Axis (TFL.Meta.Object) :
    """Axis with tick marks for a data range of a certain `Base`.

    An `Axis` instance is defined by a :class:`Base` instance :attr:`base`, and
    minimum and maximum data values, :attr:`data_min` and :attr:`data_max`, to
    be displayed.

    >>> ax1 = Axis (base_10, 0, 100)

    >>> print (ax1.data_min, ax1.data_max)
    0 100

    Based on :attr:`base` and the data range, an `Axis` instance determines the
    minimum and maximum values of the axis and the tick marks to be displayed.

    :attr:`major_delta` is the distance between major tick marks:
    >>> print (ax1.major_min, ax1.major_max, ax1.major_delta)
    0 100 10

    Axis extreme values:
    >>> print (ax1.ax_min, ax1.ax_max)
    -10 110

    Major tick marks:
    >>> print (ax1.major_range)
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    Medium tick marks:
    >>> print (ax1.medium_range)
    [-5.0, 5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0, 105.0]

    Minor tick marks:
    >>> print (ax1.minor_range)
    [-9.0, -8.0, -7.0, -6.0, -4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 11.0, 12.0, 13.0, 14.0, 16.0, 17.0, 18.0, 19.0, 21.0, 22.0, 23.0, 24.0, 26.0, 27.0, 28.0, 29.0, 31.0, 32.0, 33.0, 34.0, 36.0, 37.0, 38.0, 39.0, 41.0, 42.0, 43.0, 44.0, 46.0, 47.0, 48.0, 49.0, 51.0, 52.0, 53.0, 54.0, 56.0, 57.0, 58.0, 59.0, 61.0, 62.0, 63.0, 64.0, 66.0, 67.0, 68.0, 69.0, 71.0, 72.0, 73.0, 74.0, 76.0, 77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 86.0, 87.0, 88.0, 89.0, 91.0, 92.0, 93.0, 94.0, 96.0, 97.0, 98.0, 99.0, 101.0, 102.0, 103.0, 104.0, 106.0, 107.0, 108.0, 109.0]

    By default `Axis` uses a margin of one major tick mark on each side.
    Passing :attr:`margin` to the `Axis` constructor changes the :attr:`ax_min`
    and :attr:`ax_max`.

    >>> ax2 = Axis (base_10, 0, 100, margin = 0, max_major_ticks = 7)
    >>> print (ax2.data_min, ax2.data_max)
    0 100
    >>> print (ax2.major_min, ax2.major_max, ax2.major_delta)
    0 100 20
    >>> print (ax2.ax_min, ax2.ax_max)
    0 100

    Major tick marks:
    >>> print (ax2.major_range)
    [0, 20, 40, 60, 80, 100]

    Medium tick marks:
    >>> print (ax2.medium_range)
    [5.0, 10.0, 15.0, 25.0, 30.0, 35.0, 45.0, 50.0, 55.0, 65.0, 70.0, 75.0, 85.0, 90.0, 95.0]

    Minor tick marks:
    >>> print (ax2.minor_range)
    [1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 11.0, 12.0, 13.0, 14.0, 16.0, 17.0, 18.0, 19.0, 21.0, 22.0, 23.0, 24.0, 26.0, 27.0, 28.0, 29.0, 31.0, 32.0, 33.0, 34.0, 36.0, 37.0, 38.0, 39.0, 41.0, 42.0, 43.0, 44.0, 46.0, 47.0, 48.0, 49.0, 51.0, 52.0, 53.0, 54.0, 56.0, 57.0, 58.0, 59.0, 61.0, 62.0, 63.0, 64.0, 66.0, 67.0, 68.0, 69.0, 71.0, 72.0, 73.0, 74.0, 76.0, 77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 86.0, 87.0, 88.0, 89.0, 91.0, 92.0, 93.0, 94.0, 96.0, 97.0, 98.0, 99.0]

    >>> ax3 = Axis (base_10, 0, 100, margin = 0.5)
    >>> print (ax3.data_min, ax3.data_max)
    0 100
    >>> print (ax3.major_min, ax3.major_max, ax3.major_delta)
    0 100 10
    >>> print (ax3.ax_min, ax3.ax_max)
    -5.0 105.0

    >>> ax4 = Axis (base_10, 0, 100, major_delta = 25, margin = 0)
    >>> print (ax4.major_delta, ax4.medium_delta, ax4.minor_delta)
    25 5.0 1.0
    >>> print (ax4.major_range)
    [0, 25, 50, 75, 100]
    >>> print (ax4.medium_range)
    [5.0, 10.0, 15.0, 20.0, 30.0, 35.0, 40.0, 45.0, 55.0, 60.0, 65.0, 70.0, 80.0, 85.0, 90.0, 95.0]
    >>> print (ax4.minor_range)
    [1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 11.0, 12.0, 13.0, 14.0, 16.0, 17.0, 18.0, 19.0, 21.0, 22.0, 23.0, 24.0, 26.0, 27.0, 28.0, 29.0, 31.0, 32.0, 33.0, 34.0, 36.0, 37.0, 38.0, 39.0, 41.0, 42.0, 43.0, 44.0, 46.0, 47.0, 48.0, 49.0, 51.0, 52.0, 53.0, 54.0, 56.0, 57.0, 58.0, 59.0, 61.0, 62.0, 63.0, 64.0, 66.0, 67.0, 68.0, 69.0, 71.0, 72.0, 73.0, 74.0, 76.0, 77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 86.0, 87.0, 88.0, 89.0, 91.0, 92.0, 93.0, 94.0, 96.0, 97.0, 98.0, 99.0]

    >>> ax5 = Axis (base_10, 0, 1, major_delta = 0.25, margin = 0)
    >>> print (ax5.major_delta, ax5.medium_delta, ax5.minor_delta)
    0.25 0.05 0.01

    >>> ax6 = Axis (base_10, 0, 10, major_delta = 2.5, margin = 0)
    >>> print (ax6.major_delta, ax6.medium_delta, ax6.minor_delta)
    2.5 0.5 0.1

    >>> ax7 = Axis (base_month, 0, 42, margin = 0)
    >>> print (ax7.major_delta, ax7.medium_delta, ax7.minor_delta)
    3 1.0 0

    >>> ax8 = Axis (base_10, 0, 72, major_delta = 8, margin = 0.25)
    >>> print (ax8.major_delta, ax8.medium_delta, ax8.minor_delta)
    8 2.0 1.0

    >>> ax9 = Axis (base_degree, 0, 360, major_delta = 30, margin = 0)
    >>> print (ax9.major_delta, ax9.medium_delta, ax9.minor_delta)
    30 15.0 5.0

    """

    label_delta             = 1
    label_fill              = None
    major_lines             = ""
    max_major_ticks         = 20
    max_ticks               = 100
    minor_lines             = ""
    _labels                 = None

    def __init__ \
            ( self, base, data_min, data_max
            , ax_min            = None
            , ax_max            = None
            , margin            = 1
            , max_major_ticks   = None
            , max_ticks         = None
            , major_delta       = None
            , major_offset      = 0
            , medium_lines      = None
            , medium_ticks      = None
            , minor_ticks       = None
            , round_extrema     = True
            , ** kwds
            ) :
        self.base               = base
        self.data_min           = data_min
        self.data_max           = data_max
        if ax_min is not None :
            self.ax_min         = ax_min
        if ax_max is not None :
            self.ax_max         = ax_max
        self.margin             = margin
        if max_major_ticks is not None :
            self.max_major_ticks= max_major_ticks
        if max_ticks is not None :
            self.max_ticks      = max_ticks
        if major_delta is not None :
            self.major_delta    = major_delta
        self.major_offset       = major_offset
        if medium_lines is not None :
            self.medium_lines   = medium_lines
        if medium_ticks is not None :
            self.medium_ticks   = medium_ticks
        if minor_ticks is not None :
            self.minor_ticks    = minor_ticks
        self.round_extrema      = round_extrema
        self.pop_to_self     (kwds, "labels", prefix = "_")
        self.__dict__.update (** kwds)
    # end def __init__

    @Optional_Computed_Once_Property
    def ax_max (self) :
        """Maximum value of axis."""
        d_max   = self.data_max
        m_max   = self.major_max
        delta   = self.margin_delta
        result  = max (m_max, d_max + delta) \
            if d_max != m_max else m_max + delta
        return result
    # end def ax_max

    @Optional_Computed_Once_Property
    def ax_min (self) :
        """Minimum value of axis."""
        d_min   = self.data_min
        m_min   = self.major_min
        delta   = self.margin_delta
        result  = min (m_min, d_min - delta) \
            if d_min != m_min else m_min - delta
        return result
    # end def ax_min

    @Once_Property
    def data_length (self) :
        """Difference between `self.data_max` and `self.data_min`."""
        return abs (self.data_max - self.data_min)
    # end def data_length

    @property
    def labels (self) :
        ld     = self.label_delta
        result = self._labels
        if result is True :
            result = self._labels = \
                tuple (formatted_repr (m) for m in self.major_range)
        if ld > 1 :
            def _gen (result, ld) :
                for r in result [::ld] :
                    yield r
                    for i in range (ld - 1) :
                        yield ""
            result = tuple (_gen (result, ld))
        return result
    # end def labels

    @labels.setter
    def labels (self, value) :
        self._labels = value
    # end def labels

    @Optional_Computed_Once_Property
    def major_delta (self) :
        """Delta between major tick marks."""
        return self.scaled.major_tick_delta \
            (float (self.data_length), self.max_major_ticks)
    # end def major_delta

    @Once_Property
    def major_max (self) :
        """Maximum major tick mark."""
        result = rounded_up (self.data_max, self.major_delta) \
            if self.round_extrema else self.data_max
        if not self.data_length :
            result += self.major_delta
        return result
    # end def major_max

    @Once_Property
    def major_min (self) :
        """Minimum major tick mark."""
        result = rounded_down (self.data_min, self.major_delta) \
            if self.round_extrema else self.data_min
        if not self.data_length :
            result -= self.major_delta
        return result
    # end def major_min

    @Once_Property
    def major_range (self) :
        """Range of values of major tick marks."""
        ax_min       = self.ax_min
        ax_max       = self.ax_max
        data_min     = self.data_min
        data_max     = self.data_max
        major_delta  = self.major_delta
        major_min    = self.major_min + self.major_offset
        major_max    = self.major_max
        margin_delta = self.margin_delta
        if major_min - ax_min > major_delta :
            major_min -= major_delta * int ((major_min - ax_min) / major_delta)
        if ax_max - major_max > major_delta :
            major_max += major_delta * int ((ax_max - major_max) / major_delta)
        bounds       = "".join \
            ( ( "[" if data_min != ax_min or not margin_delta else "("
              , "]" if data_max != ax_max or not margin_delta else ")"
              )
            )
        result = F_Range (major_min, major_max, bounds, delta = major_delta)
        return list (result)
    # end def major_range

    @Once_Property
    def margin_delta (self) :
        """Delta between first/last major tick mark and end of axis."""
        return self.major_delta * self.margin
    # end def margin_delta

    @Once_Property
    def medium_delta (self) :
        """Delta between major and medium tick marks."""
        medium_ticks = self.medium_ticks
        return self.major_delta / (medium_ticks + 1.0) if medium_ticks else 0
    # end def medium_delta

    @Optional_Computed_Once_Property
    def medium_lines (self) :
        return self.major_lines and bool (self.medium_range)
    # end def medium_lines

    @Once_Property
    def medium_range (self) :
        """Range of values of medium tick marks."""
        return list (self._gen_tick_marks (self.medium_delta, self.major_range))
    # end def medium_range

    @Optional_Computed_Once_Property
    def medium_ticks (self) :
        """Number of medium tick marks between each pair of major tick marks."""
        return self.sub_ticks [0]
    # end def medium_ticks

    @Once_Property
    def minor_delta (self) :
        """Delta between major/medium and minor tick marks."""
        minor_ticks = self.minor_ticks
        delta       = self.medium_delta or self.major_delta
        return delta / (minor_ticks + 1.0) if minor_ticks else 0
    # end def minor_delta

    @Once_Property
    def minor_range (self) :
        """Range of values of minor tick marks."""
        delta  = self.minor_delta
        result = []
        if delta :
            higher_range = sorted \
                (itertools.chain (self.major_range, self.medium_range))
            result       = list (self._gen_tick_marks (delta, higher_range))
        return result
    # end def minor_range

    @Optional_Computed_Once_Property
    def minor_ticks (self) :
        """Number of minor tick marks between each pair of major/medium tick marks."""
        return self.sub_ticks [1]
    # end def minor_ticks

    @Once_Property
    def scaled (self) :
        """Base scaled to `data_length`."""
        return self.base.scaled (self.data_length)
    # end def scaled

    @Once_Property
    def sub_ticks (self) :
        major_ticks = len (self.major_range) - 1
        limit       = rounded_to (self.max_ticks / major_ticks, 1)
        result      = self.scaled.sub_ticks (self.major_delta, limit)
        return result
    # end def sub_ticks

    def adjust_major_offset (self, start_value) :
        """Adjust `major_offset`  to force major ticks to multiples of `major_delta`"""
        m_delta = self.major_delta
        rr      = start_value % m_delta
        result  = self.major_offset = m_delta - rr if rr else rr
        return result
    # end def adjust_major_offset

    def _gen_tick_marks (self, delta, higher_tick_marks) :
        if delta :
            def _gen (delta, higher_tick_marks) :
                cmp_op = operator.lt if delta > 0 else operator.gt
                eps    = delta / 10
                for l, r in pairwise (higher_tick_marks) :
                    r  = r - eps
                    t  = l + delta
                    while cmp_op (t, r) :
                        yield t
                        t += delta
            return itertools.chain \
                ( reversed
                    (list (_gen (-delta, [higher_tick_marks [0], self.ax_min])))
                , _gen (delta, higher_tick_marks)
                , _gen (delta, [higher_tick_marks [-1], self.ax_max])
                )
        return ()
    # end def _gen_tick_marks

    def __str__ (self) :
        result = "%s (%r, %s, %s, %s, %s, %s, %s, %s)" % \
            ( self.__class__.__name__, self.base
            , self.data_min, self.data_max
            , self.ax_min, self.ax_max
            , self.margin
            , self.max_major_ticks, self.max_ticks
            )
        return result
    # end def __str__

# end class Axis

class Base (TFL.Meta.Object) :
    """Number base for tick mark determination.

    >>> b = Base (10)
    >>> print (b)
    10 : (1, 2, 5, 10)

    >>> print (b.scaled (15000))
    10 ^ 3 : (1000, 1250, 2000, 2500, 5000, 10000)
    >>> print (b.scaled (10000))
    10 ^ 3 : (1000, 1250, 2000, 2500, 5000, 10000)
    >>> print (b.scaled (1000))
    10 ^ 2 : (100, 125, 200, 250, 500, 1000)
    >>> print (b.scaled (100))
    10 ^ 1 : (10, 20, 25, 50, 100)
    >>> print (b.scaled (10))
    10 : (1, 2, 5, 10)
    >>> print (b.scaled (1))
    10 ^ -1 : (0.1, 0.2, 0.5, 1)
    >>> print (b.scaled (0.1))
    10 ^ -2 : (0.01, 0.02, 0.05, 0.1)
    >>> print (b.scaled (0.01))
    10 ^ -3 : (0.001, 0.002, 0.005, 0.01)
    >>> print (b.scaled (0.001))
    10 ^ -4 : (0.0001, 0.0002, 0.0005, 0.001)
    >>> print (b.scaled (0.0005))
    10 ^ -4 : (0.0001, 0.0002, 0.0005, 0.001)

    """

    scale_factor = 1

    def __init__ \
            ( self, base
            , deltas           = None
            , log_round_amount = None
            , scale            = 0
            , ** kwds
            ) :
        self.base   = base
        self.deltas = \
            ( None if deltas is None else sorted
                (uniq (itertools.chain (deltas, ([] if scale else [1, base]))))
            )
        self.lra    = log_round_amount
        self.scale  = scale
        self._kwds  = kwds
        self.pop_to_self     (kwds, "base_deltas")
        self.__dict__.update (kwds)
        if base == 10 :
            self.log = log10
    # end def __init__

    @Optional_Computed_Once_Property
    def base_deltas (self) :
        return self.deltas
    # end def base_deltas

    @property
    def deltas (self) :
        """Possible deltas between tick marks for values of this `Base`"""
        result = self._deltas
        if result is None :
            result = self._deltas = tuple (Divisor_Dag (self.base).divisors)
        return result
    # end def deltas

    @deltas.setter
    def deltas (self, value) :
        self._deltas = tuple (value) if value is not None else None
    # end def deltas

    def log (self, v) :
        """Logarithm of base `self.base` of `v`."""
        return log (v, self.base)
    # end def log

    def log_rounded (self, v) :
        """Logarithm of base `self.base` of `v` rounded to `int`."""
        log_v  = self.log (v) if v else 1.0
        lra    = self.lra
        if lra is not None :
            result = int (log_v + lra)
        else :
            result = rounded_to (log_v, 1.0)
        return int (result)
    # end def log_rounded

    def major_tick_delta (self, data_length, max_ticks) :
        deltas = self.deltas
        for d in deltas :
            if rounded_up (data_length / d, 1.0) <= max_ticks :
                result = d
                break
        else :
            result = deltas [-1]
        return result
    # end def major_tick_delta

    def scaled (self, delta) :
        """`Base` scaled to range of `delta`"""
        scale = self.log_rounded (delta) - 1
        if scale :
            base          = self.base
            factor        = base ** scale
            scaled_deltas = tuple (delta * factor for delta in self.deltas)
            if scale > 0 :
                sds       = set (scaled_deltas)
                sds.update  (Divisor_Dag (base * factor).divisors)
                scaled_deltas = sorted (d for d in sds if factor <= d <= delta)
            result        = self.__class__ \
                ( base, scaled_deltas, self.lra, scale
                , base_deltas  = self.base_deltas
                , scale_factor = factor
                , ** self._kwds
                )
        else :
            result        = self
        return result
    # end def scaled

    def sub_ticks (self, delta, limit, medium_limit = 4) :
        base        = self.base
        b_divs      = self.base_deltas
        if delta < base :
            ### scale `delta` to interval `base .. base * base`
            s_factor    = min (self.scale_factor, 1)
            s_delta     = (delta / s_factor) * base
            deltas      = tuple (d * s_factor for d in b_divs)
        else :
            s_delta     = delta
            deltas      = self.deltas
        delta_divs  = Divisor_Dag (s_delta).divisors
        med_cands   = sorted ((d - 1 for d in delta_divs), reverse = True)
        minor_divs  = sorted \
            ( (   d
              for d in set (itertools.chain (b_divs, deltas))
              if  1 < d <= limit
              )
            , reverse = True
            )
        minor_limit = rounded_up (base / 2, 1.0)
        def _gen (s_delta) :
            valid_tick = self._valid_tick
            for medium in med_cands :
                if 1 <= medium <= limit :
                    if valid_tick (delta, medium) :
                        total = 0
                        if medium <= medium_limit :
                            total   = medium
                            minor   = 0
                            lim     = min (limit / (medium + 1), minor_limit)
                            delta_m = delta / (medium + 1)
                            for md in minor_divs :
                                md_1 = md - 1
                                if md <= lim and valid_tick (delta_m, md_1) :
                                    minor  = md_1
                                    total += (medium + 1) * minor
                                    break
                        else :
                            if medium <= minor_limit :
                                total, medium, minor = medium, 0, medium
                        if total :
                            yield total, medium, minor
        def sk (cand) :
            total, medium, minor = cand
            both_p      = - bool (medium and minor)
            prio_med    = - bool (medium)
            prio_min    = - bool (minor)
            more_p      = - total
            more_med    = - medium
            if prio_med :
                ### prefer `medium` values that are
                ### + power-of-two
                ### + divisors of `s_delta`
                prio_med -= \
                    (   is_int (log2 (medium + 1))
                    and is_int (s_delta / (medium + 1))
                    )
            if prio_min :
                ### prefer `minor` values that are divisors of `delta`
                prio_min -= is_int (delta / (minor + 1))
            result  = \
                ( prio_med ### medium : power-of-two, divisors of `s_delta`
                , prio_min ### minor  : divisors of `delta`
                , more_p   ### bigger number of sub-ticks
                , both_p   ### alternatives with both `medium` and `minor`
                , more_med ### medium : larger number
                )
            return result
        candidates  = sorted (_gen (s_delta), key = sk) or [(0, 0, 0)]
        return candidates [0] [1:]
    # end def sub_ticks

    def _valid_tick (self, delta, n) :
        return True
    # end def _valid_tick

    def __repr__ (self) :
        return "%s (%s, %s)" % \
            (self.__class__.__name__, self.base, self.deltas [1:-1])
    # end def __repr__

    def __str__ (self) :
        s = self.scale
        return "%2d%s : %s" % \
            (self.base, (" ^ %s" % s) if s else "", portable_repr (self.deltas))
    # end def __str__

# end class Base

class Base_Integral (Base) :
    """Intgral number base for tick mark determination."""

    def major_tick_delta (self, data_length, max_ticks) :
        result = self.__super.major_tick_delta (data_length, max_ticks)
        if result and result < 1 :
            result = 1
        return result
    # end def major_tick_delta

    def _valid_tick (self, delta, n) :
        result = is_int (delta  / (n + 1))
        return result
    # end def _valid_tick

# end class Base_Integral

base_10         = Base          ( 10)
base_12         = Base          ( 12)
base_16         = Base          ( 16, (4, 8))
base_day        = Base_Integral ( 28, (7, 14))
base_degree     = Base          (360, (3, 15, 22.5, 30, 45, 60, 90, 180))
base_hour       = Base_Integral ( 24, (3, 6, 12))
base_hour_f     = Base          ( 24, (3, 6, 12))
base_month      = Base_Integral ( 12, (3, 6),    log_round_amount = 0.0)
base_quarter    = Base_Integral (  4,            log_round_amount = 0.0)
base_week       = Base_Integral ( 52,            log_round_amount = 0.0)

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Ticker

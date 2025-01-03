# Rounds a measurement value and its uncertainty

Rounds a measurement value and its uncertainty to a specified number
of significant digits.

First, the measurement uncertainty is rounded, 
by default to one significant digit unless this (first) significant digit is 1,
in which case it is rounded to two significant digits. 
Rounding is always done upwards, that is, to a greater value unless
rounding down is more reasonable (the second significant digit is zero), 
for example, 0.502 will be rounded to 0.5, not to 0.6. 
The number of significant digits can be explicitly specified, 
in which case the rounded value will always have as many significant digits as specified.

Next, the value itself is rounded so that it has 
the same number of decimal places as the measurement uncertainty.

Trailing zeros in these values are also considered significant, 
so a value of 0.50 indicates that we are confident that 
the second decimal place is zero. 
Writing 0.5 instead of 0.50 would suggest an unknown (unmeasured) value
of the hundredths place, and such ambiguities are to be avoided.

The results are returned as a string to avoid potential formatting
difficulties with numbers (which might lose trailing zeros).
The current version, in accordance with the concept used in Python,
always uses a dot as the decimal separator.

Examples:

    >>> precise_rounding(123.45678, 0.0215)
    ('123.46', '0.03')

    >>> precise_rounding(123.45678, 0.01009)
    ('123.457', '0.010')

    >>> precise_rounding(123.4545, 0.07234, 2)
    ('123.455', '0.073')

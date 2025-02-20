from math import ceil, fabs, floor


def precise_rounding(value, uncertainty, uncertainty_digits='auto'):
    """
    Rounds a measurement value and its uncertainty to a specified number
    of significant digits.

    Args:
        value (float): The measurement value.
        uncertainty (float): The uncertainty of the measurement.
        uncertainty_digits (int, optional): The number of significant
            digits for the uncertainty. Defaults to 'auto', which gives
            two (when leading digit is 1) or one significant digit.

    Returns:
        tuple: A tuple containing the rounded value and the rounded
            uncertainty as strings.

    Raises:
        ValueError: If uncertainty is negative.
        ValueError: If uncertainty_digits is less than 1.
        TypeError: If value or uncertainty cannot be converted to float.

    Examples:
        >>> precise_rounding(123.45678, 0.0215)
        ('123.46', '0.03')

        >>> precise_rounding(123.45678, 0.01009)
        ('123.457', '0.010')

        >>> precise_rounding(123.4545, 0.07234, 2)
        ('123.455', '0.073')

        >>> precise_rounding(123.4545, 0, 2)
        ('123.4545', '0.0000')
    """
    measurement = PreciseRounding(value, uncertainty)
    if uncertainty_digits != 'auto':
        measurement.uncertainty_digits = uncertainty_digits
    return measurement.value, measurement.uncertainty


class PreciseRounding:
    """
    A class to handle precise rounding of a measurement value and its
    uncertainty.

    Attributes:
        _value (float): The measurement value.
        _uncertainty (float): The uncertainty of the measurement.
        _uncertainty_digits (int): The number of significant digits for
            the uncertainty.
        _auto_uncertainty_digits (bool): Flag to determine if uncertainty
            digits are set automatically.
        _value_rounded_str (str): The rounded measurement value as a
            string.
        _uncertainty_rounded_str (str): The rounded uncertainty as a
            string.
    """

    def __init__(self, value, uncertainty):
        """
        Initializes the PreciseRounding class with the given value and
        uncertainty.

        Args:
            value (float): The measurement value.
            uncertainty (float): The uncertainty of the measurement.
        """
        self._value = value
        self._uncertainty = uncertainty
        self._uncertainty_digits = 2  # provisional
        self._auto_uncertainty_digits = True
        self._value_rounded_str = None
        self._uncertainty_rounded_str = None
        self._compute()

    def __str__(self):
        """
        Returns a string representation of the rounded value and
        uncertainty.

        Returns:
            str: The rounded value and uncertainty in the format
                'value±uncertainty'.
        """
        return self.value + '±' + self.uncertainty

    @property
    def uncertainty_digits(self):
        """
        Gets the number of significant digits for the uncertainty.

        Returns:
            int: The number of significant digits for the uncertainty.
        """
        return self._uncertainty_digits

    @uncertainty_digits.setter
    def uncertainty_digits(self, uncertainty_digits):
        """
        Sets the number of significant digits for the uncertainty.

        Args:
            uncertainty_digits (int or str): The number of significant
                digits for the uncertainty. If set to 'auto', the number
                of digits is determined automatically.
        """
        if uncertainty_digits == 'auto':
            self._auto_uncertainty_digits = True
            self._uncertainty_digits = 2
        else:
            self._auto_uncertainty_digits = False
            self._uncertainty_digits = uncertainty_digits
        self._compute()

    @property
    def value(self):
        """
        Gets the rounded measurement value as a string.

        Returns:
            str: The rounded measurement value.
        """
        return self._value_rounded_str

    @property
    def uncertainty(self):
        """
        Gets the rounded uncertainty as a string.

        Returns:
            str: The rounded uncertainty.
        """
        return self._uncertainty_rounded_str

    def is_exact(self):
        """
        Checks if the uncertainty is zero.

        Returns:
            bool: True if the uncertainty is zero, False otherwise.
        """
        return self._uncertainty == 0

    @property
    def relative_uncertainty(self):
        """
        Calculates the relative uncertainty.

        Returns:
            float: The relative uncertainty.
        """
        if self._value == 0 and self._uncertainty == 0:
            relative = float('nan')
        elif self._value == 0:
            relative = float('inf')
        else:
            relative = abs(self._uncertainty) / abs(self._value)
            # TODO: rounding to 2 significant digits
        return relative

    def _compute(self):
        """
        Rounds a measurement value and its uncertainty to a specified
        number of significant digits.
        """
        # Ensure the inputs can be converted to numbers
        #
        try:
            self._value = float(self._value)
        except ValueError:
            raise TypeError("value must be a number")
        try:
            self._uncertainty = float(self._uncertainty)
        except ValueError:
            raise TypeError("uncertainty must be a number")
        try:
            self._uncertainty_digits = int(self._uncertainty_digits)
        except ValueError:
            raise TypeError("uncertainty_digits must be a number")

        # Ensure the uncertainty and uncertainty_digits are valid
        #
        if self._uncertainty < 0:
            raise ValueError("uncertainty must be non-negative")
        if self._uncertainty_digits != 'auto' and self._uncertainty_digits < 1:
            raise ValueError("uncertainty_digits must be at least 1 or 'auto'")

        # Handle NaN
        #
        if self._value != self._value:  # is NaN
            raise ValueError("value is not-a-number (NaN)")
        if self._uncertainty != self._uncertainty:  # is NaN
            raise ValueError("uncertainty is not-a-number (NaN)")

        if self._uncertainty != 0:            
            # Repeat the calculations thrice to handle rounding edge cases
            #
            uncertainty = self._uncertainty
            uncertainty_digits = self._uncertainty_digits
            for i in range(3 if self._auto_uncertainty_digits else 2):
                significand, characteristic, exponential = (
                    self._decompose(uncertainty))
                factor = 10 ** (uncertainty_digits - 1)
                threshold = 0.1 * exponential / factor

                # Round uncertainty up and down
                uncertainty_rounded_up = (
                    exponential * ceil(significand * factor) / factor)
                uncertainty_rounded_down = (
                    exponential * floor(significand * factor) / factor)

                # Determine the rounded uncertainty
                if fabs(uncertainty_rounded_down - uncertainty) <= threshold:
                    uncertainty = uncertainty_rounded_down
                else:
                    uncertainty = uncertainty_rounded_up

                if self._auto_uncertainty_digits:
                    # Automatically choose the number of significant digits
                    uncertainty_digits = 1 if int(significand) != 1 else 2

            # Round value using scientific rounding
            ef = exponential / factor
            if self._value >= 0:
                value_rounded = ef * int(self._value / ef + 0.5)
            else:
                value_rounded = - ef * int(-self._value / ef + 0.5)

            # Format the rounded value and uncertainty as strings
            if uncertainty != int(uncertainty):
                n_digits = uncertainty_digits - characteristic - 1
                self._uncertainty_rounded_str = (
                    f"{uncertainty:.{n_digits}f}")
                self._value_rounded_str = f"{value_rounded:.{n_digits}f}"
            else:
                self._uncertainty_rounded_str = f"{uncertainty:.0f}"
                self._value_rounded_str = f"{value_rounded:.0f}"
                emitted_u_digits = len(self._uncertainty_rounded_str)
                if emitted_u_digits < uncertainty_digits:
                    padding = "." + "0" * (
                        uncertainty_digits - emitted_u_digits)
                    self._uncertainty_rounded_str += padding
                    self._value_rounded_str += padding
        else:
            # Handle the case where uncertainty is zero.
            assert self._uncertainty == 0
            self._value_rounded_str = str(self._value)
            self._uncertainty_rounded_str = "0"
            if "." in self._value_rounded_str:
                self._value_rounded_str = (self._value_rounded_str.
                                           rstrip("0").rstrip("."))
            if "." in self._value_rounded_str:
                length = len(self._value_rounded_str)
                position = self._value_rounded_str.index('.')
                number_frac_digits = length - position - 1
                self._uncertainty_rounded_str = (
                    "0." + "0" * number_frac_digits)

    @staticmethod
    def _decompose(value):
        """
        Decomposes a floating point value into its characteristic,
        significand, and exponent.

        This method calculates the characteristic, significand,
        and exponent of a given floating point value.
        The characteristic is adjusted to ensure the significand
        is within the range [0.1, 1.0).

        Args:
            value (float): Floating point value to decompose.

        Returns:
            tuple: A tuple containing the characteristic (int),
                significand (float), and exponent (float).
        """
        significand = value
        characteristic = 0
        exponent = 1

        # Adjust characteristic and significand for values < 1.0
        while significand < 1.0:
            characteristic -= 1
            exponent = 10 ** characteristic
            significand = value / exponent

        # Adjust characteristic and significand for values >= 10.0
        while significand >= 10.0:
            characteristic += 1
            exponent = 10 ** characteristic
            significand = value / exponent

        return significand, characteristic, exponent

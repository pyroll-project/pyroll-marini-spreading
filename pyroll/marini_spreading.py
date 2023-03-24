import numpy as np
from pyroll.core import RollPass, root_hooks, Unit, ThreeRollPass
from pyroll.core.hooks import Hook

VERSION = "2.0"

root_hooks.add(Unit.OutProfile.width)
RollPass.first_marini_parameter = Hook[float]()
"""First parameter a of Marini's spread equation."""

RollPass.second_marini_parameter = Hook[float]()
"""Second parameter b of Marini's spread equation."""


@RollPass.first_marini_parameter
def first_marini_parameter(self: RollPass):
    import pyroll.interface_friction

    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return np.sqrt(equivalent_height_change) / (
            2 * self.coulomb_friction_coefficient * np.sqrt(self.roll.working_radius))


@RollPass.second_marini_parameter
def second_marini_parameter(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return np.sqrt(equivalent_height_change / self.roll.working_radius)


# noinspection PyUnresolvedReferences
@RollPass.spread
def spread(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    numerator = 2 * equivalent_height_change * self.in_profile.equivalent_width * (
            self.roll.working_radius - self.in_profile.equivalent_height / 2) * self.second_marini_parameter

    first_denominator = self.out_profile.equivalent_height * self.in_profile.equivalent_width

    second_denominator = (self.in_profile.equivalent_width * (
            self.in_profile.equivalent_height + self.out_profile.equivalent_height) / 2) * (
                                 (1 + self.first_marini_parameter) / (1 - self.first_marini_parameter))

    third_denominator = (0.91 * (
            self.in_profile.equivalent_width + 3 * self.in_profile.equivalent_height)) / (
                                4 * self.in_profile.equivalent_height)

    fourth_denominator = 2 * self.out_profile.equivalent_height * self.roll.working_radius * self.second_marini_parameter

    return (
            1 + (numerator / (
            first_denominator + second_denominator * third_denominator + fourth_denominator)) / self.in_profile.equivalent_width
    )


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.spread * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.spread * rp.in_profile.width

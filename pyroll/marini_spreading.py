import logging
import numpy as np

from pyroll.core import RollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.0b"

RollPass.coulomb_friction_coefficient = Hook[float]()
RollPass.marini_parameter_a = Hook[float]()
RollPass.marini_parameter_b = Hook[float]()


@RollPass.coulomb_friction_coefficient
def coulomb_friction_coefficient(self: RollPass):
    raise ValueError("You must provide a friction coefficient to use the pyroll-marini-spreading plugin.")


@RollPass.marini_parameter_a
def marini_parameter_a(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return np.sqrt(equivalent_height_change) / (
            2 * self.coulomb_friction_coefficient * np.sqrt(self.roll.working_radius))


@RollPass.hookimpl
def marini_parameter_b(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    return np.sqrt(equivalent_height_change / self.roll.working_radius)


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    roll_pass = self.roll_pass()
    log = logging.getLogger(__name__)

    if not self.has_set_or_cached("width"):
        self.width = self.roll.groove.usable_width

    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    numerator = 2 * equivalent_height_change * roll_pass.in_profile.equivalent_width * (
            roll_pass.roll.working_radius - roll_pass.in_profile.equivalent_height / 2) * roll_pass.marini_parameter_b

    first_denominator = roll_pass.out_profile.equivalent_height * roll_pass.in_profile.equivalent_width

    second_denominator = (roll_pass.in_profile.equivalent_width * (
            roll_pass.in_profile.equivalent_height + roll_pass.out_profile.equivalent_height) / 2) * (
                                 (1 + roll_pass.marini_parameter_a) / (1 - roll_pass.marini_parameter_a))

    third_denominator = (0.91 * (
            roll_pass.in_profile.equivalent_width + 3 * roll_pass.in_profile.equivalent_height)) / (
                                4 * roll_pass.in_profile.equivalent_height)

    fourth_denominator = 2 * roll_pass.out_profile.equivalent_height * roll_pass.roll.working_radius * roll_pass.marini_parameter_b

    spread = 1 + (numerator / (
            first_denominator + second_denominator * third_denominator + fourth_denominator)) / roll_pass.in_profile.equivalent_rectangle.width

    log.info(f"Spread after Marini spreading model: {spread}.")

    return spread * self.in_profile.width


root_hooks.add(Unit.OutProfile.width)

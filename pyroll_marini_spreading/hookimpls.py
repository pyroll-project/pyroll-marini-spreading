import logging
import sys

import numpy as np
from pyroll import RollPass


@RollPass.hookimpl
def friction_coefficient(roll_pass: RollPass):
    return 0.2


@RollPass.hookimpl
def equivalent_height_change(roll_pass: RollPass):
    return roll_pass.in_profile.equivalent_rectangle.height - roll_pass.out_profile.equivalent_rectangle.height


@RollPass.hookimpl
def marini_parameter_a(roll_pass: RollPass):
    return np.sqrt(roll_pass.equivalent_height_change) / (2 * roll_pass.friction_coefficient * np.sqrt(roll_pass.roll.nominal_radius))


@RollPass.hookimpl
def marini_parameter_b(roll_pass: RollPass):
    return np.sqrt(roll_pass.equivalent_height_change / roll_pass.roll.nominal_radius)


@RollPass.OutProfile.hookimpl
def width(roll_pass: RollPass):
    log = logging.getLogger(__name__)

    numerator = 2 * roll_pass.equivalent_height_change * roll_pass.in_profile.equivalent_rectangle.width * (
            roll_pass.roll.nominal_radius - roll_pass.in_profile.equivalent_rectangle.height / 2) * roll_pass.marini_parameter_b

    first_denominator = roll_pass.out_profile.equivalent_rectangle.height * roll_pass.in_profile.equivalent_rectangle.width

    second_denominator = (roll_pass.in_profile.equivalent_rectangle.width * (
            roll_pass.in_profile.equivalent_rectangle.height + roll_pass.out_profile.equivalent_rectangle.height) / 2) * ((
                                  1 + roll_pass.marini_parameter_a) / (1 - roll_pass.marini_parameter_a))

    third_denominator = (0.91 * (roll_pass.in_profile.equivalent_rectangle.width + 3 * roll_pass.in_profile.equivalent_rectangle.height)) / (
            4 * roll_pass.in_profile.equivalent_rectangle.height)

    fourth_denominator = 2 * roll_pass.out_profile.equivalent_rectangle.height * roll_pass.roll.nominal_radius * roll_pass.marini_parameter_b

    out_width = roll_pass.in_profile.equivalent_rectangle.width + (
            numerator / (first_denominator + second_denominator * third_denominator + fourth_denominator))

    log.debug(f"Width after Marini spreading model: {out_width}.")

    return out_width

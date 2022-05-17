from pyroll.core import RollPass


@RollPass.hookspec
def equivalent_height_change(roll_pass):
    """Height change for equivalent rectangle of the roll pass"""


@RollPass.hookspec
def friction_coefficient(roll_pass):
    """Friction coefficient."""


@RollPass.hookspec
def marini_parameter_a(roll_pass):
    """Marini spreading model parameter a."""


@RollPass.hookspec
def marini_parameter_b(roll_pass):
    """Marini spreading model parameter b."""

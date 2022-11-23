from pyroll.core import RollPass
from . import rollpass_hookspecs
from . import rollpass_hookimpls

RollPass.plugin_manager.add_hookspecs(hookspecs)

RollPass.plugin_manager.register(hookimpls)


from pyroll import RollPass
from . import hookspecs
from . import hookimpls

RollPass.plugin_manager.add_hookspecs(hookspecs)

RollPass.plugin_manager.register(hookimpls)
RollPass.OutProfile.plugin_manager.register(hookimpls)

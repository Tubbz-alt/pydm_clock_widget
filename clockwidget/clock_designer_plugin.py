from pydm.widgets.qtplugin_base import qtplugin_factory
from .clock import Clock
from .dynlabel import DynamicSizeLabel

# Clock plugin
LCLSClock = qtplugin_factory(Clock, group="LCLS Display")
LCLSDynamicSizeLabel = qtplugin_factory(DynamicSizeLabel, group="LCLS Display")
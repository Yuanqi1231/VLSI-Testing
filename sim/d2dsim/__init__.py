"""Pure-ngspice D2D interconnect simulation workflow.

Modules:
  params    -- Config dataclass + physical defaults (cited to DEEP_SIM doc)
  prbs      -- LFSR PRBS bit streams
  netlist   -- ngspice netlist generation (link + TDR) with defect injection
  measure   -- run ngspice, extract eye/jitter/BER/skew/TDR features (stdlib)
  campaign  -- fault-injection grid -> labelled telemetry dataset
"""
from .params import Config, DEFECT_KINDS
from .campaign import run_campaign, make_defect, default_defect, build_grid
from .measure import simulate_link, simulate_tdr

__all__ = [
    "Config", "DEFECT_KINDS", "run_campaign", "make_defect", "default_defect",
    "build_grid", "simulate_link", "simulate_tdr",
]

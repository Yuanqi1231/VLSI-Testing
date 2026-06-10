"""Entry point for the v2 waveform campaign (spawn-safe for multiprocessing).

    ~/miniconda3/envs/drl_hw2/bin/python run_wave2.py --n-rows 4000
"""
from d2dsim.wave_campaign_v2 import main

if __name__ == "__main__":
    main()

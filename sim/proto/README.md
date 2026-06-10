# proto/ — verified ngspice-46 prototypes for the active TX/RX upgrade

Reproducible decks backing `../MULTIPHYSICS_DESIGN.md`. Run with the project ngspice:

    ngspice -b active_txrx_min.cir          # minimal alpha-law TX + RC-CTLE + tanh slicer

`active_txrx_min.cir` — minimal behavioural TX/RX in the netlist.py idiom (numerics inlined,
no .param/.func in B-sources, no LAPLACE). Demonstrates: swing rides the PDN node, the tanh
slicer makes decisions, converges (rc=0) with `.ic v(vddtx)=0.8` required (uic + Lpdn).

Key result (see MULTIPHYSICS_DESIGN.md Part D): a stress field splits TX rise/fall edge times
(opposite NMOS/PMOS piezoresistive sign) while temperature scales them together — the
fingerprint that makes the mechanical-stress axis identifiable against the thermal confounder.

#!/bin/bash
cd $HOME/git/Frituur_Receipt_Generator/
python3 generate_receipt_from_arg.py "$(<./example2.json)"

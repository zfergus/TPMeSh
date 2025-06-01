#!/bin/sh
for i in {0..7}; do
    echo "Creating primitive $i"
    python3 -m TPMeSh.mesh_tpms -i $i -r 1 1 1 -o meshes/primitive_$i.ply -n 4 -s
done
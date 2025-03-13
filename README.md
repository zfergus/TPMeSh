# <ins>TPM</ins>e<ins>S</ins>h
Triply Periodic Meshing for Triply Periodic Minimal Surfaces

## Volumetric Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -o "2.msh"
```

![Periodic Meshing](assets/volumetric.gif)

## Surface Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -s -o "2.stl"
```

![Periodic Meshing](assets/surface.gif)

## Periodic Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -p -o "2p.msh"
```

![Periodic Meshing](assets/periodic.png)
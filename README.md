# <ins>TPM</ins>e<ins>S</ins>h

Triply Periodic Meshing for Triply Periodic Minimal Surfaces

## Usage

```
$ python TPMeSh/mesh_tpms.py -h
usage: mesh_tpms.py [-h] [-x X X X X X X X X] [-i I] [-s] [-p] [-o OUTPUT] [-t THICKNESS]
                    [-n ELEMENTS_IN_THICKNESS] [-r REPEATS REPEATS REPEATS] [-v]

Generate a TPMS mesh with given design parameters.

options:
  -h, --help            show this help message and exit
  -x X X X X X X X X    design parameters
  -i I                  Generate a canonical TPMS with the given index
  -s, --surface         generate surface mesh
  -p, --periodic        generate periodic mesh
  -o, --output OUTPUT   output mesh name (.stl for surface mesh, .msh for volume mesh)
  -t, --thickness THICKNESS thickness of the TPMS mesh walls (default: 0.5)
  -n, --elements-in-thickness ELEMENTS_IN_THICKNESS
                        Number of elements in the thickness of the mesh (default: 2)
  -r, --repeats REPEATS REPEATS REPEATS
                        Number of repeats in each direction (default: 4 2 4 for full mesh,
                        1 1 1 for periodic mesh)
  -v, --visualize       visualize the mesh

```

### Primitives

To generate a mesh for a specific TPMS primitive, use the `-i` option with an integer index.

```bash
python -m TPMeSh.mesh_tpms -i <primitive_index>
```

where `<primitive_index>` is an integer from 0 to 7, corresponding to the following TPMS primitives:

<!-- 4x2 Tables of Images for TPMS primitives -->
| (1) Schoen Gyroid | (2) Schwarz Diamond | (3) Schwarz Primitive | (4) Schoen IWP |
| :---: | :---: | :---: | :---: |
| ![Primitive 0](assets/primitives/0.png) | ![Primitive 1](assets/primitives/1.png) | ![Primitive 2](assets/primitives/2.png) | ![Primitive 3](assets/primitives/3.png) |
| **(5) Neovius** | **(6) Fischer Koch S** | **(7) Schoen FRD** | **(8) PMY** |
| ![Primitive 4](assets/primitives/4.png) | ![Primitive 5](assets/primitives/5.png) | ![Primitive 6](assets/primitives/6.png) | ![Primitive 7](assets/primitives/7.png) |

### Volumetric Meshing

```bash
python -m TPMeSh.mesh_tpms -i 2 -r 2 2 2 -o "2.msh"
```

![Periodic Meshing](assets/volumetric.gif)

### Surface Meshing

```bash
python -m TPMeSh.mesh_tpms -i 2 -r 2 2 2 -s -o "2.stl"
```

![Periodic Meshing](assets/surface.gif)

### Periodic Meshing

```bash
python -m TPMeSh.mesh_tpms -i 2 -r 1 1 1 -p -o "2p.msh"
```

![Periodic Meshing](assets/periodic.png)
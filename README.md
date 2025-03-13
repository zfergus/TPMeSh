# <ins>TPM</ins>e<ins>S</ins>h

Triply Periodic Meshing for Triply Periodic Minimal Surfaces

## Primitives

<!-- 4x2 Tables of Images for TPMS primitives -->
| Schoen Gyroid | Schwarz Diamond | Schwarz Primitive | Schoen IWP |
| :---: | :---: | :---: | :---: |
| ![Primitive 0](assets/primitives/0.png) | ![Primitive 1](assets/primitives/1.png) | ![Primitive 2](assets/primitives/2.png) | ![Primitive 3](assets/primitives/3.png) |
| **Neovius** | **Fischer Koch S** | **Schoen FRD** | **PMY** |
| ![Primitive 4](assets/primitives/4.png) | ![Primitive 5](assets/primitives/5.png) | ![Primitive 6](assets/primitives/6.png) | ![Primitive 7](assets/primitives/7.png) |

## Usage

### Volumetric Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -o "2.msh"
```

![Periodic Meshing](assets/volumetric.gif)

### Surface Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -s -o "2.stl"
```

![Periodic Meshing](assets/surface.gif)

### Periodic Meshing

```bash
python TPMeSh/mesh_tpms.py -i 2 -r 1 1 1 -p -o "2p.msh"
```

![Periodic Meshing](assets/periodic.png)
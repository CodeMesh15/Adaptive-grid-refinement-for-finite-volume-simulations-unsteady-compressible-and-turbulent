# Adaptive-grid-refinement-for-finite-volume-simulations-unsteady-compressible-and-turbulent
Hybrid RANS/LES (HRLES): Combines Reynolds-Averaged Navier-Stokes (RANS) for attached flows and Large Eddy Simulation (LES) for separated regions. The goal is to optimize computational grids to resolve turbulent structures efficiently.

Mesh Adaptation Strategies:

h-adaptation: Refines/coarsens mesh elements (isotropic/anisotropic).

Truncation Error Criterion (TECq): Derived from a third-order k-exact finite volume scheme, it uses correction terms (ΔQ₁ and ΔQ₂) to estimate discretization errors.

Time-Averaged Criteria: Reduces solution-mesh delay by averaging TECq over intervals.

Automatic Period Control (APC): Dynamically adjusts adaptation intervals based on error norms.

Validation: Tested on inviscid vortex advection, mixing layers, shock interactions, and a turbulent backward-facing step. Results show improved accuracy and reduced computational cost compared to uniform meshes.
# Adaptive Grid Refinement for HRLES Simulations  
Reproduces the methodology from *"Adaptive Grid Refinement for High-Order Finite Volume Simulations of Unsteady Compressible and Turbulent Flows"*.

## Setup  
1. Install dependencies:  
   - ANSYS Fluent/OpenFOAM v2112 (for open-source workflow)  
   - Python 3.8+ with NumPy, Matplotlib  
2. Clone the repo:  
   ```bash
   git clone https://github.com/yourusername/adaptive-grid-refinement-HRLES.git
   cd adaptive-grid-refinement-HRLES

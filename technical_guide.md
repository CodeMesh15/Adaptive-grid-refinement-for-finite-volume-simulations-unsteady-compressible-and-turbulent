# Technical Guide: Adaptive Grid Refinement for HRLES Simulations  
**Authors**: Ariadni Liapi, Anca Belme, Mikail Salihoglu, Pierre Brenner, et al.  
**Version**: 1.0  
**Date**: December 2024  

---

## Table of Contents  
1. [Methodology](#1-methodology)  
2. [Governing Equations](#2-governing-equations)  
3. [Numerical Scheme](#3-numerical-scheme)  
4. [Error Estimator (TECq)](#4-error-estimator-tecq)  
5. [Grid Adaptation Strategy](#5-grid-adaptation-strategy)  
6. [Validation Cases](#6-validation-cases)  
7. [Implementation Steps](#7-implementation-steps)  
8. [Troubleshooting](#8-troubleshooting)  
9. [References](#9-references)  

---

## 1. Methodology  
This work focuses on **adaptive mesh refinement (AMR)** for hybrid RANS/LES (HRLES) simulations of compressible turbulent flows. Key components include:  

### Hybrid RANS/LES Framework  
- **RANS Regions**: Resolve attached boundary layers using Reynolds-Averaged Navier-Stokes equations with the DDES \(k\)-\(\omega\) SST model.  
- **LES Regions**: Resolve large-scale vortical structures in separated flows via Large Eddy Simulation.  

### Adaptive Grid Refinement  
- **h-Adaptation**: Refines/coarsens cells *isotropically* using octree splitting.  
- **TECq Criterion**: A truncation error estimator derived from the \(k\)-exact finite-volume scheme.  
- **Time-Averaged Adaptation**: Reduces solution-mesh delay by averaging TECq over intervals.  
- **Automatic Period Control (APC)**: Dynamically adjusts adaptation frequency based on error norms.  

---

## 2. Governing Equations  
The compressible RANS/LES equations are solved in integral form:  

\[
\frac{d}{dt} \iint_{\Omega_{CV}} \mathbf{w} \, d\Omega + \oint_{A_{CV}} \mathbf{F} \cdot \mathbf{n} \, dS = 0  
\]  

- **Resolved Variables**: \(\mathbf{w} = (\rho, \rho u, \rho E)^T\) (conservative variables).  
- **Fluxes**: \(\mathbf{F} = \mathbf{F}_E + \mathbf{F}_V\), where:  
  - \(\mathbf{F}_E\): Inviscid flux (Euler equations).  
  - \(\mathbf{F}_V\): Viscous flux (Navier-Stokes).  

---

## 3. Numerical Scheme  
### \(k\)-Exact Finite Volume Method  
- **Reconstruction**: Primitive variables (\(\mathbf{q} = (u, P, T)^T\)) are reconstructed via Taylor series:  
  \[
  \mathbf{q}(\mathbf{x}) = \mathbf{q}_I + \mathbf{D}^{(1)}\mathbf{q}|_I \cdot (\mathbf{x} - \mathbf{x}_I) + \frac{1}{2} \mathbf{D}^{(2)}\mathbf{q}|_I \cdot (\mathbf{x} - \mathbf{x}_I)^{\otimes 2} + \mathcal{O}(h^3)
  \]  
- **Flux Integration**: High-order approximation using surface moments \(\mathcal{S}_{A_{IK}}^{(m)}\):  
  \[
  \iint_{A_{IK}} \mathbf{F} \cdot \mathbf{n} \, dS \approx \mathbf{F}|_\Gamma \cdot \mathcal{S}_{A_{IK}}^{(0)} + \mathbf{D}^{(1)}\mathbf{F}|_\Gamma \cdot \mathcal{S}_{A_{IK}}^{(1)} + \dots
  \]  

### Third-Order Accuracy  
- Achieved by correcting cell-averaged primitive variables using volume moments (\(\mathcal{M}_I^{(m)}\)).  

---

## 4. Error Estimator (TECq)  
The Truncation Error Criterion combines two correction terms:  
\[
\text{TEC}_q = |\Delta Q_1| + |\Delta Q_2|  
\]  
- **First Correction Term**:  
  \[
  \Delta Q_1 = \Delta q = \frac{1}{\beta_I} \mathcal{M}_I^{(2)} : \left( \mathbf{D}^{(1)}\rho|_I \otimes \mathbf{D}^{(1)}\mathbf{u}|_I \right)  
  \]  
- **Second Correction Term**:  
  \[
  \Delta Q_2 = \frac{1}{2} \mathcal{M}_I^{(2)} : \mathbf{D}^{(2)}q|_I  
  \]  
- **Normalization**: TECq is scaled between 0 and 1 using field max/min values.  

---

## 5. Grid Adaptation Strategy  
### Dynamic Mesh Adaptation (DMA)  
1. **Initialization**: Start with a coarse mesh (e.g., \(160 \times 80\) for vortex advection).  
2. **Refinement Marking**: Cells with \(\text{TEC}_q > \theta_{\text{refine}}\) are split.  
3. **Coarsening**: Cells with \(\text{TEC}_q < \theta_{\text{coarsen}}\) are merged.  

### Time-Averaged Adaptation  
- **Averaging Window**: TECq is averaged over \(N\) time steps (e.g., \(N = 40\)).  

### Automatic Period Control (APC)  
- **Adaptation Interval Adjustment**:  
  \[
  \epsilon = \frac{\|\bar{c}_{(n+1)}\|_{L^2} - \|\bar{c}_{(n)}\|_{L^2}}{\|\bar{c}_{(n+1)}\|_{L^2} + \|\bar{c}_{(n)}\|_{L^2}}  
  \]  
  - If \(\epsilon \leq 0\), increase interval: \(I \leftarrow I \times (1 - \epsilon)\).  
  - If \(\epsilon > 0\), decrease interval: \(I \leftarrow I \times (1 - \epsilon)\).  

---

## 6. Validation Cases  
### 6.1 Inviscid Vortex Advection  
- **Setup**: Convected isentropic vortex (\(M_\infty = 0.5\)).  
- **Results**:  
  - 2 refinement levels on coarse mesh reduce cells by 85% vs. uniform refinement.  
  - \(L^\infty\) velocity error: 0.44% (vs. 0.33% for fine mesh).  

### 6.2 Spatially Evolving Mixing Layer  
- **Setup**: Laminar mixing layer (\(Re = 500\), \(Ma_c = 0.6\)).  
- **Results**: APC reduces CPU time by 27% vs. instantaneous adaptation.  

### 6.3 Shock-Mixing Layer Interaction  
- **Setup**: Oblique shock (\(\beta = 12^\circ\)) impinging on shear layer.  
- **Results**: TECq captures shocks and vortices without explicit sensors.  

### 6.4 Backward-Facing Step (DDES)  
- **Setup**: Transonic flow (\(Re = 1.2 \times 10^6\), \(M = 0.7\)).  
- **Results**:  
  - Reattachment length: \(X_{r}/D = 1.12\) (matches experiments).  
  - Resolved 80% of turbulent kinetic energy in LES regions.  

---

## 7. Implementation Steps  
### Software Requirements  
- **CFD Solver**: ANSYS Fluent (UDFs) or OpenFOAM.  
- **Postprocessing**: Python/Paraview.  

### Workflow  
1. **Geometry & Mesh**:  
   ```bash
   # Generate hexahedral mesh with overset grids
   blockMesh -case cases/backward_step

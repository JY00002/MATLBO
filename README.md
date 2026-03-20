# MATLBO Algorithm for Heterogeneous UAV Swarm Cooperative Task Allocation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

> This repository contains the official implementation of the paper: **"Efficient modular adaptive teaching-learning-based optimization for heterogeneous UAV swarm task allocation under temporal constraints"**.
>
> **Note**: Currently, only the data generation code is provided. The full code will be open-sourced upon paper acceptance.

---

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Environment Requirements](#environment-requirements)
- [Usage](#usage)
- [Results](#results)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

---

## 🚀 About the Project
This work addresses the **heterogeneous UAV swarm cooperative task allocation problem** under complex constraints (e.g., task precedence). We propose a **Modular Adaptive Teaching-Learning-Based Optimization (MATLBO)** algorithm to efficiently solve this NP-hard problem.

The codebase currently includes:
- Data generation code for test instances
- (Full code coming soon after paper acceptance)

---

## ✨ Key Features
- 🎯 **Unified and Extensible Test Case Generation**: Generate diverse test instances with configurable UAV and task parameters
- 📊 **Multi-Objective Collaborative Optimization**: Optimize distance, time, and load simultaneously
- 🔗 **Complex Constraints Handling**: Natively supports temporal coupling and skill matching constraints
- 🧠 **MATLBO Algorithm**: Modular and configurable metaheuristic solver with clear structure
- 🎨 **Visualization Tools**: Routing curves and convergence curves

---

## 🛠️ Environment Requirements
- **Python 3.10 or higher**
- Dependencies:
  ```
  dubins==1.0.1
  rlco==0.6.0
  PyYAML==6.0.2
  ```

  ** Note for Windows users**: If you encounter issues installing `dubins==1.0.1`, please refer to [this guide](https://blog.csdn.net/qq_28266955/article/details/80332909) for detailed installation instructions.

---

## 🎮 Usage
### 1. Generate Test Data
```bash
python generate_data.py --config config.json
```

### 2. (Coming Soon) Run MATLBO Algorithm
```bash
    python matlbo.py --use_npz_data --npz_file_path "./n50_m12_seed1002.npz" \
        --population_size 50 --num_classes 3 --max_iterations 500 \
        --objective_type weighted_sum --distance_type dubins \
        --initialization_strategy nnloadbalancing --enable_adaptive_weights \
        --enable_relocate --enable_heading_optimization --enable_2opt --enable_swap --enable_or_opt \
        --enable_shift_task --enable_block_swap --enable_block_relocate --enable_two_opt_star \
        --experiment_name matlbo_c3_ls9 
```

---

## 📊 Results
### Performance Comparison
MATLBO outperforms baseline algorithms on all test instances


## 📝 Citation
If you find this code useful in your research, please cite our paper:

```bibtex
@article{jy2026matlbo,
  title={Efficient modular adaptive teaching-learning-based optimization for heterogeneous UAV swarm task allocation under temporal constraints},
  author={xxx},
  journal={XX},
  year={2026},
  volume={XX},
  pages={XX--XX}
}
```

---

## 🙏 Acknowledgments
We sincerely thank the following open-source projects for their valuable code and inspiration:

- [GA-Implementation](https://github.com/jerryfungi/Multi-UAV_Task_Allocation_SEADmission) - For the baseline Genetic Algorithm implementation
- [AMTLBO-Reference](https://github.com/yuxinyongMath16/CPMCTA-AMTLBO) - For the baseline AMTLBO algorithm implementation reference
- [TestCase-Generator](https://github.com/ai4co/parco) - For the test case generation framework reference

---

⭐ If this project helps you, please give it a star!

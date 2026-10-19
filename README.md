# Deep Learning-Based Quantification of *Plasmodium falciparum* Cytoadhesion

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow / PyTorch](https://img.shields.io/badge/framework-Deep%20Learning-orange.svg)]()

Official repository for the research article: **"Deep Learning Approaches for Automated Quantification of *Plasmodium falciparum* Cytoadhesion under Flow Conditions"**.

Repository link: [https://github.com/Laboratorio-de-Analise-de-Dados/img-PEP.git](https://github.com/Laboratorio-de-Analise-de-Dados/img-PEP.git)

---

## 📌 Overview

Severe malaria caused by *Plasmodium falciparum* is closely linked to cytoadhesion—the adhesion of infected red blood cells (iRBCs) to endothelial receptors under physiological flow conditions. Traditional manual counting methods are labor-intensive, operator-dependent, and prone to variability.

This repository provides an end-to-end computer vision and Convolutional Neural Network (CNN) pipeline designed to automatically quantify cytoadherent parasites in microfluidic assay images.

### Key Features
- **Preprocessing Pipeline**: Contrast enhancement, automated segmentation, and ROI extraction to handle varying illumination and artifacts.
- **Deep Neural Architecture**: Custom/tuned CNN optimized for accurate particle/cell density quantification.
- **Robust Cross-Validation**: Evaluated using 5-fold cross-validation with quantitative metrics ($R^2$, MSE, MAE).

---

## 📊 Performance Metrics

Across 5-fold cross-validation on the experimental dataset, the model demonstrated high precision and consistency:

| Metric | Mean Performance | 95% Confidence Interval |
| :--- | :---: | :---: |
| **Correlation ($R$)** | $0.9017$ | $[0.8387, 0.9647]$ |
| **Mean Squared Error (MSE)** | $735.67$ | — |
| **Statistical Significance ($p$-value)** | $p \le 0.01$ | — |

---

## 📁 Repository Structure

```text
img-PEP/
├── data/
│   ├── raw/                 # Raw microfluidic assay images (or sample placeholders)
│   └── processed/           # Preprocessed and cropped ROI datasets
├── notebooks/
│   ├── 01_preprocessing.ipynb # Image cleaning, filtering, and augmentation
│   ├── 02_model_training.ipynb  # CNN training pipeline and cross-validation
│   └── 03_evaluation.ipynb      # Metrics calculation, regression analysis, and plots
├── src/
│   ├── __init__.py
│   ├── dataset.py           # Data loaders and augmentation logic
│   ├── model.py             # CNN architecture definitions
│   └── utils.py             # Helper functions for evaluation metrics
├── requirements.txt         # Required Python packages
├── LICENSE                  # Open-source license
└── README.md                # Repository documentation
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed. It is recommended to use a virtual environment or Conda environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Laboratorio-de-Analise-de-Dados/img-PEP.git
   cd img-PEP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔬 Usage & Pipeline

### 1. Data Preprocessing
To prepare raw microscopy images for the CNN:
```bash
python src/dataset.py --input_dir data/raw --output_dir data/processed
```

### 2. Model Training & Evaluation
To run 5-fold cross-validation and output metrics:
```bash
python src/model.py --data_dir data/processed --epochs 50 --batch_size 16
```

---

## 📄 Citation

If you find this code or research useful in your work, please cite our manuscript:

```bibtex
@article{ferreira2026deep,
  title={Deep Learning Approaches for Automated Quantification of Plasmodium falciparum Cytoadhesion under Flow Conditions},
  author={Ferreira, [Author Name] and Ferraboli, [Author Name] and [Other Authors]},
  journal={[Journal Name]},
  year={2026},
  volume={[Volume]},
  pages={[Pages]},
  doi={[DOI]}
}
```

---

## ✉️ Contact & Support

**Laboratório de Análise de Dados (LAD)**
- **Repository Maintainer**: [Laboratorio-de-Analise-de-Dados](https://github.com/Laboratorio-de-Analise-de-Dados)
- **Issues**: For bugs, questions, or feature requests, please open a GitHub Issue in this repository.
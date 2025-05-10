
# PDF Certificate Generator and Signer

This Python project generates personalized course certificates as PDF files and digitally signs them using a `.p12` certificate (e.g., FNMT or other PKCS#12-based certificates).

## 📦 Features

- Generate styled certificates using [ReportLab](https://www.reportlab.com/).
- Digitally sign certificates with [pyHanko](https://github.com/MatthiasValvekens/pyHanko).
- Automatically deletes temporary unsigned PDFs after signing.
- Highly customizable logo, names, and course details.

## ⚙️ Requirements

- Python 3.13+
- Dependencies listed below

## 🧪 Installation

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install reportlab pyHanko
```

## 🔐 FNMT Certificate

Make sure you have your `.p12` certificate (e.g., from FNMT) and its password. You can either:

- Set the password in `settings.py`, or
- Export it as an environment variable:

```bash
export FNMT_CERTIFICATE_PASSWORD="your_password"
```

## 🧾 Usage

Run the script using:

```bash
python -m src.main
```

It will:

1. Create a certificate PDF with the provided name and course info.
2. Sign it with the configured `.p12` certificate.
3. Save the signed PDF and delete the temporary unsigned file.

## 🔧 Configuration

Edit `config/settings.py` to customize paths and certificate options.




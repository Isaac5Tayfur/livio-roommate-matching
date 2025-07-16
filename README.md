# 🧩 Livio – Smart Roommate Matching

Livio is an intelligent and multilingual roommate recommendation app that helps users find the most compatible flatmates based on lifestyle traits, habits, and preferences. Built with Streamlit, it leverages machine learning (Cosine Similarity) and real-world profiles to provide accurate, explainable matches.

![Livio Banner](Media/banner.png)

---

## 🚀 Features

- 🎯 **Personalized matching** using Cosine Similarity on normalized traits
- 🌐 **Bilingual UI**: English and Spanish support with dynamic translation
- 📊 **Interactive compatibility charts** with adaptive styling (Dark/Light Dracula Theme)
- 🧬 **Profile comparison table** with translated attributes and values
- 💬 **Explanations** of shared traits with intuitive emojis
- 🧼 **Optional filters**: non-smokers, healthy eaters, pet allergy exclusions
- 📥 **Export tools**: download results as CSV and PNG
- 📱 **Responsive & modern design** with custom CSS and Google Fonts

---

## 🧠 How It Works

1. The app loads 15,000+ diverse tenant profiles from a real-world-inspired dataset.
2. Profiles are one-hot encoded, binary-transformed, and normalized using `MinMaxScaler`.
3. Cosine Similarity is computed between selected seed tenants and the rest.
4. Top matches are displayed visually with insights and profile-level breakdowns.
5. `metadata.xlsx` serves as a reference schema outlining all possible variables and accepted values used in the dataset, ensuring consistency and future scalability.

---

## 📂 Project Structure

```bash
Livio/
├── app.py                  # Main Streamlit app
├── logic.py                # Matching algorithm and dataset preprocessing
├── ui_helpers.py           # Chart, table, and explanation generators
├── tenants_dataset.csv     # Raw tenant profiles
├── metadata.xlsx           # Reference schema of variables and allowed values
├── Media/                  # Visuals (banner)
│   └── banner.png
├── requirements.txt        # Project dependencies
├── .gitignore              # Git exclusions for build artifacts and temp files
└── README.md               # Project overview and usage instructions
```

---

## 🛠️ Tech Stack

- **Python** – Core language
- **Pandas / NumPy / Scikit-learn** – Data processing & normalization
- **Streamlit** – UI framework
- **Seaborn / Matplotlib / Plotly** – Data visualization
- **Plotly Export (Kaleido)** – PNG table/chart rendering
- **Custom CSS + Google Fonts** – Thematic styling

---

## 🧪 Run Locally

> ⚠️ Before running, make sure you have Python ≥ 3.9 and Streamlit properly installed.

### 1. Clone the repo
```bash
git clone https://github.com/Isaac5Tayfur/livio-roommate-matching.git
cd livio-roommate-matching
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the app
```bash
streamlit run app.py
```

---

## 🤖 Future Enhancements

- 🧠 Smart filtering based on user preferences or behavior
- 💾 Database support for persistence and user history
- ✨ User accounts and feedback loop integration
- 🌍 Additional languages (French, German, Italian...)

---

## 👤 Author

**Tayfur Akkaya Clavijo**  
[LinkedIn](https://www.linkedin.com/in/tayfur-akkaya-clavijo) • [GitHub](https://github.com/Isaac5Tayfur) • [Blog](https://tayfur-ac.hashnode.dev)

---

## 📄 License

MIT License. See `LICENSE` for more details.
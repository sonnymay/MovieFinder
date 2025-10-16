# 🎬 MovieFinder

**MovieFinder** is a simple web app that helps users discover new movies based on what they feel like watching.  
It uses the **OpenAI API** to generate tailored movie suggestions with short summaries,  
and the **TMDb API** to display real movie posters and release years.

🔗 **Live Demo:** [https://moviefinder-sonnymay.streamlit.app](https://moviefinder-sonnymay.streamlit.app)

---

## 🧠 Features
- Type what kind of movie you want to watch (e.g., “funny sci-fi adventure”)
- Get **5 personalized recommendations** with titles, years, and posters  
- Click **“Next Suggestions”** to discover new sets of movies  
- Clean, responsive UI built with **Streamlit**
- Integrated with **OpenAI GPT-4o-mini** and **TMDb API**

---

## 🛠️ Tech Stack
- **Language:** Python  
- **Framework:** Streamlit  
- **APIs:** OpenAI API, TMDb API  
- **Environment Management:** python-dotenv  
- **Deployment:** Streamlit Cloud  

---

## 🚀 Run Locally
```bash
git clone https://github.com/sonnymay/MovieFinder.git
cd MovieFinder
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key_here" > .env
echo "TMDB_API_KEY=your_tmdb_key_here" >> .env
streamlit run app.py

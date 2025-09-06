# 💼 AI Co-Pilot for LinkedIn Content Creation
Generate professional LinkedIn posts quickly using OpenAI by providing a topic and a custom prompt.

---

## Features

* Mandatory **Topic** and **Custom Prompt** input
* Adjustable **Tone** (formal → creative)
* Copy posts or download as `.txt`
* Optional **model selection** to manage cost/performance
* Streamlit interface for easy usage
* Preset categories for quick prompt generation: Leadership, Startups, Career Growth, Teamwork, Innovation

---

## Set-up

1. Get an **OpenAI API Key** and add it to your `.env` file as `OPENAI_API_KEY`.
2. Install dependencies:

```commandline
pip install -r requirements.txt
```

3. Run the Streamlit app:

```commandline
streamlit run app.py
```

---

## Usage

1. Enter a **Topic** and **Custom Prompt**.
2. Adjust **Tone** and **Max Tokens** as needed.
3. Click **Generate Post**.
4. Copy or download the generated LinkedIn-ready post.

---

## Advanced Options

* Choose the model for post generation:

  * `gpt-3.5-turbo` (Recommended, low cost)
  * `gpt-3.5-turbo-16k` (For long prompts)
  * `text-davinci-003` (High cost, creative)
* Adjust tone (0 = formal, 1 = creative)
* Max tokens control output length

---

## Architecture Diagram

![Uploading architecture_diagram.png…]()


---

## Author

Made with ❤️ by [Sachin Aditiya B](https://www.linkedin.com/in/sachin-aditiya-b-7691b314b/)

---

## License

MIT License. Commercial use prohibited without prior written permission. Attribution required in all copies or substantial portions of the software.

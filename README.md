# streamlit-ai-chatbot

Adds the [Asyntai](https://asyntai.com) AI chat assistant to a Streamlit app.
The assistant answers visitor questions from your own content, day and night,
in more than 80 languages.

Free and open source. Works on every Asyntai plan, including the free plan.

- Requires Streamlit 1.28 or newer and Python 3.10 or newer
- Documentation: https://asyntai.com/documentation/integrations/streamlit/

## Install

```
pip install streamlit-ai-chatbot
```

## Use

Call `chatbot()` once near the top of your app:

```python
import streamlit as st
from streamlit_ai_chatbot import chatbot

chatbot("asyntai_ab12cd34")

st.title("My app")
```

You get the ID from the Install page of your
[Asyntai dashboard](https://asyntai.com/dashboard). You can paste the whole
snippet; the package keeps only the ID.

The chat button appears in the corner of the page. It stays open when the
app reruns, and it loads only once per browser tab.

## Keep the ID out of your code

Leave out the ID, and the package reads `ASYNTAI_WIDGET_ID` from
`st.secrets` or from the environment:

```toml
# .streamlit/secrets.toml
ASYNTAI_WIDGET_ID = "asyntai_ab12cd34"
```

```python
chatbot()
```

This also works on Streamlit Community Cloud: add the line in the app's
Secrets settings.

## Multipage apps

With `st.navigation`, call `chatbot()` in the main file, before
`pg.run()`. With a `pages/` folder, call it at the top of each page.

## Options

```python
chatbot(
    "asyntai_ab12cd34",
    script_url="https://widget.asyntai.com/static/js/chat-widget.js",  # optional
)
```

`chatbot()` returns `True` when the chat is on the page. With an ID that is
not valid it shows nothing, returns `False` and logs a warning.

## How it works

On Streamlit 1.52 and newer, the package uses `st.html` to add the widget
script to the page. On older versions it uses a hidden component. Either way,
the empty block is hidden, so your layout does not change.

## What the assistant does

- Answers visitor questions from your website, documents and FAQ
- Collects leads and hands the chat to a person when needed
- Works in more than 80 languages

Set it up and train it in your [Asyntai dashboard](https://asyntai.com).

## License

MIT

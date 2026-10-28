"""The small piece of HTML and JavaScript that loads the chat widget."""
import json

#: Class on the hidden marker, so CSS can hide the empty Streamlit block.
MARKER_CLASS = 'asyntai-streamlit-marker'

_LOADER = """
(function () {
    // Inside the iframe of components.html the page is our parent. With
    // st.html the code already runs in the page itself.
    var doc = document;
    try {
        if (window.frameElement && window.parent && window.parent.document) {
            doc = window.parent.document;
            // Hide the empty block that holds this iframe. Streamlit redraws
            // the block and drops inline styles, so we mark the iframe and
            // add one CSS rule to the page instead.
            window.frameElement.setAttribute('data-asyntai-loader', '1');
            if (!doc.getElementById('asyntai-streamlit-style')) {
                var style = doc.createElement('style');
                style.id = 'asyntai-streamlit-style';
                style.textContent =
                    '[data-testid="stElementContainer"]:has(iframe[data-asyntai-loader]),' +
                    '.element-container:has(iframe[data-asyntai-loader])' +
                    '{display:none !important;}';
                doc.head.appendChild(style);
            }
        }
    } catch (error) {
        return;
    }

    var widgetId = __WIDGET_ID__;
    var scriptUrl = __SCRIPT_URL__;
    if (!widgetId || scriptUrl.indexOf('https://') !== 0) { return; }

    // Streamlit runs the app again on every click. The widget lives
    // outside the Streamlit tree, so it stays, and we load it only once.
    if (doc.querySelector('script[data-asyntai-id]')) { return; }

    var script = doc.createElement('script');
    script.src = scriptUrl;
    script.async = true;
    script.setAttribute('data-asyntai-id', widgetId);
    doc.head.appendChild(script);
}());
"""

_STYLE = (
    '<style>'
    '[data-testid="stElementContainer"]:has(.' + MARKER_CLASS + '),'
    '.element-container:has(.' + MARKER_CLASS + ')'
    '{display:none !important;}'
    '</style>'
)


def _js_string(value):
    """A JavaScript string literal that is also safe inside a script tag."""
    return (
        json.dumps(value)
        .replace('<', '\\u003c')
        .replace('>', '\\u003e')
        .replace('&', '\\u0026')
    )


def loader_js(widget_id, script_url):
    """The loader script with both values filled in."""
    return (
        _LOADER
        .replace('__WIDGET_ID__', _js_string(widget_id))
        .replace('__SCRIPT_URL__', _js_string(script_url))
    )


def html_block(widget_id, script_url):
    """The block for st.html: a hidden marker, a style rule and the loader."""
    return (
        _STYLE
        + '<div class="' + MARKER_CLASS + '" style="display:none"></div>'
        + '<script>' + loader_js(widget_id, script_url) + '</script>'
    )


def iframe_document(widget_id, script_url):
    """The document for components.html on older Streamlit versions."""
    return '<script>' + loader_js(widget_id, script_url) + '</script>'

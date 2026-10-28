import re
import shutil
import subprocess

import pytest

from streamlit_ai_chatbot._snippet import (
    MARKER_CLASS,
    html_block,
    iframe_document,
    loader_js,
)

WIDGET_ID = 'asyntai_ab12cd34'
URL = 'https://widget.asyntai.com/static/js/chat-widget.js'


def _scripts(html):
    return re.findall(r'<script>(.*?)</script>', html, re.S)


def test_loader_contains_both_values_as_strings():
    js = loader_js(WIDGET_ID, URL)
    assert '"asyntai_ab12cd34"' in js
    assert '"https://widget.asyntai.com/static/js/chat-widget.js"' in js
    assert '__WIDGET_ID__' not in js and '__SCRIPT_URL__' not in js


def test_values_cannot_close_the_script_tag():
    js = loader_js('</script><b>', 'https://a.com/</script>')
    assert '</script>' not in js
    assert '<' not in js.split('var widgetId')[1].split(';')[0]


def test_html_block_has_marker_style_and_one_script():
    html = html_block(WIDGET_ID, URL)
    assert 'class="' + MARKER_CLASS + '"' in html
    assert ':has(.' + MARKER_CLASS + ')' in html
    assert len(_scripts(html)) == 1


def test_iframe_document_has_one_script():
    assert len(_scripts(iframe_document(WIDGET_ID, URL))) == 1


def test_loader_loads_only_once():
    js = loader_js(WIDGET_ID, URL)
    assert "querySelector('script[data-asyntai-id]')" in js


@pytest.mark.skipif(shutil.which('node') is None, reason='node is not installed')
def test_loader_is_valid_javascript(tmp_path):
    for name, html in [('page', html_block(WIDGET_ID, URL)), ('frame', iframe_document(WIDGET_ID, URL))]:
        path = tmp_path / (name + '.js')
        path.write_text(_scripts(html)[0], encoding='utf-8')
        result = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


@pytest.mark.skipif(shutil.which('node') is None, reason='node is not installed')
def test_loader_adds_the_script_once_in_a_fake_page(tmp_path):
    """Run the loader twice in a tiny fake document, like two reruns."""
    harness = """
    var added = [];
    var doc = {
      querySelector: function (sel) { return added.length ? added[0] : null; },
      createElement: function () { return { attrs: {}, setAttribute: function (k, v) { this.attrs[k] = v; } }; },
      head: { appendChild: function (el) { added.push(el); } }
    };
    var document = doc;
    var window = { frameElement: null };
    for (var i = 0; i < 2; i++) { %s }
    if (added.length !== 1) { throw new Error('added ' + added.length); }
    if (added[0].src !== '%s') { throw new Error('src ' + added[0].src); }
    if (added[0].attrs['data-asyntai-id'] !== '%s') { throw new Error('id'); }
    if (added[0].async !== true) { throw new Error('async'); }
    """ % (loader_js(WIDGET_ID, URL), URL, WIDGET_ID)
    path = tmp_path / 'harness.js'
    path.write_text(harness, encoding='utf-8')
    result = subprocess.run(['node', str(path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

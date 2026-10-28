from streamlit_ai_chatbot._validate import (
    DEFAULT_SCRIPT_URL,
    clean_script_url,
    clean_widget_id,
)


def test_bare_id_is_kept():
    assert clean_widget_id('asyntai_ab12cd34') == 'asyntai_ab12cd34'


def test_spaces_are_trimmed():
    assert clean_widget_id('  asyntai_ab12cd34 \n') == 'asyntai_ab12cd34'


def test_id_is_taken_from_a_pasted_snippet():
    snippet = (
        '<script async src="https://widget.asyntai.com/static/js/chat-widget.js" '
        'data-asyntai-id="asyntai_ab12cd34"></script>'
    )
    assert clean_widget_id(snippet) == 'asyntai_ab12cd34'


def test_single_quoted_snippet():
    assert clean_widget_id("<script data-asyntai-id='asyntai_ab12cd34'>") == 'asyntai_ab12cd34'


def test_bad_ids_are_refused():
    for bad in ['', '   ', 'ab12cd34', 'asyntai_', 'asyntai_ab1', 'asyntai_ab12cd34"><script>',
                'asyntai_ab12-cd34', 'ASYNTAI_ab12cd34', 'asyntai_' + 'a' * 65]:
        assert clean_widget_id(bad) == '', bad


def test_non_strings_are_refused():
    for bad in [None, 123, ['asyntai_ab12cd34'], b'asyntai_ab12cd34']:
        assert clean_widget_id(bad) == ''


def test_script_url_defaults():
    assert clean_script_url(None) == DEFAULT_SCRIPT_URL
    assert clean_script_url('') == DEFAULT_SCRIPT_URL
    assert clean_script_url('   ') == DEFAULT_SCRIPT_URL


def test_https_script_url_is_kept():
    url = 'https://cdn.example.com/chat-widget.js'
    assert clean_script_url(url) == url


def test_bad_script_urls_are_refused():
    for bad in ['http://widget.asyntai.com/x.js', 'javascript:alert(1)', '//widget.asyntai.com/x.js',
                'https://a.com/x.js" onload="x', 'https://a.com/<script>', 'https://a.com/a b.js',
                'https://a.com/x\\y.js', 123]:
        assert clean_script_url(bad) == '', bad

#!/usr/bin/env python3
"""
Post-render fixer for the Google Scholar meta tags.

Quarto writes citation_author as "Richa Singh" and dates as 2026-05-26.
Scholar's documentation asks for "Singh, Richa" and 2026/05/26. Neither can be
reached from the front matter:

  * writing `name: "Singh, Richa"` DOES produce the right meta tag, but Quarto
    then mis-parses the name and the BibTeX block comes out as
    `author = {Richa, Singh}` - wrong, and visible on the page.
  * `issued: "2026/05/26"` is normalised straight back to 2026-05-26.

So the front matter stays natural - correct page, correct BibTeX - and this
script rewrites the two tags in the BUILT HTML afterwards. Wired up through
`project: post-render:` in _quarto.yml, so it runs on every local render and on
every GitHub Actions publish. Added 4 Sep 2026.

It also handles date precision. Quarto expands a bare year to YYYY-01-01 and
there is no way to stop it without losing the date from the visible citation
("n.d.") and from the BibTeX. Pages whose real precision is the year alone
therefore carry a marker tag, x-scholar-date-precision, which this script reads
before deleting: those pages end up with a bare year, as Scholar asks for when
no fuller date is known.
"""
import glob, os, re, sys

# "Balu Ananda Chopade" -> "Chopade, Balu Ananda". The last whitespace-separated
# token is taken as the family name. That is correct for every author on this
# site; add an entry here if one ever has a particle ("van der Waals") or a
# family name written first.
EXCEPTIONS = {}

def to_last_first(name):
    name = name.strip()
    if name in EXCEPTIONS:      return EXCEPTIONS[name]
    if ',' in name:             return name          # already Last, First
    parts = name.split()
    if len(parts) < 2:          return name
    return f"{parts[-1]}, {' '.join(parts[:-1])}"

DATE_TAGS = ('citation_publication_date', 'citation_cover_date', 'citation_online_date')
MARKER    = 'x-scholar-date-precision'

def fix(path):
    html = open(path, encoding='utf-8').read()
    original = html

    year_only = re.search(
        r'<meta name="%s" content="year"\s*/?>' % MARKER, html) is not None

    def author(m):
        return f'<meta name="citation_author" content="{to_last_first(m.group(1))}">'
    html = re.sub(r'<meta name="citation_author" content="([^"]*)"\s*/?>', author, html)

    def date(m):
        tag, value = m.group(1), m.group(2)
        value = value[:4] if year_only else value.replace('-', '/')
        return f'<meta name="{tag}" content="{value}">'
    html = re.sub(r'<meta name="(%s)" content="([^"]*)"\s*/?>' % '|'.join(DATE_TAGS),
                  date, html)

    # citation_fulltext_html_url goes from EVERY paper page (4 Sep 2026).
    # The tag means "the full text, as HTML". There is no HTML full text
    # anywhere on this site: the full text is only ever the PDF, and
    # citation_pdf_url already declares that on the sixteen papers that have
    # one. Quarto emits the tag pointing at the landing page regardless, so
    # Scholar was being sent to an abstract and told it was the full text -
    # on the twelve papers with no PDF that is the only thing it was told.
    # citation_abstract_html_url STAYS on all 28: that one is true, and it is
    # what names the page as the article's landing page.
    html = re.sub(r'\s*<meta name="citation_fulltext_html_url"[^>]*>', '', html)

    # Species binomials are italicised in the abstract, which means the YAML
    # carries markdown asterisks - correct on the page, wrong in a meta tag,
    # where Quarto copies them through literally as *Acinetobacter*. Strip the
    # emphasis markers from citation_abstract only; the visible abstract keeps
    # its italics. Added 4 Sep 2026.
    def _plain(m):
        return '<meta name="citation_abstract" content="%s">' % m.group(1).replace('*', '')
    html = re.sub(r'<meta name="citation_abstract" content="([^"]*)"\s*/?>', _plain, html)

    # Where the journal numbers articles instead of paginating, the article
    # number is NOT a first page. Quarto has only `page:`, so it emits the
    # number as citation_firstpage; citation_article_number is added by hand in
    # the page's own include-in-header. Keep the article number, drop the false
    # page. `page:` stays in the front matter so the BibTeX and the formatted
    # citation still carry the number. Nikhil's call, 4 Sep 2026.
    if 'name="citation_article_number"' in html:
        html = re.sub(r'\s*<meta name="citation_(?:first|last)page"[^>]*>', '', html)

    # Quarto copies `abstract:` into the BibTeX block it renders at the foot of
    # the page, so the abstract appeared TWICE - once where a reader wants it
    # and again inside a code box, where it made up ~80% of the record (2,171 of
    # 2,720 characters on the food-contact paper). Scholar never reads BibTeX;
    # it takes metadata from the citation_* tags and content from the visible
    # text, so nothing is lost by dropping the field. Most publishers' own
    # BibTeX exports omit it for the same reason. Nikhil's call, 4 Sep 2026.
    #
    # Brace-counted, not regex-matched: the field legitimately contains nested
    # braces where Quarto protects proper nouns, e.g. {Indian}.
    def _drop_bibtex_abstract(text):
        start = text.find('\n  abstract = {')
        if start == -1:
            return text
        i = text.index('{', start)
        depth = 0
        for j in range(i, len(text)):
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    end = j + 1
                    # take the trailing comma with it, if there is one
                    if text[end:end+1] == ',': end += 1
                    return text[:start] + text[end:]
        return text
    html = _drop_bibtex_abstract(html)

    # Double-encoded entities in citation_* attributes (4 Sep 2026). Several
    # abstracts contain a bare "<" or ">" in a measurement - "MICs of <3 ug/mL",
    # ">70% dye removal", "(p<0.05)". Pandoc turns those into &gt;/&lt; when it
    # writes the page, and the attribute-escaping pass then escapes the & again,
    # so the tag Scholar reads ends up carrying "&amp;amp;gt;70%". The visible
    # abstract is unaffected - this only ever hits the meta tags. The same
    # fault hits any citation_* value with an "&" in it, e.g. the journal name
    # "Environmental Technology & Innovation", so every citation_* tag is swept. Collapse the
    # surplus &amp; layers back to one correctly-encoded entity. The lookahead
    # means only an "&amp;" that actually prefixes an entity is touched, so an
    # abstract that legitimately discusses "&amp;" is left alone.
    _DOUBLED = re.compile(r'&amp;(?=(?:amp;)*(?:lt|gt|amp|quot|apos|#[0-9]+|#x[0-9A-Fa-f]+);)')

    def _collapse_entities(m):
        value = m.group(2)
        while True:
            once = _DOUBLED.sub('&', value)
            if once == value:
                break
            value = once
        return m.group(1) + value + m.group(3)

    html = re.sub(r'(<meta name="citation_[a-z_]+" content=")([^"]*)(")',
                  _collapse_entities, html)

    # Richa's note (4 Sep 2026, second pass). CSL renders only the FIRST author
    # inverted ("Patil, Samiksha B., and Richa Singh") and separates with commas.
    # She wants every author inverted and semicolon-separated. The citation_author
    # tags rewritten above are already exactly that list, in order, so reuse them
    # rather than re-parsing display names. The author segment of the citeas entry
    # is everything before the four-digit year, which no author name contains.
    people = re.findall(r'<meta name="citation_author" content="([^"]*)"', html)
    if people:
        joined = '; '.join(people)

        def _reauthor(m):
            if len(m.group(2)) > 500:      # not an author segment; leave it alone
                return m.group(0)
            # a name ending in an initial already supplies the sentence period
            stop = '' if joined.endswith('.') else '.'
            return m.group(1) + '\n' + joined + stop + ' ' + m.group(3)

        html = re.sub(
            r'(<div id="[^"]*" class="csl-entry quarto-appendix-citeas"[^>]*>)'
            r'(.*?)'
            r'(\d{4}\.\s)',
            _reauthor, html, count=1, flags=re.S)

    # Richa's note 3 (4 Sep 2026). Quarto's "For attribution, please cite this
    # work as:" line wraps the title in curly quotes and Title-Cases it, so the
    # page showed "Nano-Adsorbents for Microplastic Removal - Cross-Material
    # Insights..." while the heading two inches above showed the real, sentence
    # case published title. Swap in the <h1> markup instead of case-converting:
    # that is by definition the published wording, and it carries the <em> on
    # species names and any <sub> that a rule-based conversion would mangle.
    h1 = re.search(r'<h1 class="title">(.*?)</h1>', html, re.S)
    if h1:
        real = h1.group(1).strip()
        def _retitle(m):
            return m.group(1) + real.rstrip('.') + '.' + m.group(3)
        html = re.sub(
            r'(<div id="[^"]*" class="csl-entry quarto-appendix-citeas"[^>]*>.*?)'
            r'(<span>\u201c.*?\u201d</span>)'
            r'(.*?</div>)',
            _retitle, html, count=1, flags=re.S)

    # the marker is scaffolding, not metadata - it does not ship
    html = re.sub(r'\s*<meta name="%s"[^>]*>' % MARKER, '', html)

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False

out = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', '_site')
targets = glob.glob(os.path.join(out, 'papers', '*.html'))
changed = sum(fix(p) for p in targets)
print(f'[scholar-meta] rewrote citation_author / date tags in {changed} of {len(targets)} paper pages')

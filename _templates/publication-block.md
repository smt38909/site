COPY-PASTE BLOCK FOR A NEW PAPER
================================

Copy everything between the two lines of dashes, paste it into research.qmd
directly under the "HOW TO ADD A PAPER" comment (newest paper at the top),
then fill in the blanks. Delete the abstract line if you don't want one.

------------------------------------------------------------------------------
::: {.pub}
[YEAR]{.pub-year} [Open access]{.badge .badge-oa}

[Exact title as published — do not paraphrase or shorten]{.pub-title}

[**Singh R**, Coauthor A, Coauthor B (YEAR). *Journal Name* VOL(ISSUE): PP–PP. [IF X.X]{.pub-if}]{.pub-cite}

[[PDF](papers/YEAR-slug.pdf){target="_blank" rel="noopener"} [HTML](papers/YEAR-slug.html){target="_blank" rel="noopener"} [https://doi.org/10.XXXX/XXXXX](https://doi.org/10.XXXX/XXXXX){target="_blank" rel="noopener"}]{.pub-links}

[*Abstract.* Two or three sentences.]{.pub-abstract}
:::
------------------------------------------------------------------------------


THE CITATION LINE — settled 31 Aug 2026
---------------------------------------

  Author-date order: authors, then (YEAR), then journal, volume(issue): pages.

  * The TITLE IS NOT REPEATED here. It is already element 2 above, in bold.
    The Publication Page Requirements doc shows the title inside the citation
    line; v2's own worked example does not, and neither does this site. Google
    Scholar reads the meta tags on each paper page, not this line, so nothing is
    lost — see the note at the bottom of this file.
  * The YEAR IS repeated — once in the left column as a scanning aid, once here
    so that selecting the line gives a complete, pasteable citation.
  * All authors, in published order. "et al." only at 8 or more.
    NEVER "et al." in a paper page's front matter — that must list everyone.
  * Impact factor last, in the .pub-if span, if the CV records one.
  * Article-number journals (Materials, AMB Express, Frontiers, Next
    Sustainability): the article number replaces the page range — "9(5): 383".


PICK EXACTLY ONE BADGE — four states
------------------------------------

  Publisher's final PDF, hosted here (open access or otherwise permitted):
      [Open access]{.badge .badge-oa}

  Her own accepted manuscript, hosted here, posted legally after the embargo:
      [Accepted MS]{.badge .badge-am}

  No copy here — the DOI link goes to the publisher. Use this both for papers
  we may not host and for papers we may host but have no file for. The visitor
  cannot tell the difference and does not need to; our side is tracked in
  private/tracking.md:
      [Publisher site]{.badge .badge-pub}

  Under a publisher embargo — a copy WILL be posted here when it lifts. Dashed
  border, not solid, because the state is provisional. DELETE the PDF link:
      [Under embargo]{.badge .badge-embargo}


THINGS THAT BREAK THE PAGE
--------------------------

  * Changing or deleting the ::: pub lines. They are what puts the year and
    badge into the left column. Every block opens with ":::" and closes with ":::".
  * Leaving a blank line out between the paragraphs inside a block. Each of the
    four lines needs an empty line before and after it.
  * Renaming or moving a PDF that is already on the site. Google Scholar has
    indexed that exact address — a renamed file breaks the link permanently.


AND THE PART GOOGLE SCHOLAR CARES ABOUT
---------------------------------------

Adding the entry above only makes the paper VISIBLE. To make Scholar attach
your free PDF to the published citation record, you also need a paper page:
copy _templates/paper-template.qmd into papers/YEAR-slug.qmd and fill it in.


WHY THE VISIBLE CITATION FORMAT DOES NOT AFFECT GOOGLE SCHOLAR
--------------------------------------------------------------

Worth understanding before anyone reformats this list again. Scholar gets its
bibliographic data from two places, and this page is neither:

  1. The citation_* meta tags on each individual paper page (Layer 3), which
     Quarto generates from that page's front matter.
  2. The first page of the PDF itself — title in the largest font, authors
     directly below.

This browse page has exactly one job for Scholar: linking to every PDF with
ordinary HTML links it can follow. Consistency in the citation line is for human
readers. So format it for legibility, not for the crawler.

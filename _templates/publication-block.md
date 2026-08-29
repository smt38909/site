COPY-PASTE BLOCK FOR A NEW PAPER
================================

Copy everything between the two lines of dashes, paste it into research.qmd
directly under the "HOW TO ADD A PAPER" comment (newest paper at the top),
then fill in the blanks. Delete the abstract line if you don't want one.

------------------------------------------------------------------------------
::: {.pub}
[YEAR]{.pub-year} [Open access]{.badge .badge-oa}

[Exact title as published — do not paraphrase or shorten]{.pub-title}

[Singh R., Coauthor A. & Coauthor B. — *Journal Name*, YEAR, vol. XX, pp. XX–XX.]{.pub-cite}

[[PDF](papers/YEAR-slug.pdf) [DOI → published version](https://doi.org/10.XXXX/XXXXX)]{.pub-links}

[*Abstract.* Two or three sentences.]{.pub-abstract}
:::
------------------------------------------------------------------------------


PICK EXACTLY ONE BADGE
----------------------

  Publisher's final PDF, open access or otherwise permitted:
      [Open access]{.badge .badge-oa}

  Your own accepted manuscript, posted legally after the embargo:
      [Accepted MS]{.badge .badge-am}

  No PDF yet — DOI link only, and DELETE the PDF link from the .pub-links line:
      [Embargoed to 03/2027]{.badge .badge-embargo}


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

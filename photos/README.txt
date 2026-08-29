Drop candidate photos in this folder. No code edit needed — index.html tries
these filenames for each candidate, in order, and falls back to an initials
circle when none of them load:

  photos/first-last.jpg  .jpeg  .png  .webp     <- preferred
  photos/first_last.jpg  .jpeg  .png  .webp
  photos/first.jpg       .jpeg  .png  .webp

Preferred filenames:

  photos/soma-srinidhi.jpg
  photos/ashika-agrawal.jpg
  photos/sumit-kasaudhan.jpg
  photos/pranab-kumar.jpg
  photos/rajat-dubey.jpg
  photos/aditya-narayan.jpg
  photos/harsh-modi.jpg        (harsh_modi.jpeg already works)
  photos/maddi-saketh.jpg
  photos/aadvik-nautiyal.jpg
  photos/sahil-gupta.jpg
  photos/gopal-saxena.jpg

Use LOWERCASE filenames. GitHub Pages is case-sensitive, so Maddi_saketh.jpeg
404s online even though it opens fine on a Mac. build.py warns about this.

Recommended: square crop, 400x400 px or larger, under ~200 KB each.
To use a filename that does not match the patterns above, set that candidate's
`photo` field in index.html, e.g. photo: "photos/whatever.jpeg".

# SWF archaeology tools

Three Python parsers written to excavate the 2003 Firstborn site from its binary.
All take a DECOMPRESSED swf (CWS → strip 8-byte header, zlib-inflate, re-prepend header).

- `as2-disassembler.py <file.raw> <out.txt>` — AS2 bytecode → readable pseudo-source
  (constant pools, push/arithmetic expression reconstruction, function names).
- `swf-text-decoder.py <file.raw>` — recovers ALL static text: DefineText glyph indices
  mapped back through DefineFont/DefineFont2 code tables, composed through sprite
  placement matrices. Writes /tmp/swf_texts.json.
- `swf-shape-to-svg.py <file.raw>` — DefineShape edge records → SVG paths
  (fills, curves, sprite hierarchy). Writes /tmp/swfshapes.pkl for assembly.

Decompress first:
    python3 -c "import zlib;d=open('main.swf','rb').read();open('main.raw','wb').write(d[:8]+zlib.decompress(d[8:]))"

---
name: 0401-DrawioChartReconstructor
description: Classify uploaded chart/reference images in the Zotero Chart_Types LaTeX index, create any missing Chart_Types folder and .tex subfile, verify draw.io MCP connectivity, reconstruct the uploaded image as editable diagrams.net/draw.io XML, export the .drawio to .png, .pdf, and .svg, and include the exported PNG in the matching TeX subfile. Use when the user asks where an uploaded image belongs in Chart_Types_README.tex, asks to create the matching chart type files, or asks to recreate an uploaded diagram as editable draw.io output with exported assets.
---

# Chart Types Draw.io Reconstructor

Use this skill for uploaded images that should become entries under:

`/Users/quzinan/Desktop/Zotero/07_Reference/Chart_Types/Chart_Types_README.tex`

The expected deliverables are:

- A chosen chart-type category and subtype.
- A folder and `.tex` subfile if the subtype does not already exist.
- A valid editable `.drawio` file in the subtype folder.
- `.png`, `.pdf`, and `.svg` exports beside the `.drawio`.
- The exported `.png` included in the matching `.tex` subfile with `\includegraphics`.

## Workflow

1. Inspect `Chart_Types_README.tex`.
   - Read the `\section*{...}` groups and existing `\subfile{...}` entries.
   - Classify the uploaded image by visual role, not just by filename.
   - Prefer an existing subtype when it fits.
   - If no subtype fits, create a new folder and `.tex` subfile in the most appropriate category.

2. Create or update the TeX scaffold.
   - Folder pattern: `<category_folder>/<type_name>/<type_name>.tex`.
   - Subfile preamble pattern:

```tex
\documentclass[../../Chart_Types_README.tex]{subfiles}

\begin{document}

\subsection*{中文名 - English Name}
\addcontentsline{toc}{subsection}{中文名 - English Name}

\end{document}
```

   - Add `\subfile{category/type/type}` to `Chart_Types_README.tex` near related types.
   - Keep existing ordering and unrelated content unchanged.

3. Check draw.io MCP connectivity.
   - Call `mcp__drawio.search_shapes` with a small relevant query.
   - If the tool returns shape metadata, continue.
   - If unavailable or failing, still generate a hand-authored `.drawio` XML file with native mxGraph cells and report that MCP-assisted shape lookup was unavailable.

4. Reconstruct the uploaded image as editable draw.io XML.
   - Use native draw.io objects only: rectangles, rounded rectangles, ellipses, lines, connectors, text, basic vector shapes, and draw.io library shapes when exact.
   - Do not embed the uploaded image as a single bitmap.
   - Preserve wording exactly; do not correct spelling.
   - Match canvas aspect ratio, relative positions, sizes, colors, stroke widths, arrows, rounded corners, fonts, and opacity as closely as possible.
   - Estimate unclear details rather than omitting them.
   - Use editable text cells for all visible text.
   - Save as `<descriptive_name>.drawio` inside the subtype folder.

5. Validate and export.
   - Run `scripts/validate_drawio_xml.py <file.drawio>`.
   - Run `scripts/export_drawio.py <file.drawio>` to create `.png`, `.pdf`, and `.svg` beside it.
   - If export fails because no draw.io CLI/App is available, report the exact missing dependency and leave the valid `.drawio` file.
   - If export succeeds, verify all three files exist.

6. Include the exported PNG in the TeX subfile.
   - Do this only after the `.png` export exists.
   - Insert the figure in the subtype `.tex` file before `\end{document}` unless the file already has a clearer placeholder location.
   - Use a relative path from the `.tex` file to the `.png`; when the image is beside the `.tex`, use only the filename.
   - If a prior `示例图:` block or `\includegraphics` for the same asset already exists, update that block rather than duplicating it.
   - Preferred snippet:

```tex
示例图:
\begin{center}
    \includegraphics[width=0.95\textwidth]{<exported-image>.png}
\end{center}
```

   - Keep the generated `.drawio`, `.png`, `.pdf`, and `.svg` files in the same subtype folder as the `.tex` file.

7. Finish with a concise report.
   - State the category/subtype decision.
   - Link the `.tex`, `.drawio`, `.png`, `.pdf`, and `.svg` files.
   - Mention validation/export results and whether the PNG was inserted into TeX.

## Classification Hints

- Data comparison charts: `比较类`.
- Time/evolution charts: `趋势类`.
- Distribution charts: `分布类`.
- Correlation or matrix charts: `关系类`.
- Proportion/composition charts: `构成类`.
- Architecture, workflow, algorithm, infographic, network/system diagrams: `流程_结构类`.
- Tables, balance/metaphor drawings, or special uncategorized references: `其他`.

For system-level panels combining many modules, labels, arrows, sidebars, and delivery flows, prefer:

`流程_结构类/信息图/信息图.tex`

## Scripts

- `scripts/validate_drawio_xml.py`: parses `.drawio` XML and checks for an mxGraph root.
- `scripts/export_drawio.py`: tries common diagrams.net/draw.io CLIs and macOS app paths to export `.png`, `.pdf`, and `.svg`.

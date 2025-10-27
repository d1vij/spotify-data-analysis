import { readFile, writeFile } from "fs/promises";

const bakedPiePath = "baked_pie.py";

async function main() {
    const filepath = process.argv[2];
    if (filepath === undefined) {
        throw new Error("No filepath to jupyternotebook passed");
    }

    const bodyColor = process.argv[3];
    const mainColor = process.argv[4];
    const cellColor = process.argv[5];

    if (bodyColor === undefined || mainColor === undefined || cellColor == undefined) {
        throw new Error("Not all colors passed, pass color hexes as <bodycolor> <main color> <cell color>");
    }

    const ipynbContent = await readFile(filepath, { encoding: "utf8" });
    const ipynbJson = JSON.parse(ipynbContent);
    const convertedIpynb = await convertToHtml(ipynbJson, {
        "body-background-color": bodyColor,
        "main-background-color": mainColor,
        "cell-background-color": cellColor
    });

    const output = template + convertedIpynb + template2;
    await writeFile("converted.html", output);
}

main().catch(console.log);

/////////////////////////////////////////////////////////////////////////////////////////////////////

const EMPTY = '';

function getDataOfCell(ipyCell) {
    let source = EMPTY;
    let cell_type;
    let outputs = [];

    const id = ipyCell.id;
    const language = ipyCell.metadata.vscode?.languageId || "python";

    if (ipyCell.metadata.vscode?.languageId == "html") {
        source = ipyCell.source?.filter(ln => ln.trim() != "%%script false --no-raise-error")?.join('') || EMPTY;
        cell_type = "code";
    } else { // Celltype is code
        cell_type = "code";
        source = ipyCell.source?.join(EMPTY) || EMPTY;

        if (ipyCell.outputs !== undefined && ipyCell.outputs.length > 0) {
            for (let output of ipyCell.outputs) {
                if (output.output_type == "stream") {
                    console.log("* Found Text output");
                    const content = output.text?.join(EMPTY) || EMPTY;
                    outputs.push({ type: "text", content });
                } else if (output.output_type == "display_data") {
                    console.log("* Found image");
                    outputs.push({ type: "image", dataUrl: output.data?.["image/png"] });
                }
            }
        }
    }

    return { source, id, outputs, cell_type, language };
}

function sanitizeHTML(__string) {
    return __string
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

export async function  convertToHtml(json, colors) {
    const bakedPieContent = await readFile(bakedPiePath, { encoding: "utf-8" });
    const parsedCells = [];

    const builtHtmlArray = [`
    <style>
        :root {
            --body-background-color: ${colors["body-background-color"]};
            --main-background-color: ${colors["main-background-color"]};
            --cell-background-color: ${colors["cell-background-color"]};
        }
    </style>
`];

    if (json["cells"] === undefined) throw new Error("No cells found (Cells in ipynb file undefined)");
    if (!(json["cells"].length > 0)) throw new Error("No cells found");

    for (const cell of json["cells"]) {
        const data = getDataOfCell(cell);
        parsedCells.push(data);
    }

    for (const cell of parsedCells) {
        if (cell.cell_type == "code" && cell.language !== "html") {
            if (cell.outputs === undefined) continue;
            const builtOutputsHtmlArray = [];
            for (const output of cell.outputs) {
                if (output.type == "text") {
                    builtOutputsHtmlArray.push(`<div class="output-text">${output.content}</div>`);
                } else if (output.type == "image") {
                    builtOutputsHtmlArray.push(`<img class="output-image" id="${cell.id}" src="data:image/png;base64,${output.dataUrl}">`);
                }
            }
            builtHtmlArray.push(`<div class="cell"><pre class="language-${cell.language}"><code class="language-${cell.language}">${sanitizeHTML(cell.source)}</code></pre><div class="output">${builtOutputsHtmlArray.join(EMPTY)}</div></div>`);
        } else if (cell.language == "html") {
            builtHtmlArray.push(`<div class="cell in-cell-html">${cell.source}</div>`);
        } else if (cell.cell_type == "markdown") {
            throw new Error("Not implemented");
        }
    }

    builtHtmlArray.push(`<div class="cell"><pre class="language-python"><code class="language-python">${sanitizeHTML(bakedPieContent)}</code></pre></div>`);
    return builtHtmlArray.join(EMPTY);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////

const template = `<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title></title>

        <!-- FiraCode Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
            href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=IBM+Plex+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap"
            rel="stylesheet">

        <!-- prism.css -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs/themes/prism.min.css">

        <!-- prism.min.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/prism.min.js"
        integrity="sha512-UOoJElONeUNzQbbKQbjldDf9MwOHqxNz49NNJJ1d90yp+X9edsHyJoAs6O4K19CZGaIdjI5ohK+O2y5lBTW6uQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>

        <!-- prism-python.min.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/components/prism-python.min.js"
        integrity="sha512-3qtI9+9JXi658yli19POddU1RouYtkTEhTHo6X5ilOvMiDfNvo6GIS6k2Ukrsx8MyaKSXeVrnIWeyH8G5EOyIQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>


        <style>
        /* for printing */
        @media print {
            @page {
                size: A4 landscape;
                margin: 3mm 3mm;

            }
        }

        body {
            background-color: var(--body-background-color);
            min-height: 100vh;
            min-width: 100vw;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            overflow-x: hidden;
        }

        main {
            width: 80%;
            min-height: 90%;
            display: flex;
            flex-direction: column;
            justify-content: right;
            gap: 10px;
            border-radius: 15px;
            background-color: var(--main-background-color);
            padding: 15px;
            box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
        }

        /* "cell" may include code & output or html */
        .cell {
            background-color: var(--cell-background-color);
            border-radius: 15px;
            padding: 5px;

            font-family: "Fira Code", monospace;
            font-size: 15px;

            white-space: pre-wrap;
            overflow-wrap: anywhere;

            box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        }

        /* Prism.js specific fix for strings */
        .cell .token.string {
            word-break: break-word;
            overflow-wrap: anywhere;
        }

        /* output cell */
        .output {

        }

        .output .output-image {
            margin: auto;
        }          

        /* images */
        .output-image {
            width: 100%;
            border-radius: 15px;
            border-style: solid;
            border-color: #1e1e1e;
            border-width: 1px;
            margin: 2px;
        }

        /* changing defaults of prism highlighting */
        pre[class*="language-"] {
            border-radius: 15px;
            background-color: #1e1e1e;
            margin-inline: 5px;
        }

        pre[class*="language-"] code[class*="language-"] {
            background-color: inherit;
            text-shadow: none;
            font-family: "Fira Code";
            white-space: pre-wrap;
            color: #cfcfcf;
        }

        pre[class*="language-"] code[class*="language-"] .token.operator {
            background-color: inherit;
        }

        pre[class*="language-"] code[class*="language-"] .token.comment {
            color: #7e8e6f;
        }

        pre[class*="language-"] code[class*="language-"] .token.keyword {
            color: #82a7c9;
        }

        pre[class*="language-"] code[class*="language-"] .token.number {
            color: #b3c6a1;
        }

        pre[class*="language-"] code[class*="language-"] .token.boolean {
            color: #cfcb9c;
        }
        </style>
        <style>
        .text-box {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .text-box p.text {
            margin: 1px;
            align-items: center;
            font-size: 16px;
            font-optical-sizing: auto;
        }

        em {
            border-style: solid;
            width: fit-content;
            padding-inline: 4px;
            border-width: 1px;
            border-radius: 5px;
            background-color: rgba(255, 192, 0, 0.25);
            border-color: #8B8000;
        }

        .text-box.bulleted p.text::before {
            margin: 0;
            content: "*";
            padding-inline-end: 10px;
        }

        .underlined {
            text-decoration: underline;
        }

        .comment {
            color: #7e8e6f;
        }

        .header {
            width: fit-content;
            padding: 5px;
            margin: 0;
        }
        </style>

    </head>

    <body>
        <main>
`
const template2 = `

        </main>
    </body>

</html>
`

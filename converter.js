"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.convertToHtml = convertToHtml;
var promises_1 = require("fs/promises");
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var filepath, bodyColor, mainColor, cellColor, ipynbContent, ipynbJson, convertedIpynb, output;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    filepath = process.argv[2];
                    if (filepath === undefined) {
                        throw new Error("No filepath to jupyternotebook passed");
                    }
                    bodyColor = process.argv[3];
                    mainColor = process.argv[4];
                    cellColor = process.argv[5];
                    if (bodyColor === undefined || mainColor === undefined || cellColor == undefined) {
                        throw new Error("Not all colors passed, pass color hexes as <bodycolor> <main color> <cell color>");
                    }
                    return [4 /*yield*/, (0, promises_1.readFile)(filepath, { encoding: "utf8" })];
                case 1:
                    ipynbContent = _a.sent();
                    return [4 /*yield*/, JSON.parse(ipynbContent)];
                case 2:
                    ipynbJson = _a.sent();
                    convertedIpynb = convertToHtml(ipynbJson, {
                        "body-background-color": bodyColor,
                        "main-background-color": mainColor,
                        "cell-background-color": cellColor
                    });
                    output = template + convertedIpynb + template2;
                    return [4 /*yield*/, (0, promises_1.writeFile)("converted.html", output)];
                case 3:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
main().catch(console.log);
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var knownLanguageIds = ["python", "html", "javascript", "unknown"];
var EMPTY = '';
function getDataOfCell(ipyCell) {
    var _a, _b, _c, _d, _e, _f, _g;
    var source = EMPTY;
    var cell_type;
    var outputs = [];
    var id = ipyCell.id;
    var language = (((_a = ipyCell.metadata.vscode) === null || _a === void 0 ? void 0 : _a.languageId) || "python");
    if (((_b = ipyCell.metadata.vscode) === null || _b === void 0 ? void 0 : _b.languageId) == "html") {
        source = ((_d = (_c = ipyCell.source) === null || _c === void 0 ? void 0 : _c.filter(function (ln) { return ln.trim() != "%%script false --no-raise-error"; })) === null || _d === void 0 ? void 0 : _d.join('')) || EMPTY;
        cell_type = "code";
    }
    else { //Celltype is code
        cell_type = "code";
        // Joining based on empty string cuz the json is already formatted as it should be
        source = ((_e = ipyCell.source) === null || _e === void 0 ? void 0 : _e.join(EMPTY)) || EMPTY;
        if (ipyCell.outputs !== undefined && ipyCell.outputs.length > 0) {
            for (var _i = 0, _h = ipyCell.outputs; _i < _h.length; _i++) {
                var output = _h[_i];
                if (output.output_type == "stream") {
                    console.log("* Found Text output");
                    var content = ((_f = output.text) === null || _f === void 0 ? void 0 : _f.join(EMPTY)) || EMPTY;
                    outputs.push({
                        "type": "text",
                        content: content
                    });
                }
                else if (output.output_type == "display_data") {
                    console.log("* Found image");
                    outputs.push({
                        type: "image",
                        dataUrl: (_g = output.data) === null || _g === void 0 ? void 0 : _g["image/png"] //assuming all images would be pngs
                    });
                }
            }
        }
    }
    return {
        source: source,
        id: id,
        outputs: outputs,
        cell_type: cell_type,
        language: language
    };
}
function sanitizeHTML(__string) {
    return __string
        .replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;");
}
/**
 * Takes in JSON Object of the ipynb file and returns output html string
 * */
function convertToHtml(json, colors) {
    var parsedCells = [];
    var builtHtmlArray = ["\n    <style>\n        :root {\n            --body-background-color: ".concat(colors["body-background-color"], ";\n            --main-background-color: ").concat(colors["main-background-color"], ";\n            --cell-background-color: ").concat(colors["cell-background-color"], ";\n        }\n    </style>\n")];
    if (json["cells"] === undefined)
        throw new Error("No cells found (Cells in ipynb file undefined)");
    if (!(json["cells"].length > 0))
        throw new Error("No cells found");
    // Parsing json cells
    for (var _i = 0, _a = json["cells"]; _i < _a.length; _i++) {
        var cell = _a[_i];
        var data = getDataOfCell(cell);
        parsedCells.push(data);
    }
    // Building the html
    for (var _b = 0, parsedCells_1 = parsedCells; _b < parsedCells_1.length; _b++) {
        var cell = parsedCells_1[_b];
        if (cell.cell_type == "code" && cell.language !== "html") {
            if (cell.outputs === undefined)
                continue;
            var builtOutputsHtmlArray = [];
            for (var _c = 0, _d = cell.outputs; _c < _d.length; _c++) {
                var output = _d[_c];
                if (output.type == "text") {
                    builtOutputsHtmlArray.push("<pre class=\"output-text\">".concat(output.content, "</pre>"));
                }
                else if (output.type == "image") {
                    builtOutputsHtmlArray.push("<img class=\"output-image\" id=\"".concat(cell.id, "\" src=\"data:image/png;base64,").concat(output.dataUrl, "\">"));
                }
            }
            builtHtmlArray.push("<div class=\"cell\"><pre class=\"language-".concat(cell.language, "\"><code class=\"language-").concat(cell.language, "\">").concat(sanitizeHTML(cell.source), "</code></pre><div class=\"output\">").concat(builtOutputsHtmlArray.join(EMPTY), "</div></div>"));
        }
        else if (cell.language == "html") {
            builtHtmlArray.push("<div class=\"cell in-cell-html\">".concat(cell.source, "</div>"));
        }
        else if (cell.cell_type == "markdown") {
            throw new Error("Not implemented");
        }
    }
    return builtHtmlArray.join(EMPTY);
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
var template = "<!DOCTYPE html>\n<html lang=\"en\">\n    <head>\n        <meta charset=\"UTF-8\">\n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n        <title></title>\n\n        <!-- FiraCode Font -->\n        <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n        <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n        <link\n            href=\"https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=IBM+Plex+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap\"\n            rel=\"stylesheet\">\n\n        <!-- prism.css -->\n        <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/prismjs/themes/prism.min.css\">\n\n        <!-- prism.min.js -->\n        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/prism.min.js\"\n        integrity=\"sha512-UOoJElONeUNzQbbKQbjldDf9MwOHqxNz49NNJJ1d90yp+X9edsHyJoAs6O4K19CZGaIdjI5ohK+O2y5lBTW6uQ==\"\n        crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script>\n\n        <!-- prism-python.min.js -->\n        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/components/prism-python.min.js\"\n        integrity=\"sha512-3qtI9+9JXi658yli19POddU1RouYtkTEhTHo6X5ilOvMiDfNvo6GIS6k2Ukrsx8MyaKSXeVrnIWeyH8G5EOyIQ==\"\n        crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script>\n\n\n        <style>\n        /* for printing */\n        @media print {\n            @page {\n                size: A4 landscape;\n                margin: 3mm 3mm;\n\n            }\n        }\n\n        body {\n            background-color: var(--body-background-color);\n            min-height: 100vh;\n            min-width: 100vw;\n            display: flex;\n            justify-content: center;\n            align-items: flex-start;\n            overflow-x: hidden;\n        }\n\n        main {\n            width: 80%;\n            min-height: 90%;\n            display: flex;\n            flex-direction: column;\n            justify-content: right;\n            gap: 10px;\n            border-radius: 15px;\n            background-color: var(--main-background-color);\n            padding: 15px;\n            box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;\n        }\n\n        /* \"cell\" may include code & output or html */\n        .cell {\n            background-color: var(--cell-background-color);\n            border-radius: 15px;\n            padding: 5px;\n\n            font-family: \"Fira Code\", monospace;\n            font-size: 15px;\n\n            white-space: pre-wrap;\n            overflow-wrap: anywhere;\n\n            box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;\n        }\n\n        /* Prism.js specific fix for strings */\n        .cell .token.string {\n            word-break: break-word;\n            overflow-wrap: anywhere;\n        }\n\n        /* output cell */\n        .output {\n\n        }\n\n        .output .output-image {\n            margin: auto;\n        }          \n\n        /* images */\n        .output-image {\n            width: 100%;\n            border-radius: 15px;\n            border-style: solid;\n            border-color: #1e1e1e;\n            border-width: 1px;\n            margin: 2px;\n        }\n\n        /* changing defaults of prism highlighting */\n        pre[class*=\"language-\"] {\n            border-radius: 15px;\n            background-color: #1e1e1e;\n            margin-inline: 5px;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] {\n            background-color: inherit;\n            text-shadow: none;\n            font-family: \"Fira Code\";\n            white-space: pre-wrap;\n            color: #cfcfcf;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] .token.operator {\n            background-color: inherit;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] .token.comment {\n            color: #7e8e6f;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] .token.keyword {\n            color: #82a7c9;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] .token.number {\n            color: #b3c6a1;\n        }\n\n        pre[class*=\"language-\"] code[class*=\"language-\"] .token.boolean {\n            color: #cfcb9c;\n        }\n        </style>\n        <style>\n        .text-box {\n            display: flex;\n            flex-direction: column;\n            gap: 2px;\n        }\n\n        .text-box p.text {\n            margin: 1px;\n            align-items: center;\n            font-size: 16px;\n            font-optical-sizing: auto;\n        }\n\n        em {\n            border-style: solid;\n            width: fit-content;\n            padding-inline: 4px;\n            border-width: 1px;\n            border-radius: 5px;\n            background-color: rgba(255, 192, 0, 0.25);\n            border-color: #8B8000;\n        }\n\n        .text-box.bulleted p.text::before {\n            margin: 0;\n            content: \"*\";\n            padding-inline-end: 10px;\n        }\n\n        .underlined {\n            text-decoration: underline;\n        }\n\n        .comment {\n            color: #7e8e6f;\n        }\n\n        .header {\n            width: fit-content;\n            padding: 5px;\n            margin: 0;\n        }\n        </style>\n\n    </head>\n\n    <body>\n        <main>\n";
var template2 = "\n\n        </main>\n    </body>\n\n</html>\n";

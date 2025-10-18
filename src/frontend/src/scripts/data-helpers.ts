import type { AnalyzedData } from "../../../common.typings.d.ts"
import { ResponseStatus } from "../../../backend/enums.ts";
import { pause, wfapLoader,waitingForDataAnalysisPopup, mainContentDiv } from "./script.ts"


const delay = 100; //ms
let state = 1;
let loading = false;


export async function requestDataAnalysis(): Promise<AnalyzedData | void> {
    console.log("indeez")
    const p = startLoading();
    
    const response = await fetch("/analysis");
    const json = await response.json();
    
    loading = false; //stop loading
    await p;
    
    if(json.status === ResponseStatus.failure){
        alert("Failed to analyze data " + json.err);
        return;
    }
    
    const id = json.id;
    const analysisResponse = await fetch(`/analysis/${id}.json`);
    const analysisJson = await analysisResponse.json();

    return analysisJson as AnalyzedData;
}

function startLoading() {
    waitingForDataAnalysisPopup.classList.remove("hidden");
    loading = true;
    return new Promise(async (resolve) => {
        while (true) {
            await pause(delay);
            const states = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
            wfapLoader.innerText = states[state++];
            console.log(state);
            if (loading === false) { 
                waitingForDataAnalysisPopup.classList.add("hidden");
                resolve(0);
                break;
            }
            if(state >= states.length) state = 0;
        }
    })
}




export function displayData(data: AnalyzedData) {
    for(const content of data){
        if(content.type === "image"){
            const imgElm = document.createElement("img") as HTMLImageElement;
            imgElm.src = "data:svg;base64," +  content.data;
            mainContentDiv.appendChild(imgElm);
        }
    }
}
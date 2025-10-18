import {ResponseStatus} from "../../../backend/enums.ts";
import { displayData, requestDataAnalysis } from "./data-helpers.ts";

const filenamePreview = document.querySelector<HTMLParagraphElement>("p#filename-preview")!;
const fileSelectButton = document.querySelector<HTMLInputElement>("input#zf-input")!;
const uploadFormElement = document.querySelector<HTMLFormElement>("form#upload-form")!;
const processingPopup = document.querySelector<HTMLDivElement>("div#popup")!;
const uploadWindow = document.querySelector<HTMLDivElement>("div#upload-window")!;
const showUploadFormButton = document.querySelector<HTMLButtonElement>("button#show-upload-popup")!;
const cancelUploadFormButton = document.querySelector<HTMLButtonElement>("button#cancel")!;
const noZipFileUploadedPopup = document.querySelector<HTMLDivElement>("div#no-zip-uploaded-popup")!;
export const waitingForDataAnalysisPopup = document.querySelector<HTMLDivElement>("div#waiting-for-analysis-popup")!;
export const wfapLoader = document.querySelector<HTMLParagraphElement>("p#loader")!;
export const mainContentDiv = document.querySelector<HTMLDivElement>("main#main-content")!;

export async function pause(ms:number){
    return new Promise(resolve => {
        setTimeout(resolve,ms);
    })
}

fileSelectButton.addEventListener("change", ()=>{
    
    const file = fileSelectButton.files![0];
    filenamePreview.innerText = file.name;
})

uploadFormElement.addEventListener("submit", async (event)=>{
    event.preventDefault();
    processingPopup.classList.remove("hidden");
    uploadWindow.classList.add("hidden");

    const formData = new FormData();
    formData.append("zipfile", fileSelectButton.files![0]);
    
    const response = await fetch("/upload", {
        method:"POST",
        body:formData
    })
    processingPopup.classList.add("hidden");

    const data = await response.json();
    if(data.status === ResponseStatus.failure){
        alert("Failed!"); //TODO: Make it better
        return;
    }
    noZipFileUploadedPopup.classList.add("hidden");
    document.body.classList.remove("no-scroll");
    const analyzedData = await requestDataAnalysis();
    if(analyzedData == undefined) return; //do nothing since the error has been handled in the requestDataAnalysis function
    displayData(analyzedData);
})

showUploadFormButton.addEventListener("click", ()=>{
    uploadFormElement.reset();
    filenamePreview.innerHTML = "(no file selected)"
    document.body.classList.add("no-scroll");
    uploadWindow.classList.remove("hidden");
    
})
cancelUploadFormButton.addEventListener("click", ()=>{
    uploadWindow.classList.add("hidden");
    document.body.classList.remove("no-scroll")
})
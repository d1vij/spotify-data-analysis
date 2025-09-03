import fs from "fs/promises"

async function main(){
    const buffer = await fs.readFile("mapped-uris-mbid.json");
    const json = JSON.parse(buffer);
    const clean = []

    for(let idx=0; idx < json.length; idx++){
        if(!(typeof json[idx] == "string")){
            
            clean.push(json[idx]);
        }
    }

    fs.writeFile("cleaned-mapped-uris-mbid.json", JSON.stringify(clean));
}


main().catch(console.log);
// simple script to get MusicBrainz id for a given track

import fetch from "node-fetch";
import fs from "fs/promises"

const datapath = "track-uri-name.json"


async function wait(ms){
    return new Promise(resolve => {
        setTimeout(()=>{
            resolve(0);
        },ms)
    })
}

async function queryByMetadata(obj){
    const trackName = obj["master_metadata_track_name"].replace(/"/g, '\\"');
    const albumName = obj["master_metadata_album_album_name"].replace(/"/g, '\\"');
    const artistName = obj["master_metadata_album_artist_name"].replace(/"/g, '\\"');

    const query = `recording:"${trackName}" AND artist:"${artistName}"`
    const encodedQuery = encodeURIComponent(query);
    const url = `https://musicbrainz.org/ws/2/recording?query=${encodedQuery}&fmt=json&limit=1`;
    // console.log(url);
    
    const response = await fetch(url, {
        headers:{
            "User-Agent": "MySpotifyApp/1.0 (d1vijv3rma@gmail.com)"
        }
    });
    const json = await response.json();
    const mbid = json["recordings"]?.[0]?.["id"];
    if(mbid != undefined){
        console.log("Found " + mbid + " for trackname " + trackName);
        obj["mbid"] = mbid;
        return obj;
    }
    
    return undefined;
}



async function main() {
    const buffer = await fs.readFile(datapath);
    const data = JSON.parse(buffer)

    const found = [];
    const seen = [];
    
    for(const obj of data){
        if(!seen.includes(obj["master_metadata_track_name"])){
            seen.push(obj["master_metadata_track_name"]);
            const result = await queryByMetadata(obj);
            if(result != undefined){
                found.push(result)
            }
    
            await wait(10);
        }
    }

    fs.writeFile("mapped-uris-mbid.json", JSON.stringify(found));
    // fuck i coulve just queried the lastfm api with track metadata
    // **since not all mbids are listed on lastfm
}
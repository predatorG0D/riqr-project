import { pathFromServer } from "./fromServer";

export const downloadFile = async (url, fileName) => {
    const link = document.createElement("a");  
    const path = URL.createObjectURL(await (await fetch(pathFromServer(url))).blob())  
    link.setAttribute("href", path);
    link.setAttribute("download", fileName);
    link.click();
}
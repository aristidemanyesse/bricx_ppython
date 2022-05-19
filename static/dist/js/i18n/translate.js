import fs from "fs";

$(function () {


  const getFilesRecursively = (directory) => {
    let files = [];
    const filesInDirectory = fs.readdirSync(directory);
    for (const file of filesInDirectory) {
      const absolute = path.join(directory, file);
      if (fs.statSync(absolute).isDirectory()) {
        getFilesRecursively(absolute);
      } else {
        if (absolute.endsWith('fr.json')) {
          files.push(absolute);
        }
      }
    }
    return files
  };


  alert("bfjdhkh")


})
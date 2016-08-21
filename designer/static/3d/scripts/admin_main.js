"use strict";

var config; // объект, отражающий содержимое конфигурационного файла
var currentState;

// В случае если конфигурационный файл недоступен или не является корректным json'ом,
// то скрипт прекратит работу
loadJSON("customization.json", function (loadedJSON) {
    try {
        config = JSON.parse(loadedJSON);
    } catch (err) {
        console.log("Error: ", err);
        stopScript();
    }

    try {
        loadParameters();
    } catch (err) {
        console.log("Error: ", err);
        stopScript();
    }
}, function () {
    console.log("Error: ", xobj.statusText);
    stopScript();
});

function loadParameters() {
    var tablinks = $("textures");
    var isFirst = true;
    for (var textureType in config["Parameters"]["Texture 1"]["Type"]) {
        var entry = document.createElement("li");
        var entryLink = document.createElement("a");
        entryLink.setAttribute("href", "#");
        entryLink.classList.add("texture-link");
        entryLink.setAttribute("onclick", "changeTextureInfo(event, '" + textureType + "')");
        if (isFirst) {
            entryLink.click();
            isFirst = false;
        }

        entryLink.appendChild(document.createTextNode(config["Parameters"]["Texture 1"]["Type"][textureType]["Text"]));
        entry.appendChild(entryLink);
        tablinks.appendChild(entry);
    }
}

function changeTextureInfo(event, textureType) {
    var tablinks = document.getElementsByClassName("texture-link");
    for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    var image = $("texture_img");
    if (textureType != undefined) {
        image.setAttribute('src', config["Texture folder"] + config["Parameters"]["Texture 1"]["Type"][textureType]["Texture filename"]);
    } else {
        image.removeAttribute('src');
    }
    var nameField = $("texture_name");
    nameField.value = event.currentTarget.childNodes[0].nodeValue;
    event.currentTarget.className += " active";
}

function changeTextureName(event) {
    if (event.keyCode == 13) {
        var tablinks = document.getElementsByClassName("texture-link");
        var i = 0;
        while (!tablinks[i].className.endsWith("active")) {
            i += 1;
        }
        tablinks[i].childNodes[0].nodeValue = $("texture_name").value;
    }
}

function addNewTexture(event) {
    var tablinks = $("textures");
    var entry = document.createElement("li");
    var entryLink = document.createElement("a");
    entryLink.setAttribute("href", "#");
    entryLink.classList.add("texture-link");
    entryLink.classList.add("new_texture");
    entryLink.setAttribute("onclick", "changeTextureInfo(event)");
    entryLink.appendChild(document.createTextNode("Texture"));
    entry.appendChild(entryLink);
    tablinks.appendChild(entry);
    entryLink.click();
    tablinks.scrollTop = tablinks.scrollHeight;
}

function removeTexture(event) {
    var textures = $("textures");
    var tablinks = document.getElementsByClassName("texture-link");
    var i = 0;
    while (!tablinks[i].className.endsWith("active")) {
        i += 1;
    }
    textures.removeChild(tablinks[i].parentNode);

    if (i == tablinks.length && tablinks.length != 0) {
        tablinks[i - 1].click();
    } else if (i < tablinks.length && tablinks.length != 0) {
        tablinks[i].click();
    }
}

function handleFiles(files) {
    var reader = new FileReader();
    var image = reader.readAsBinaryString(files[0]);
}

String.prototype.endsWith = function (suffix) {
    return this.match(suffix + "$") == suffix;
};
"use strict";

function $(id) {
    return document.getElementById(id);
};

function stopScript() {
    throw new Error("Aborting JavaScript execution");
}

function loadJSON(filename, callback, errorCallback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open("GET", filename, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState === 4) {
            if (xobj.status === 200) {
                callback(xobj.responseText);
            } else {
                errorCallback();
            }
        }
    };
    xobj.send(null);
}
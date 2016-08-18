"use strict";

var config; // объект, отражающий содержимое конфигурационного файла
var currentState; // объект, содержащий в себе выбранные пользователем варианты конфигурации
// повторяет структуру config["Defaults"]
// Может быть использовано для последующей пересылки и обработки в нетронутом виде.

// В случае если конфигурационный файл недоступен или не является корректным json'ом,
// то скрипт прекратит работу
loadJSON("customization.json", function (loadedJSON) {
    try {
        config = JSON.parse(loadedJSON);
        currentState = config["Defaults"];
    } catch (err) {
        console.log("Error: ", err);
        stopScript();
    }

    try {
        Constructor.init($("render-canvas"), config); // Создание движка и загрузка дефолтных параметров
        Constructor.run(); // Запуск движка BabylonJS и прогрузка сцены
        loadParameters();
    } catch (err) {
        console.log("Error: ", err);
        stopScript();
    }
}, function () {
    console.log("Error: ", xobj.statusText);
    stopScript();
});

// Динамическое формирование таблицы с заголовками параметров конфигурации
function loadParameters() {
    var tablinks = $("tab-links");

    // Последовательное создание новых вкладок таблицы вида <li><a ...></a></li>
    // В случае если в конфиге установлен параметр "Disabled", то вкладка будет
    // недоступна для взаимодействия(отключена)
    var isFirst = true;
    for (var parameter in config["Parameters"]) {
        var entry = document.createElement("li");
        var entryLink = document.createElement("a");
        entryLink.setAttribute("href", "#");
        entryLink.classList.add("tab-link");

        if (config["Parameters"][parameter]["Disabled"] == "true") {
            entry.onclick = function () {
                return false;
            };
            entry.classList.add("disabled");
        } else {
            entryLink.setAttribute("onclick", "openTab(event, '" + parameter + "')");
            if (isFirst) {
                // Первая вкладка открывается после загрузки
                entryLink.click();
                isFirst = false;
            }
        }

        entryLink.appendChild(document.createTextNode(config["Parameters"][parameter]["Text"]));
        entry.appendChild(entryLink);
        tablinks.appendChild(entry);
    }
}

// Динамическое формирование вариантов конфигурации выбранного параметра
function loadParameterContent(parameter) {
    var tabs = $("parameters");
    var parametersTab = document.createElement("div");
    parametersTab.classList.add("tab-content");
    parametersTab.id = parameter + "-tab";

    var parameterTypes = config["Parameters"][parameter]["Type"];
    for (var type in parameterTypes) {
        if (parameterTypes.hasOwnProperty(type)) {
            var radio = appendRadioButton(parametersTab, parameter, type, "parameter-type", parameterTypes[type]["Text"]);
            radio.setAttribute("onclick", "changeParameterType(this)");
            if (type == currentState[parameter]["Type"]) {
                // Дефолтный параметр конфигурации будет выбран сразу после создания кнопки
                radio.click();
                radio.checked = true;
            }
        }
    }

    tabs.appendChild(parametersTab);
    return parametersTab;
}

// Функция, срабатывающая на клик по радиокнопке с вариантом конфигурации.
// Влечёт за собой изменения на отображаемой модели и в объекте с текущим состоянием конфигурации
// Вся необходимая информация хранится в атрибутах кнопки
function changeParameterType(parameterRadioButton) {
    var parameter = parameterRadioButton.name;
    var type = parameterRadioButton.value;

    Constructor.changeModelObject(parameter, type, currentState[parameter]["Type"]);
    currentState[parameter]["Type"] = type;
}

// Отображение вариантов конфигурации заданного параметра
function openTab(event, parameterName) {
    var i, tabcontent, tablinks;

    // Старое содержимое лишь скрывается
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // В случае если пользователь уже просматривал вкладку, то загрузится её старое содержимое,
    // а иначе будет оно будет создано с нуля
    var contentTab = $(parameterName + "-tab");
    if (typeof contentTab === "undefined" || contentTab === null) {
        contentTab = loadParameterContent(parameterName);
    }

    contentTab.style.display = "block";
    event.currentTarget.className += " active";
}

// Функция, возвращающая радиокнопку с заданными параметрами: имя, значение, класс, текст.
// Прикрепляется к переданному родительскому объекту.
function appendRadioButton(parent, name, value, classAttr, text) {
    var label = document.createElement("label");
    var radio = document.createElement("input");
    radio.type = "radio";
    radio.name = name;
    radio.value = value;

    label.appendChild(radio);
    label.appendChild(document.createTextNode(text));
    label.classList.add(classAttr);
    parent.appendChild(label);
    return radio;
}
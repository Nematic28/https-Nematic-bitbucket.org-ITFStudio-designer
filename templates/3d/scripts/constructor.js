"use strict";

var Constructor = function () {
    var publicMethods = {};

    var config; // объект, отражающий содержимое конфигурационного файла customization.json
    var canvas; // элемент html-документа, отображающий сцену.
    var engine; // ядро трехмерной обработки BABYLON
    var scene;
    var camera;

    /** Сокрытие старого объекта, соотвествующего предыдущему активному варианту конфигурации
    параметра, а также отображение объекта, соотвествующего новому варианту(например, сокрытие
    круглых углов ежедневника и отображение квадратных).
    */
    function changeMesh(parameter, oldParameterType, newParameterType) {
        if (oldParameterType != null) {
            var oldObjectName = config["Parameters"][parameter]["Type"][oldParameterType]["Object name"];
            var oldObjectMesh = scene.getMeshByName(oldObjectName);
            if (oldObjectMesh !== null) {
                oldObjectMesh.isVisible = false;
            }
        }

        var newObjectName = config["Parameters"][parameter]["Type"][newParameterType]["Object name"];
        var newObjectMesh = scene.getMeshByName(newObjectName);
        if (newObjectMesh !== null) {
            newObjectMesh.isVisible = true;
        }
    }

    /** Словарь параметров конфигурации и соотвествующие функции, изменяющие их.*/
    var meshModificators = {
        /** Создание новой текстуры и размещение её в качестве первой на каждом объекте, покрытом
            мульти-текстурным материалом(TerrainMaterial) путем изменения его свойства diffuseTexture1.
            Позиция, на которой будет находится текстура, определяется картой смешивания
            текстур для каждого объекта(карты изменяются при изменении сшивки).
            Первая текстура будет там, где на карте красный цвет.
        */
        "Texture 1": function Texture1(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 1"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var objectsNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by object"];

            for (var objectName in objectsNames) {
                var mesh = scene.getMeshByName(objectName);
                if (mesh.material.diffuseTexture1) {
                    mesh.material.diffuseTexture1.dispose();
                }
                mesh.material.diffuseTexture1 = texture;
            }
        },
        // Вторая текстура - на месте зеленого цвета.
        "Texture 2": function Texture2(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 2"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var objectsNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by object"];

            for (var objectName in objectsNames) {
                var mesh = scene.getMeshByName(objectName);
                if (mesh.material.diffuseTexture2) {
                    mesh.material.diffuseTexture2.dispose();
                }
                mesh.material.diffuseTexture2 = texture;
            }
        },
        // Третья - на месте синего цвета.
        "Texture 3": function Texture3(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 3"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var objectsNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by object"];

            for (var objectName in objectsNames) {
                var mesh = scene.getMeshByName(objectName);
                if (mesh.material.diffuseTexture3) {
                    mesh.material.diffuseTexture3.dispose();
                }
                mesh.material.diffuseTexture3 = texture;
            }
        },
        "Corners": function Corners(oldCornerType, cornerType) {
            changeMesh("Corners", oldCornerType, cornerType);
        },
        "Spiral": function Spiral(oldSpiralType, spiralType) {
            changeMesh("Spiral", oldSpiralType, spiralType);
        },

        /** На каждом объекте, покрытом мульти-текстурным
        * материалом, изменяется карта смешивания текстур. Вариант
        * сшивки представляет из себя отдельную папку с изображениями, т.е.
        * картами смешивания для каждого объета. Соответствие файла изображения
        * карты и объекта представлено в конфиге.
        */
        "Stitch": function Stitch(_, stitchType) {
            var mapFolder = config["Stitch folder"] + config["Parameters"]["Stitch"]["Type"][stitchType]["Folder"];
            var objectNames = config["Parameters"]["Stitch"]["Type"][stitchType]["File by object"];

            for (var objectName in objectNames) {
                var fileName = config["Parameters"]["Stitch"]["Type"][stitchType]["File by object"][objectName];
                var map = new BABYLON.Texture(mapFolder + fileName, scene);

                var mesh = scene.getMeshByName(objectName);
                if (mesh.material.mixTexture) {
                    mesh.material.mixTexture.dispose();
                }

                mesh.material.mixTexture = map;
            }
        },

        /* Прошивка обычно представлена множеством сфер, а не одним объектом(в результате работы экспортера
        * из blender в babylon). В соотвествии с форматом именования(Threads1, Threads2, ....),
        * после фильтрации происходит получение нужных объетов и включение/выключение их видимости.
        */
        "Threads": function Threads(oldThreadsType, threadsType) {
            if (oldThreadsType !== null) {
                var oldThreadsName = config["Parameters"]["Threads"]["Type"][oldThreadsType]["Object name"];
                var oldThreadMeshes = scene.meshes.filter(function (elem) {
                    return elem.name.startsWith(oldThreadsName);
                });
                oldThreadMeshes.forEach(function (v) {
                    return v.isVisible = false;
                });
            }

            var newThreadstName = config["Parameters"]["Threads"]["Type"][threadsType]["Object name"];
            var newThreadMeshes = scene.meshes.filter(function (elem) {
                return elem.name.startsWith(newThreadstName);
            });
            newThreadMeshes.forEach(function (v) {
                return v.isVisible = true;
            });
        },
        "Clasp": function Clasp(oldClaspType, claspType) {
            changeMesh("Clasp", oldCornerType, cornerType);
        },
        "Button": function Button(oldbuttonType, buttonType) {
            changeMesh("Button", oldCornerType, cornerType);
        },
        "ElasticBand": function ElasticBand(oldElasticBandType, elasticBandType) {
            changeMesh("ElasticBand", oldElasticBandType, elasticBandType);
        },
        "Personalization": function Personalization(oldPersonalizationType, personalizationType) {
            changeMesh("Personalization", oldPersonalizationType, personalizationType);
        }
    };

    /* Создание: 1) камеры которая будет вращаться вокруг ежедневника, указание её местоположения,
    * 2) света для всей сцены,
    * 3) мульти-текстурного материала для каждого из объектов, которые будут изменять свой внешний вид
    * в процессе изменения текстур и сшивок.
    * 4) Материала черного цвета для резинки.
    * Получение значений параметров, которые должны быть установлены по умолчанию и вызов
    * методов для изменения внешнего вида ежедневника в соответствии с этими значениями.
    */
    function loadDefaults() {
        camera = camera = new BABYLON.ArcRotateCamera("Camera", 10, 1.2, 50, BABYLON.Vector3.Zero(), scene);
        scene.activeCamera = camera;
        camera.lowerRadiusLimit = 25;
        camera.upperRadiusLimit = 50;

        var light = new BABYLON.HemisphericLight("hemi", new BABYLON.Vector3(0, 1, 0), scene);
        light.groundColor = new BABYLON.Color3(1, 1, 1);

        var rightMainMaterial = new BABYLON.TerrainMaterial("RightMainMaterial", scene);
        var leftMainMaterial = new BABYLON.TerrainMaterial("LeftMainMaterial", scene);
        var roundCornersMaterial = new BABYLON.TerrainMaterial("RoundCornersMaterial", scene);
        var squareCornersMaterial = new BABYLON.TerrainMaterial("SquareCornersMaterial", scene);
        var defaultBinderMaterial = new BABYLON.TerrainMaterial("DefaultBinderMaterial", scene);

        var mesh = scene.getMeshByName("RightMainCover");
        mesh.material = rightMainMaterial;
        mesh = scene.getMeshByName("LeftMainCover");
        mesh.material = leftMainMaterial;
        mesh = scene.getMeshByName("DefaultBinder");
        mesh.material = defaultBinderMaterial;
        mesh = scene.getMeshByName("SquareCornersCover");
        mesh.material = squareCornersMaterial;
        mesh = scene.getMeshByName("RoundCornersCover");
        mesh.material = roundCornersMaterial;

        var material = scene.getMaterialByID("dailybook.BinderMaterial");
        material.diffuseColor = new BABYLON.Color3(0, 0, 0);
        material.specularColor = new BABYLON.Color3(0.3, 0.3, 0.3);

        // !! Необходимо раскомментировать когда будут готовы недостающие элементы модели !!
        // !! Перед конвертированием необходимо в Blender скрыть все элементы, которые могут изменяться

        var defaultTexture1 = config["Defaults"]["Texture 1"]["Type"];
        var defaultTexture2 = config["Defaults"]["Texture 2"]["Type"];
        var defaultTexture3 = config["Defaults"]["Texture 3"]["Type"];
        var defaultCorners = config["Defaults"]["Corners"]["Type"];
        var defaultSpiral = config["Defaults"]["Spiral"]["Type"];
        var defaultStitch = config["Defaults"]["Stitch"]["Type"];
        // var defaultClasp = config["Defaults"]["Clasp"]["Type"];
        // var defaultButton = config["Defaults"]["Button"]["Type"];
        var defaultElasticBand = config["Defaults"]["ElasticBand"]["Type"];
        // var defaultPersonalization = config["Defaults"]["Personalization"]["Type"];

        meshModificators["Corners"](null, defaultCorners);
        meshModificators["Spiral"](null, defaultSpiral);
        meshModificators["Stitch"](null, defaultStitch);
        meshModificators["Texture 1"](null, defaultTexture1);
        meshModificators["Texture 2"](null, defaultTexture2);
        meshModificators["Texture 3"](null, defaultTexture3);
        // meshModificators["Clasp"](null, defaultClasp);
        // meshModificators["Button"](null, defaultButton);
        meshModificators["ElasticBand"](null, defaultElasticBand);
        // meshModificators["Personalization"](null, defaultPersonalization);
    }

    publicMethods.init = function (renderCanvas, jsonConfig) {
        canvas = renderCanvas;
        engine = new BABYLON.Engine(renderCanvas, true);
        config = jsonConfig;
    };

    publicMethods.run = function () {
        BABYLON.SceneLoader.Load(config["Scene folder"], config["Scene filename"], engine, function (newScene) {
            scene = newScene;
            // Метод, который реагирует на событие окончания загрузки сцены
            scene.executeWhenReady(function () {
                loadDefaults();
                // Добавление камеры на холст.
                scene.activeCamera.attachControl(canvas, false);
                // Запуск цикла визуализации сцены.
                engine.runRenderLoop(function () {
                    scene.render();
                });
            });
        });
    };

    publicMethods.changeModelObject = function (parameter, type, oldType) {
        if (config && scene) {
            meshModificators[parameter](oldType, type);
        }
    };

    return publicMethods;
}();
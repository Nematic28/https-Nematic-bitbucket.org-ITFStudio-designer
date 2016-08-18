"use strict";

var Constructor = function () {
    var publicMethods = {};

    var config;
    var canvas;
    var engine;
    var scene;
    var camera;

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

    var meshModificators = {
        "Texture 1": function Texture1(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 1"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var materialNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by material"];

            for (var materialName in materialNames) {
                var material = scene.getMaterialByID(materialName);
                if (material.diffuseTexture1) {
                    material.diffuseTexture1.dispose();
                }
                material.diffuseTexture1 = texture;
            }
        },
        "Texture 2": function Texture2(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 2"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var materialNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by material"];

            for (var materialName in materialNames) {
                var material = scene.getMaterialByID(materialName);
                if (material.diffuseTexture2) {
                    material.diffuseTexture2.dispose();
                }
                material.diffuseTexture2 = texture;
            }
        },
        "Texture 3": function Texture3(_, textureType) {
            var texturePath = config["Texture folder"] + config["Parameters"]["Texture 3"]["Type"][textureType]["Texture filename"];
            var texture = new BABYLON.Texture(texturePath, scene);

            var materialNames = config["Parameters"]["Stitch"]["Type"]["Without stitch"]["File by material"];

            for (var materialName in materialNames) {
                var material = scene.getMaterialByID(materialName);
                if (material.diffuseTexture3) {
                    material.diffuseTexture3.dispose();
                }
                material.diffuseTexture3 = texture;
            }
        },
        "Corners": function Corners(oldCornerType, cornerType) {
            changeMesh("Corners", oldCornerType, cornerType);
        },
        "Spiral": function Spiral(oldSpiralType, spiralType) {
            changeMesh("Spiral", oldSpiralType, spiralType);
        },
        "Stitch": function Stitch(_, stitchType) {
            var mapFolder = config["Stitch folder"] + config["Parameters"]["Stitch"]["Type"][stitchType]["Folder"];
            var filesByMaterials = config["Parameters"]["Stitch"]["Type"][stitchType]["File by material"];

            for (var materialName in filesByMaterials) {
                var file = config["Parameters"]["Stitch"]["Type"][stitchType]["File by material"][materialName];
                var map = new BABYLON.Texture(mapFolder + file, scene);
                var material = scene.getMaterialByID(materialName);

                if (material.mixTexture) {
                    material.mixTexture.dispose();
                }

                material.mixTexture = map;
            }
        },
        "Threads": function Threads(oldThreadsType, threadsType) {
            // Прошивка обычно представлена множеством сфер, а не одним объектом,
            // поэтому для неё отдельный случай
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
            scene.executeWhenReady(function () {
                loadDefaults();
                scene.activeCamera.attachControl(canvas, false);

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
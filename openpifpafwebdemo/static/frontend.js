(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["openpifpafwebdemo"] = factory();
	else
		root["openpifpafwebdemo"] = factory();
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./js/src/frontend.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./js/src/camera.ts":
/*!**************************!*\
  !*** ./js/src/camera.ts ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const defaultCapabilities = { audio: false, video: { width: 640, height: 480 } };
class Camera {
    constructor(ui) {
        this.ui = ui;
        this.video = ui.getElementsByTagName('video')[0];
        this.captureCanvas = ui.getElementsByTagName('canvas')[0];
        this.originalCaptureCanvasSize = [this.captureCanvas.width,
            this.captureCanvas.height];
        this.captureContext = this.captureCanvas.getContext('2d');
        this.buttonNextCamera = ui.getElementsByClassName('nextCamera')[0];
        this.captureCounter = 0;
        this.facingMode = null;
        this.setCamera('user');
        this.buttonNextCamera.onclick = this.nextCamera.bind(this);
    }
    setCamera(facingMode) {
        return __awaiter(this, void 0, void 0, function* () {
            if (facingMode === this.facingMode)
                return;
            this.facingMode = facingMode;
            let capabilities = Object.assign({}, defaultCapabilities, { video: Object.assign({}, defaultCapabilities.video, { facingMode: this.facingMode }) });
            const stream = yield navigator.mediaDevices.getUserMedia(capabilities);
            this.video.srcObject = stream;
        });
    }
    imageData() {
        // update capture canvas size
        const landscape = this.video.clientWidth > this.video.clientHeight;
        const targetSize = landscape ? this.originalCaptureCanvasSize : this.originalCaptureCanvasSize.slice().reverse();
        if (this.captureCanvas.width !== targetSize[0])
            this.captureCanvas.width = targetSize[0];
        if (this.captureCanvas.height !== targetSize[1])
            this.captureCanvas.height = targetSize[1];
        // capture
        this.captureCounter += 1;
        // draw
        this.captureContext.save();
        if (this.facingMode === 'user') {
            this.captureContext.translate(this.captureCanvas.width, 0);
            this.captureContext.scale(-1, 1);
        }
        this.captureContext.drawImage(this.video, 0, 0, this.captureCanvas.width, this.captureCanvas.height);
        this.captureContext.restore();
        return { image_id: this.captureCounter, image: this.captureCanvas.toDataURL() };
    }
    nextCamera() {
        const facingMode = this.facingMode === 'user' ? 'environment' : 'user';
        this.setCamera(facingMode);
    }
}
exports.Camera = Camera;


/***/ }),

/***/ "./js/src/frontend.ts":
/*!****************************!*\
  !*** ./js/src/frontend.ts ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

/* global document */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const camera_1 = __webpack_require__(/*! ./camera */ "./js/src/camera.ts");
const visualization_1 = __webpack_require__(/*! ./visualization */ "./js/src/visualization.ts");
let backend_location = '';
if (document.location.search && document.location.search[0] === '?') {
    backend_location = document.location.search.substr(1);
}
if (!backend_location && document.location.hostname === 'vita-epfl.github.io') {
    backend_location = 'https://vitademo.epfl.ch';
}
const fpsSpan = document.getElementById('fps');
let captureCounter = 0;
let fps = 0.0;
let lastProcessing = null;
const c = new camera_1.Camera(document.getElementById('capture'));
const vis = new visualization_1.Visualization(document.getElementById('visualization'));
function newImage() {
    return __awaiter(this, void 0, void 0, function* () {
        const data = c.imageData();
        const response = yield fetch(backend_location + '/process', {
            method: 'post',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (lastProcessing != null) {
            const duration = Date.now() - lastProcessing;
            fps = 0.5 * fps + 0.5 * (1000.0 / duration);
            fpsSpan.textContent = `${fps.toFixed(1)}`;
        }
        lastProcessing = Date.now();
        const body = yield response.json();
        console.log(body);
        yield vis.draw(data.image, body);
    });
}
exports.newImage = newImage;
function loop_forever() {
    return __awaiter(this, void 0, void 0, function* () {
        while (true) {
            yield newImage();
            yield new Promise(resolve => requestAnimationFrame(() => resolve()));
        }
    });
}
loop_forever();


/***/ }),

/***/ "./js/src/visualization.ts":
/*!*********************************!*\
  !*** ./js/src/visualization.ts ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
const COCO_PERSON_SKELETON = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
    [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
    [2, 4], [3, 5], [4, 6], [5, 7]
];
const COLORS = [
    '#1f77b4',
    '#aec7e8',
    '#ff7f0e',
    '#ffbb78',
    '#2ca02c',
    '#98df8a',
    '#d62728',
    '#ff9896',
    '#9467bd',
    '#c5b0d5',
    '#8c564b',
    '#c49c94',
    '#e377c2',
    '#f7b6d2',
    '#7f7f7f',
    '#c7c7c7',
    '#bcbd22',
    '#dbdb8d',
    '#17becf',
    '#9edae5',
];
class Visualization {
    constructor(ui) {
        this.canvas = ui.getElementsByTagName('canvas')[0];
        this.originalCanvasSize = [this.canvas.width, this.canvas.height];
        this.context = this.canvas.getContext('2d');
        this.lineWidth = 10;
        this.markerSize = 4;
    }
    draw(image, data) {
        const scores = data.map((entry) => entry.score);
        // adjust height of output canvas
        if (data && data.length > 0) {
            const landscape = data[0].width_height[0] > data[0].width_height[1];
            const targetSize = landscape ? this.originalCanvasSize : this.originalCanvasSize.slice().reverse();
            if (this.canvas.width !== targetSize[0])
                this.canvas.width = targetSize[0];
            if (this.canvas.height !== targetSize[1])
                this.canvas.height = targetSize[1];
        }
        // draw on output canvas
        const canvasImage = new Image();
        return new Promise((resolve, reject) => {
            canvasImage.onload = () => {
                this.context.drawImage(canvasImage, 0, 0, this.canvas.width, this.canvas.height);
                data.forEach((entry) => this.drawSkeleton(entry.coordinates, entry.detection_id));
                resolve();
            };
            canvasImage.onerror = () => reject();
            canvasImage.src = image;
        });
    }
    drawSkeletonLines(keypoints) {
        COCO_PERSON_SKELETON.forEach((joint_pair, connection_index) => {
            const [joint1i, joint2i] = joint_pair;
            const joint1xyv = keypoints[joint1i - 1];
            const joint2xyv = keypoints[joint2i - 1];
            const color = COLORS[connection_index % COLORS.length];
            this.context.strokeStyle = color;
            this.context.lineWidth = this.lineWidth;
            if (joint1xyv[2] === 0.0 || joint2xyv[2] === 0.0)
                return;
            this.context.beginPath();
            this.context.moveTo(joint1xyv[0] * this.canvas.width, joint1xyv[1] * this.canvas.height);
            this.context.lineTo(joint2xyv[0] * this.canvas.width, joint2xyv[1] * this.canvas.height);
            this.context.stroke();
        });
    }
    drawSkeleton(keypoints, detection_id) {
        this.drawSkeletonLines(keypoints);
        keypoints.forEach((xyv, joint_id) => {
            if (xyv[2] === 0.0)
                return;
            this.context.beginPath();
            this.context.fillStyle = '#ffffff';
            this.context.arc(xyv[0] * this.canvas.width, xyv[1] * this.canvas.height, this.markerSize, 0, 2 * Math.PI);
            this.context.fill();
        });
    }
    drawFields(image, pifC, pifR, pafC, pafR1, pafR2, threshold) {
        // adjust height of output canvas
        const landscape = pifC.dims[3] > pifC.dims[2];
        const targetSize = landscape ? this.originalCanvasSize : this.originalCanvasSize.slice().reverse();
        if (this.canvas.width !== targetSize[0])
            this.canvas.width = targetSize[0];
        if (this.canvas.height !== targetSize[1])
            this.canvas.height = targetSize[1];
        // draw on output canvas
        const canvasImage = new Image();
        return new Promise((resolve, reject) => {
            canvasImage.onload = () => {
                this.context.drawImage(canvasImage, 0, 0, this.canvas.width, this.canvas.height);
                const xScale = this.canvas.width / (pifC.dims[3] - 1);
                const yScale = this.canvas.height / (pifC.dims[2] - 1);
                let pafCounter = 0;
                for (let ii = 0; ii < pafC.dims[2]; ++ii) {
                    for (let jj = 0; jj < pafC.dims[3]; ++jj) {
                        for (let kk = 0; kk < pafC.dims[1]; ++kk) {
                            const v = pafC.get(0, kk, ii, jj);
                            if (v < threshold)
                                continue;
                            pafCounter += 1;
                            const fx1 = jj + pafR1.get(0, kk, 0, ii, jj);
                            const fy1 = ii + pafR1.get(0, kk, 1, ii, jj);
                            const fx2 = jj + pafR2.get(0, kk, 0, ii, jj);
                            const fy2 = ii + pafR2.get(0, kk, 1, ii, jj);
                            this.context.beginPath();
                            this.context.lineWidth = this.lineWidth;
                            this.context.strokeStyle = COLORS[kk];
                            this.context.moveTo(fx1 * xScale, fy1 * yScale);
                            this.context.lineTo(fx2 * xScale, fy2 * yScale);
                            this.context.stroke();
                        }
                    }
                }
                let pifCounter = 0;
                for (let ii = 0; ii < pifC.dims[2]; ++ii) {
                    for (let jj = 0; jj < pifC.dims[3]; ++jj) {
                        for (let ll = 0; ll < pifC.dims[1]; ++ll) {
                            const v = pifC.get(0, ll, ii, jj);
                            if (v < threshold)
                                continue;
                            pifCounter += 1;
                            this.context.beginPath();
                            this.context.fillStyle = '#fff';
                            const fx = jj + pifR.get(0, ll, 0, ii, jj);
                            const fy = ii + pifR.get(0, ll, 1, ii, jj);
                            this.context.arc(fx * xScale, fy * yScale, (v - threshold) / threshold * this.markerSize, 0, 2 * Math.PI);
                            this.context.fill();
                        }
                    }
                }
                console.log({ pifCounter, pafCounter });
                resolve();
            };
            canvasImage.onerror = () => reject();
            canvasImage.src = image;
        });
    }
}
exports.Visualization = Visualization;


/***/ })

/******/ });
});
//# sourceMappingURL=frontend.js.map
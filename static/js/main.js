
var scene, camera, renderer;

var WIDTH  = window.innerWidth;
var HEIGHT = window.innerHeight;

var SPEED = 0.01;

function init() {
    scene = new THREE.Scene();

    initMesh();
    initCamera();
    initLights();
    initRenderer();

    document.body.appendChild(renderer.domElement);
}

function initCamera() {
    camera = new THREE.PerspectiveCamera(70, WIDTH / HEIGHT, 1, 10);
    camera.position.set(0, 0, 8);
    //camera.lookAt(scene.position);
}


function initRenderer() {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha:true });
    renderer.setSize(WIDTH, HEIGHT);
    renderer.setClearColor( 0x000000, 0 );
}

function initLights() {
    var light = new THREE.PointLight();
    light.position.set(0, -3, 0);
    scene.add(light);
    var light2 = new THREE.PointLight();
    light2.position.set(0, -3, 0);
    scene.add(light2);
    var light3 = new THREE.PointLight();
    light3.position.set(5, 2, 2);
    scene.add(light3);
    var light4 = new THREE.PointLight();
    light4.position.set(-5, 2, 2);
    scene.add(light4);
    var light5 = new THREE.AmbientLight();
    light5.position.set(0, 10, 0);
    light5.intensity = 3
    scene.add(light5);

}

var mesh = null;
function initMesh() {
    var loader = new THREE.GLTFLoader();

    loader.load( '/static/models/chipbag.glb', function ( gltf ) {

        scene.add( gltf.scene.getObjectByName('Cube') );

        mesh = scene.getObjectByName('Cube')
        oldmaterial = mesh.material

        var newmaterial = new THREE.MeshStandardMaterial()
        newmaterial.map = oldmaterial.map
        newmaterial.metalness = 0.5
        newmaterial.roughness = oldmaterial.roughness.map
        mesh.material = newmaterial



    }, undefined, function ( error ) {

        console.error( error );

    } );
}

function rotateMesh() {
    if (!mesh) {
        return;
    }

   // mesh.rotation.x -= SPEED * 2;
    mesh.rotation.y -= SPEED;
   // mesh.rotation.z -= SPEED * 3;
}

function render() {
    requestAnimationFrame(render);
    rotateMesh();
    renderer.render(scene, camera);
}

init();
render();

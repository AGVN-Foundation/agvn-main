export default function main() {
    const canvas = document.querySelector('#c');
    const renderer = new THREE.WebGLRenderer({ canvas });

    // applies for both vertical and horizontal FOV
    const fov = 80;
    // responsiveness -> twice as wide as height
    const aspect = 2;  // the canvas default
    // plane of the camera
    const near = 0.1;
    // perspective cut off point
    const far = 10;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    // position camera at (0,0,2)
    camera.position.z = 5;

    const scene = new THREE.Scene();

    const boxWidth = 1;
    const boxHeight = 1;
    const boxDepth = 1;
    const geometry = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);

    const color = 0xFFFFFF;
    const intensity = 1;
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(-1, 2, 4);
    scene.add(light);

    // mesh basic -> not affected by light. Mesh phong -> affected
    function makeInstance(geometry, color, x) {
        const material = new THREE.MeshPhongMaterial({ color });

        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        cube.position.x = x;

        return cube;
    }

    const cubes = [
        makeInstance(geometry, 0x44aa88, 0),
        makeInstance(geometry, 0x8844aa, -2),
        makeInstance(geometry, 0xaa8844, 2),
    ];

    // renderer.render(scene, camera);
    function render(time) {
        // dt = time*0.001
        time *= 0.001;  // convert time to seconds

        cubes.forEach((cube, ndx) => {
            const speed = 1 + ndx * .1;
            const rot = time * speed;
            cube.rotation.x = rot;
            cube.rotation.y = rot;
        });

        // re-render
        renderer.render(scene, camera);

        // request the next frame when done -> pass new time in
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
}

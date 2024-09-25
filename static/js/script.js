// Setup scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Function to generate random stars in a 3D space
function createStarField() {
  const starGeometry = new THREE.BufferGeometry();
  const starMaterial = new THREE.PointsMaterial({ color: 0xffffff });

  const starVertices = [];
  for (let i = 0; i < 10000; i++) {
    const x = (Math.random() - 0.5) * 2000;
    const y = (Math.random() - 0.5) * 2000;
    const z = (Math.random() - 0.5) * 2000;
    starVertices.push(x, y, z);
  }

  starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));

  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);
}

// Create stars and add them to the scene
createStarField();

// Move the camera slightly back so we can see the stars
camera.position.z = 500;

// Animation loop to create a "flying through stars" effect
function animate() {
  requestAnimationFrame(animate);

  // Rotate the scene for effect
  scene.rotation.x += 0.0005;
  scene.rotation.y += 0.001;

  renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', function () {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

// Start animation
animate();

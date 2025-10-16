window.onload = function popImage() {
  setTimeout(() => {
    const images = document.getElementsByTagName('img');
    for (let img of images) {
      img.style.display = 'none';
    }
  }, 5000); // optional delay (e.g., 1 second)
};

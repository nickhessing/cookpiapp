function addListeners() {
  console.log('adding listeners');
  const body = document.querySelector("body"),
        sidebar = body.querySelector("#nav"),
        toggle = body.querySelector(".toggle"),
        searchBtn = body.querySelector(".search-box"),
        modeSwitch = body.querySelector(".toggle-switch"),
        modeText = document.querySelector(".mode-text");

  if (!sidebar) {
    console.error("Unable to find sidebar element");
    return;
  }

  // Swipe handling for mobile devices
  let touchStartX = 0, touchEndX = 0;
  let swipeableArea = body;
  let delta = 0;

  swipeableArea.addEventListener('touchstart', function(event) {
    const screenWidth = window.innerWidth;
    const touchX = event.touches[0].clientX;
    touchStartX = touchX < screenWidth * 0.2 ? touchX : 0;
  });

  swipeableArea.addEventListener('touchmove', function(event) {
    touchEndX = event.touches[0].clientX;
    delta = touchEndX - touchStartX;

    if (sidebar && delta < -80 && !sidebar.classList.contains('close')) {
      sidebar.classList.add('close');
      document.getElementById("page-content").classList.add('close');
    } else if (sidebar && delta > 80 && sidebar.classList.contains('close')) {
      sidebar.classList.remove('close');
      document.getElementById("page-content").classList.remove('close');
    }
  });

  swipeableArea.addEventListener('touchend', function(event) {
    touchEndX = event.changedTouches[0].clientX;
    delta = touchEndX - touchStartX;

    if (sidebar && delta < -80 && !sidebar.classList.contains('close')) {
      sidebar.classList.add('close');
      document.getElementById("page-content").classList.add('close');
    } else if (sidebar && delta > 80 && sidebar.classList.contains('close')) {
      sidebar.classList.remove('close');
      document.getElementById("page-content").classList.remove('close');
    }
  });

  // Click handling for desktop devices
  if (toggle) {
    toggle.addEventListener("click", function() {
      sidebar.classList.toggle("close");
      document.getElementById("page-content").classList.toggle("close");
    });
  }

  // Click handling to close sidebar when clicking outside of it
  document.addEventListener("click", function(event) {
    if (sidebar && !sidebar.contains(event.target) && event.target !== toggle) {
      sidebar.classList.add("close");
      document.getElementById("page-content").classList.add("close");
    }
  });
}

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {addListeners()}, 1000);
});
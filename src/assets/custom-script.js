function addListeners() {
  console.log('adding listeners')
  const body = document.querySelector("body"),
  sidebar = body.querySelector("#nav"),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

  toggle.addEventListener("click", function() {
      sidebar.classList.toggle("close");
      document.getElementById("page-content").classList.toggle("close");
  });

  searchBtn.addEventListener("click", function() {
      sidebar.classList.remove("close");
      document.getElementById("page-content").classList.remove("close");
  });

  modeSwitch.addEventListener("click", function() {
      body.classList.toggle("dark");
      if (body.classList.contains("dark")) {
          modeText.innerText = "Dark mode";
      } else {
          modeText.innerText = "Light mode";
      }
  });
}

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {addListeners()}, 1000)
})

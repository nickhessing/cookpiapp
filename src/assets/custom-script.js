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
    if (touchStartX > 0) {
      touchEndX = event.touches[0].clientX;
      delta = touchEndX - touchStartX;

      if (sidebar && delta < -80 && !sidebar.classList.contains('close')) {
        sidebar.classList.add('close');
        document.getElementById("page-content").classList.add('close');
      } else if (sidebar && delta > 80 && sidebar.classList.contains('close')) {
        sidebar.classList.remove('close');
        document.getElementById("page-content").classList.remove('close');
      }
    }
  });

  swipeableArea.addEventListener('touchend', function(event) {
    if (touchStartX > 0) {
      touchEndX = event.changedTouches[0].clientX;
      delta = touchEndX - touchStartX;

      if (sidebar && delta < -80 && !sidebar.classList.contains('close')) {
        sidebar.classList.add('close');
        document.getElementById("page-content").classList.add('close');
      } else if (sidebar && delta > 80 && sidebar.classList.contains('close')) {
        sidebar.classList.remove('close');
        document.getElementById("page-content").classList.remove('close');
      }

      touchStartX = 0;
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


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Get a reference to the component with id='dropdowncontrol'
const dropdownControl = document.getElementById('dropdowncontrol');

// Get a reference to the modal with id='modalfilter'
const modalFilter = document.getElementById('modalfilter');

// Variables to track touch start and end positions
let startX, endX;

// Listen for touch start event on the document
document.addEventListener('touchstart', function(event) {
  // Record the x position of the touch start
  startX = event.touches[0].pageX;
});

// Listen for touch end event on the document
document.addEventListener('touchend', function(event) {
  // Record the x position of the touch end
  endX = event.changedTouches[0].pageX;

  // Calculate the distance between the start and end positions
  const distance = endX - startX;

  // If the distance is greater than or equal to 50 (pixels), open the modalFilter element
  if (distance >= 50) {
    modalFilter.classList.add('show');
    modalFilter.style.display = 'block';
    modalFilter.setAttribute('aria-modal', true);
    modalFilter.removeAttribute('aria-hidden');
    document.body.classList.add('modal-open');
  }
});

// Listen for clicks on the dropdownControl element to close the modal
dropdownControl.addEventListener('click', function() {
  modalFilter.classList.remove('show');
  modalFilter.style.display = 'none';
  modalFilter.removeAttribute('aria-modal');
  modalFilter.setAttribute('aria-hidden', true);
  document.body.classList.remove('modal-open');
});
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// Get the select-value element
var selectValueElement = document.querySelector('.Select-value');

// Attach a click event listener to the select-value element
selectValueElement.addEventListener('click', function() {

  // Get the currently selected value(s) from the dropdown
  var currentValue = document.querySelector('#Level0NameSelect').value;

  // If there is a selected value, remove it and update the dropdown
  if (currentValue) {
    // If the selected value is an array, remove the last element
    if (Array.isArray(currentValue)) {
      currentValue.pop();
    } 
    // If the selected value is a string, remove it completely
    else {
      currentValue = null;
    }
    // Update the dropdown with the new selected value
    Plotly.d3.select('#Level0NameSelect').property('value', currentValue);
  }

});
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


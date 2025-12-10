// Shared JavaScript across all pages
console.log('Dark Reel Cinema loaded');

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
let selectedSeats = [];

function toggleSeatSelection(button) {
  const seatCode = button.getAttribute("data-seat");

  if (button.classList.contains("bg-available")) {
    button.classList.remove("bg-available");
    button.classList.add("bg-selected");
    selectedSeats.push(seatCode);
  } else if (button.classList.contains("bg-selected")) {
    button.classList.remove("bg-selected");
    button.classList.add("bg-available");
    selectedSeats = selectedSeats.filter(seat => seat !== seatCode);
  }

  document.getElementById("selected_seats").value = selectedSeats.join(",");
}

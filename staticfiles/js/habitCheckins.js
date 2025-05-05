document.addEventListener("DOMContentLoaded", () => {
    console.log("💡 habitCheckins.js loaded");
  
    const checkboxes = document.querySelectorAll(".habit-check");
  
    checkboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", async (event) => {
        const card = event.target.closest(".habit-card");
        const habitId = card.dataset.habitId;
  
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
        try {
          const response = await fetch(`/habits/${habitId}/toggle-checkin/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({}),
          });
  
          if (!response.ok) {
            throw new Error("Network response was not OK");
          }
  
          const data = await response.json();
          card.classList.toggle("checked-in", data.checked_in);
          console.log(`Habit ${habitId} checked in: ${data.checked_in}`);
        } catch (error) {
          console.error("Error toggling habit check-in:", error);
        }
      });
    });
  });
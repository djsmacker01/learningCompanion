
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
    if (window.LearningCompanion && window.LearningCompanion.updateDashboardStats) {
      window.LearningCompanion.updateDashboardStats();
    }
    
    setInterval(() => {
      if (window.LearningCompanion && window.LearningCompanion.updateDashboardStats) {
        window.LearningCompanion.updateDashboardStats();
      }
    }, 30000);
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function () {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML =
          '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = `${this.scrollHeight}px`;
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const textareas = document.querySelectorAll("textarea[maxlength]");
  textareas.forEach((textarea) => {
    const maxLength = parseInt(textarea.getAttribute("maxlength"));
    const counter = document.createElement("small");
    counter.className = "text-muted character-counter";
    counter.style.display = "block";
    counter.style.marginTop = "0.25rem";

    textarea.parentNode.appendChild(counter);

    function updateCounter() {
      const currentLength = textarea.value.length;
      const remaining = maxLength - currentLength;
      counter.textContent = `${currentLength}/${maxLength} characters`;

      if (remaining < 50) {
        counter.className = "text-danger character-counter";
      } else {
        counter.className = "text-muted character-counter";
      }
    }

    textarea.addEventListener("input", updateCounter);
    updateCounter();
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll("[data-confirm]");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const message = this.getAttribute("data-confirm");
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll("form[data-autosave]");
  forms.forEach((form) => {
    const formId = form.getAttribute("data-autosave");
    const inputs = form.querySelectorAll("input, textarea, select");

    const savedData = localStorage.getItem(`form_${formId}`);
    if (savedData) {
      const data = JSON.parse(savedData);
      inputs.forEach((input) => {
        if (data[input.name]) {
          input.value = data[input.name];
        }
      });
    }

    inputs.forEach((input) => {
      input.addEventListener("input", function () {
        const formData = {};
        inputs.forEach((input) => {
          if (input.name) {
            formData[input.name] = input.value;
          }
        });
        localStorage.setItem(`form_${formId}`, JSON.stringify(formData));
      });
    });

    form.addEventListener("submit", function () {
      localStorage.removeItem(`form_${formId}`);
    });
  });
});

window.LearningCompanion = {
  showToast: function (message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText =
      "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
    toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

    document.body.appendChild(toast);

    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(toast);
      bsAlert.close();
    }, 5000);
  },

  formatDate: function (date) {
    return new Date(date).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  },

  formatTime: function (minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  },

  debounce: function (func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  updateDashboardStats: function() {
    fetch('/api/dashboard-stats')
      .then(response => response.json())
      .then(data => {
        const topicCountElement = document.querySelector('.dashboard-container .col-md-3:nth-child(1) h3');
        if (topicCountElement) {
          topicCountElement.textContent = data.topic_count;
        }

        const sessionCountElement = document.querySelector('.dashboard-container .col-md-3:nth-child(2) h3');
        if (sessionCountElement) {
          sessionCountElement.textContent = data.session_count;
        }

        const timeElement = document.querySelector('.dashboard-container .col-md-3:nth-child(3) h3');
        if (timeElement) {
          timeElement.textContent = data.total_time_hours + 'h';
        }

        const streakElement = document.querySelector('.dashboard-container .col-md-3:nth-child(4) h3');
        if (streakElement) {
          streakElement.textContent = data.study_streak;
        }
      })
      .catch(error => {
        console.log('Error updating dashboard stats:', error);
      });
  },
};

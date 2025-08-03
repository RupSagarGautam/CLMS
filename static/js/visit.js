// Visit Pages JavaScript Functions

// Global variables for delete confirmation
let currentDeleteId = null;
let currentDeleteUrl = null;

// Auto-hide flash message after 3 seconds
document.addEventListener('DOMContentLoaded', function() {
  const flashMessage = document.getElementById('flashMessage');
  if (flashMessage) {
    setTimeout(function() {
      flashMessage.classList.add('fade-out');
      setTimeout(function() {
        flashMessage.style.display = 'none';
      }, 500);
    }, 3000);
  }
});

// Show custom delete confirmation modal
function showDeleteConfirmation(visitId, visitName, deleteUrl) {
  currentDeleteId = visitId;
  currentDeleteUrl = deleteUrl;
  document.getElementById('visitName').textContent = visitName;
  document.getElementById('deleteModal').classList.add('show');
}

// Hide delete confirmation modal
function hideDeleteConfirmation() {
  document.getElementById('deleteModal').classList.remove('show');
  currentDeleteId = null;
  currentDeleteUrl = null;
}

// Confirm delete action
function confirmDelete() {
  if (currentDeleteId && currentDeleteUrl) {
    // Create and submit the form
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = currentDeleteUrl;
    
    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);
    
    document.body.appendChild(form);
    form.submit();
  }
  hideDeleteConfirmation();
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
  const deleteModal = document.getElementById('deleteModal');
  if (deleteModal) {
    deleteModal.addEventListener('click', function(e) {
      if (e.target === this) {
        hideDeleteConfirmation();
      }
    });
  }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    hideDeleteConfirmation();
  }
});

// Helper functions for different visit types
function showOfficeVisitDeleteConfirmation(visitId, visitName) {
  showDeleteConfirmation(visitId, visitName, `/add-dashboard/delete/office/${visitId}/`);
}

function showClientVisitDeleteConfirmation(visitId, visitName) {
  showDeleteConfirmation(visitId, visitName, `/add-dashboard/delete/client/${visitId}/`);
}

function showCollegeVisitDeleteConfirmation(visitId, visitName) {
  showDeleteConfirmation(visitId, visitName, `/add-dashboard/delete/college/${visitId}/`);
}

function showOnlineClassDeleteConfirmation(visitId, visitName) {
  showDeleteConfirmation(visitId, visitName, `/add-dashboard/delete/online/${visitId}/`);
} 
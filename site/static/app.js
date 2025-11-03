// Main application JavaScript for index page
(function() {
  'use strict';

  const BOOKMARKS_KEY = 'ml-notes-bookmarks';
  let allQuestions = [];
  let currentFilter = 'all';
  let bookmarks = new Set();

  // Load bookmarks from localStorage
  function loadBookmarks() {
    const stored = localStorage.getItem(BOOKMARKS_KEY);
    if (stored) {
      try {
        bookmarks = new Set(JSON.parse(stored));
      } catch (e) {
        bookmarks = new Set();
      }
    }
    updateBookmarkCount();
  }

  // Save bookmarks to localStorage
  function saveBookmarks() {
    localStorage.setItem(BOOKMARKS_KEY, JSON.stringify([...bookmarks]));
    updateBookmarkCount();
  }

  // Update bookmark count in header
  function updateBookmarkCount() {
    const countEl = document.querySelector('.bookmark-count');
    if (countEl) {
      countEl.textContent = bookmarks.size;
    }
  }

  // Toggle bookmark
  function toggleBookmark(slug, event) {
    if (event) {
      event.stopPropagation();
    }
    
    if (bookmarks.has(slug)) {
      bookmarks.delete(slug);
    } else {
      bookmarks.add(slug);
    }
    saveBookmarks();
    renderQuestions();
  }

  // Render questions
  function renderQuestions() {
    const container = document.getElementById('questionsContainer');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    // Filter questions
    let filtered = allQuestions.filter(q => {
      // Text search
      if (searchTerm && !q.text.toLowerCase().includes(searchTerm) && !q.title.toLowerCase().includes(searchTerm)) {
        return false;
      }
      
      // Unit filter
      if (currentFilter === 'bookmarked') {
        return bookmarks.has(q.slug);
      } else if (currentFilter !== 'all' && q.unit !== currentFilter) {
        return false;
      }
      
      return true;
    });

    if (filtered.length === 0) {
      container.innerHTML = '<div class="empty-state">No questions found. Try adjusting your filters or search.</div>';
      return;
    }

    // Group by unit and marks
    const grouped = {};
    filtered.forEach(q => {
      if (!grouped[q.unit]) {
        grouped[q.unit] = {};
      }
      if (!grouped[q.unit][q.marks]) {
        grouped[q.unit][q.marks] = [];
      }
      grouped[q.unit][q.marks].push(q);
    });

    // Render
    let html = '';
    const unitOrder = ['Unit 1', 'Unit 2', 'Unit 3', 'Unit 4'];
    
    unitOrder.forEach(unit => {
      if (!grouped[unit]) return;
      
      html += `<div class="unit-section">`;
      html += `<div class="unit-header">${unit}</div>`;
      
      // Sort marks: 4-marks first, then 8-marks
      const marksOrder = ['4-marks', '8-marks'];
      marksOrder.forEach(marks => {
        if (!grouped[unit][marks]) return;
        
        const marksLabel = marks === '4-marks' ? '4 Marks Questions' : '8 Marks Questions';
        html += `<div class="marks-group">`;
        html += `<div class="marks-label">${marksLabel}</div>`;
        
        grouped[unit][marks].forEach(q => {
          const isBookmarked = bookmarks.has(q.slug);
          const bookmarkClass = isBookmarked ? 'bookmarked' : '';
          const bookmarkIcon = isBookmarked ? '⭐' : '☆';
          
          html += `
            <div class="question-card ${bookmarkClass}" onclick="navigateToQuestion('${q.slug}')">
              <div class="question-text">${q.text}</div>
              <button class="bookmark-btn ${bookmarkClass}" 
                      onclick="event.stopPropagation(); window.toggleBookmark('${q.slug}', event)"
                      title="${isBookmarked ? 'Remove bookmark' : 'Bookmark this question'}">
                ${bookmarkIcon}
              </button>
            </div>
          `;
        });
        
        html += `</div>`;
      });
      
      html += `</div>`;
    });

    container.innerHTML = html;
  }

  // Render bookmarks panel
  function renderBookmarksPanel() {
    const panel = document.getElementById('bookmarksPanel');
    const list = document.getElementById('bookmarksList');
    
    if (bookmarks.size === 0) {
      list.innerHTML = '<p class="empty-state">No bookmarks yet. Click the star icon on any question to bookmark it!</p>';
      return;
    }

    const bookmarkedQuestions = allQuestions.filter(q => bookmarks.has(q.slug));
    
    let html = '';
    bookmarkedQuestions.forEach(q => {
      html += `
        <div class="question-card bookmarked" onclick="navigateToQuestion('${q.slug}')">
          <div class="question-text">${q.text} <small style="color: var(--muted);">(${q.unit})</small></div>
          <button class="bookmark-btn bookmarked" 
                  onclick="event.stopPropagation(); window.toggleBookmark('${q.slug}', event)"
                  title="Remove bookmark">
            ⭐
          </button>
        </div>
      `;
    });
    
    list.innerHTML = html;
  }

  // Navigate to question
  window.navigateToQuestion = function(slug) {
    window.location.href = slug;
  };

  // Toggle bookmarks panel
  function toggleBookmarksPanel() {
    const panel = document.getElementById('bookmarksPanel');
    panel.classList.toggle('hidden');
    if (!panel.classList.contains('hidden')) {
      renderBookmarksPanel();
    }
  }

  // Load questions from JSON
  async function loadQuestions() {
    try {
      const response = await fetch('questions.json');
      allQuestions = await response.json();
      renderQuestions();
    } catch (error) {
      console.error('Error loading questions:', error);
      document.getElementById('questionsContainer').innerHTML = 
        '<div class="empty-state">Error loading questions. Please refresh the page.</div>';
    }
  }

  // Setup event listeners
  function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', renderQuestions);

    // Filter tabs
    document.querySelectorAll('.filter-tab').forEach(tab => {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        currentFilter = this.dataset.filter;
        
        if (currentFilter === 'bookmarked') {
          // Show bookmarks panel
          document.getElementById('bookmarksPanel').classList.remove('hidden');
          renderBookmarksPanel();
        } else {
          // Hide bookmarks panel
          document.getElementById('bookmarksPanel').classList.add('hidden');
        }
        
        renderQuestions();
      });
    });

    // Bookmarks toggle button
    const bookmarksToggle = document.getElementById('bookmarksToggle');
    if (bookmarksToggle) {
      bookmarksToggle.addEventListener('click', toggleBookmarksPanel);
    }
  }

  // Make toggleBookmark available globally
  window.toggleBookmark = toggleBookmark;

  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    loadBookmarks();
    loadQuestions();
    setupEventListeners();
  });
})();

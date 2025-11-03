// JavaScript for individual question pages
(function() {
  'use strict';

  const BOOKMARKS_KEY = 'ml-notes-bookmarks';
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
  }

  // Save bookmarks to localStorage
  function saveBookmarks() {
    localStorage.setItem(BOOKMARKS_KEY, JSON.stringify([...bookmarks]));
  }

  // Get current page slug
  function getCurrentSlug() {
    const path = window.location.pathname;
    const filename = path.split('/').pop();
    return filename;
  }

  // Toggle bookmark for current page
  function toggleBookmark() {
    const slug = getCurrentSlug();
    const btn = document.getElementById('bookmarkBtn');
    const icon = btn.querySelector('.bookmark-icon');
    
    if (bookmarks.has(slug)) {
      bookmarks.delete(slug);
      btn.classList.remove('bookmarked');
      icon.textContent = '☆';
      btn.title = 'Bookmark this question';
    } else {
      bookmarks.add(slug);
      btn.classList.add('bookmarked');
      icon.textContent = '⭐';
      btn.title = 'Remove bookmark';
      
      // Visual feedback
      btn.style.transform = 'scale(1.3)';
      setTimeout(() => {
        btn.style.transform = 'scale(1)';
      }, 200);
    }
    
    saveBookmarks();
  }

  // Update bookmark button state
  function updateBookmarkButton() {
    const slug = getCurrentSlug();
    const btn = document.getElementById('bookmarkBtn');
    const icon = btn.querySelector('.bookmark-icon');
    
    if (bookmarks.has(slug)) {
      btn.classList.add('bookmarked');
      icon.textContent = '⭐';
      btn.title = 'Remove bookmark';
    } else {
      btn.classList.remove('bookmarked');
      icon.textContent = '☆';
      btn.title = 'Bookmark this question';
    }
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    loadBookmarks();
    updateBookmarkButton();

    // Setup bookmark button click
    const bookmarkBtn = document.getElementById('bookmarkBtn');
    if (bookmarkBtn) {
      bookmarkBtn.addEventListener('click', toggleBookmark);
    }
  });
})();

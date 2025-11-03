// Bookmark Management System
class BookmarkManager {
  constructor() {
    this.storageKey = 'mlNotesBookmarks';
    this.bookmarks = this.loadBookmarks();
    this.init();
  }

  init() {
    this.updateBookmarkCount();
    this.renderBookmarkList();
    this.setupEventListeners();
    this.highlightBookmarkedQuestions();
    this.highlightCurrentPage();
  }

  loadBookmarks() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.error('Error loading bookmarks:', e);
      return [];
    }
  }

  saveBookmarks() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.bookmarks));
      this.updateBookmarkCount();
      this.renderBookmarkList();
    } catch (e) {
      console.error('Error saving bookmarks:', e);
    }
  }

  addBookmark(slug, title) {
    if (!this.isBookmarked(slug)) {
      this.bookmarks.push({ slug, title, timestamp: Date.now() });
      this.saveBookmarks();
      return true;
    }
    return false;
  }

  removeBookmark(slug) {
    this.bookmarks = this.bookmarks.filter(b => b.slug !== slug);
    this.saveBookmarks();
  }

  isBookmarked(slug) {
    return this.bookmarks.some(b => b.slug === slug);
  }

  updateBookmarkCount() {
    const countElement = document.getElementById('bookmarkCount');
    if (countElement) {
      countElement.textContent = this.bookmarks.length;
    }
  }

  renderBookmarkList() {
    const listElement = document.getElementById('bookmarkList');
    if (!listElement) return;

    if (this.bookmarks.length === 0) {
      listElement.innerHTML = '<p class="empty-bookmarks">No bookmarks yet. Click the bookmark icon on any question to save it.</p>';
      return;
    }

    // Sort by most recent first
    const sortedBookmarks = [...this.bookmarks].sort((a, b) => b.timestamp - a.timestamp);

    listElement.innerHTML = sortedBookmarks.map(bookmark => `
      <div class="bookmark-item" data-slug="${bookmark.slug}">
        <a href="${bookmark.slug}">${bookmark.title}</a>
        <button class="remove-bookmark" data-slug="${bookmark.slug}" title="Remove bookmark">
          <i class="fas fa-times"></i>
        </button>
      </div>
    `).join('');

    // Add event listeners to remove buttons
    listElement.querySelectorAll('.remove-bookmark').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const slug = btn.getAttribute('data-slug');
        this.removeBookmark(slug);
        this.highlightBookmarkedQuestions();
      });
    });
  }

  setupEventListeners() {
    // Toggle bookmark panel
    const toggleBtn = document.getElementById('bookmarkToggle');
    const panel = document.getElementById('bookmarkPanel');
    const closeBtn = document.getElementById('closePanel');

    if (toggleBtn && panel) {
      toggleBtn.addEventListener('click', () => {
        panel.classList.toggle('active');
      });
    }

    if (closeBtn && panel) {
      closeBtn.addEventListener('click', () => {
        panel.classList.remove('active');
      });
    }

    // Close panel when clicking outside
    if (panel) {
      document.addEventListener('click', (e) => {
        if (!panel.contains(e.target) && !toggleBtn.contains(e.target) && panel.classList.contains('active')) {
          panel.classList.remove('active');
        }
      });
    }

    // Bookmark buttons in question cards
    document.querySelectorAll('.bookmark-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const slug = btn.getAttribute('data-slug');
        const title = btn.getAttribute('data-title');
        
        if (this.isBookmarked(slug)) {
          this.removeBookmark(slug);
          btn.classList.remove('bookmarked');
          btn.innerHTML = '<i class="far fa-bookmark"></i>';
        } else {
          this.addBookmark(slug, title);
          btn.classList.add('bookmarked');
          btn.innerHTML = '<i class="fas fa-bookmark"></i>';
        }
      });
    });

    // Floating bookmark button on question pages
    const pageBookmarkBtn = document.getElementById('pageBookmarkBtn');
    if (pageBookmarkBtn) {
      pageBookmarkBtn.addEventListener('click', () => {
        const slug = pageBookmarkBtn.getAttribute('data-slug');
        const title = pageBookmarkBtn.getAttribute('data-title');
        
        if (this.isBookmarked(slug)) {
          this.removeBookmark(slug);
          pageBookmarkBtn.classList.remove('bookmarked');
          pageBookmarkBtn.innerHTML = '<i class="far fa-bookmark"></i>';
        } else {
          this.addBookmark(slug, title);
          pageBookmarkBtn.classList.add('bookmarked');
          pageBookmarkBtn.innerHTML = '<i class="fas fa-bookmark"></i>';
        }
      });
    }
  }

  highlightBookmarkedQuestions() {
    document.querySelectorAll('.bookmark-btn').forEach(btn => {
      const slug = btn.getAttribute('data-slug');
      if (this.isBookmarked(slug)) {
        btn.classList.add('bookmarked');
        btn.innerHTML = '<i class="fas fa-bookmark"></i>';
      } else {
        btn.classList.remove('bookmarked');
        btn.innerHTML = '<i class="far fa-bookmark"></i>';
      }
    });
  }

  highlightCurrentPage() {
    const pageBookmarkBtn = document.getElementById('pageBookmarkBtn');
    if (pageBookmarkBtn) {
      const slug = pageBookmarkBtn.getAttribute('data-slug');
      if (this.isBookmarked(slug)) {
        pageBookmarkBtn.classList.add('bookmarked');
        pageBookmarkBtn.innerHTML = '<i class="fas fa-bookmark"></i>';
      }
    }
  }
}

// Search and Filter System
class QuestionFilter {
  constructor() {
    this.searchInput = document.getElementById('searchInput');
    this.filterTabs = document.querySelectorAll('.filter-tab');
    this.questionCards = document.querySelectorAll('.question-card');
    this.init();
  }

  init() {
    if (this.searchInput) {
      this.searchInput.addEventListener('input', () => this.filterQuestions());
    }

    this.filterTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        this.filterTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.filterQuestions();
      });
    });
  }

  filterQuestions() {
    const searchTerm = this.searchInput ? this.searchInput.value.toLowerCase() : '';
    const activeFilter = document.querySelector('.filter-tab.active');
    const filterValue = activeFilter ? activeFilter.getAttribute('data-filter') : 'all';

    this.questionCards.forEach(card => {
      const title = card.querySelector('.question-title').textContent.toLowerCase();
      const unit = card.getAttribute('data-unit');
      
      const matchesSearch = title.includes(searchTerm);
      const matchesFilter = filterValue === 'all' || unit === filterValue;

      if (matchesSearch && matchesFilter) {
        card.style.display = 'flex';
        // Add animation
        card.style.animation = 'fadeIn 0.3s ease';
      } else {
        card.style.display = 'none';
      }
    });
  }
}

// Text-to-Speech System
class TextToSpeech {
  constructor() {
    this.synth = window.speechSynthesis;
    this.utterance = null;
    this.isPaused = false;
    this.isPlaying = false;
    this.init();
  }

  init() {
    const ttsBtn = document.getElementById('ttsBtn');
    if (!ttsBtn) return;

    // Check if browser supports speech synthesis
    if (!this.synth) {
      ttsBtn.style.display = 'none';
      console.warn('Text-to-speech not supported in this browser');
      return;
    }

    ttsBtn.addEventListener('click', () => this.toggleSpeech());
  }

  getTextContent() {
    const answerContent = document.getElementById('answerContent');
    if (!answerContent) return '';

    // Extract text from the answer content, excluding code blocks
    let text = '';
    const walker = document.createTreeWalker(
      answerContent,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          // Skip code blocks and script tags
          const parent = node.parentElement;
          if (parent.tagName === 'CODE' || parent.tagName === 'SCRIPT' || 
              parent.tagName === 'STYLE' || parent.closest('pre')) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while (node = walker.nextNode()) {
      const textContent = node.textContent.trim();
      if (textContent) {
        text += textContent + ' ';
      }
    }

    return text.trim();
  }

  toggleSpeech() {
    const ttsBtn = document.getElementById('ttsBtn');
    
    if (this.isPlaying && !this.isPaused) {
      // Pause speech
      this.synth.pause();
      this.isPaused = true;
      ttsBtn.innerHTML = '<i class="fas fa-play"></i> <span>Resume</span>';
      ttsBtn.classList.add('paused');
    } else if (this.isPaused) {
      // Resume speech
      this.synth.resume();
      this.isPaused = false;
      ttsBtn.innerHTML = '<i class="fas fa-pause"></i> <span>Pause</span>';
      ttsBtn.classList.remove('paused');
    } else {
      // Start new speech
      this.startSpeech();
    }
  }

  startSpeech() {
    const ttsBtn = document.getElementById('ttsBtn');
    const text = this.getTextContent();

    if (!text) {
      alert('No text content found to read');
      return;
    }

    // Cancel any ongoing speech
    this.synth.cancel();

    // Create new utterance
    this.utterance = new SpeechSynthesisUtterance(text);
    
    // Configure utterance
    this.utterance.rate = 1.0; // Normal speed
    this.utterance.pitch = 1.0; // Normal pitch
    this.utterance.volume = 1.0; // Full volume

    // Set up event listeners
    this.utterance.onstart = () => {
      this.isPlaying = true;
      this.isPaused = false;
      ttsBtn.innerHTML = '<i class="fas fa-pause"></i> <span>Pause</span>';
      ttsBtn.classList.add('playing');
    };

    this.utterance.onend = () => {
      this.isPlaying = false;
      this.isPaused = false;
      ttsBtn.innerHTML = '<i class="fas fa-volume-up"></i> <span>Read Aloud</span>';
      ttsBtn.classList.remove('playing', 'paused');
    };

    this.utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      this.isPlaying = false;
      this.isPaused = false;
      ttsBtn.innerHTML = '<i class="fas fa-volume-up"></i> <span>Read Aloud</span>';
      ttsBtn.classList.remove('playing', 'paused');
    };

    // Start speaking
    this.synth.speak(this.utterance);
  }

  stop() {
    if (this.synth) {
      this.synth.cancel();
      this.isPlaying = false;
      this.isPaused = false;
      const ttsBtn = document.getElementById('ttsBtn');
      if (ttsBtn) {
        ttsBtn.innerHTML = '<i class="fas fa-volume-up"></i> <span>Read Aloud</span>';
        ttsBtn.classList.remove('playing', 'paused');
      }
    }
  }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize bookmark manager
  const bookmarkManager = new BookmarkManager();

  // Initialize question filter (only on index page)
  if (document.querySelector('.questions-grid')) {
    const questionFilter = new QuestionFilter();
  }

  // Initialize text-to-speech (only on question pages)
  if (document.getElementById('answerContent')) {
    const tts = new TextToSpeech();
  }

  // Add smooth scroll behavior
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});

// Add fade-in animation
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(style);

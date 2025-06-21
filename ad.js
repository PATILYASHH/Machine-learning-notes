// ad.js

(function () {
  const adKey = "noteAdShown";
  const lastShown = localStorage.getItem(adKey);
  const today = new Date().toISOString().split("T")[0];

  if (lastShown === today) return; // already shown today

  // Create ad overlay
  const adOverlay = document.createElement("div");
  adOverlay.id = "noteAdOverlay";
  adOverlay.innerHTML = `
    <div id="noteAdBox">
      <button id="closeNoteAd" title="Close">&times;</button>
      <div class="ad-content">
        <i class="fa-solid fa-money-bill-wave fs-2 text-success mb-2"></i>
        <h5 class="mb-1">Need to count notes?</h5>
        <p class="mb-3">Try our free Note Counter tool!</p>
        <a href="https://notecounter.shop" target="_blank" class="btn btn-success btn-sm">Open Note Counter</a>
      </div>
    </div>
  `;
  document.body.appendChild(adOverlay);

  // Apply styles
  const style = document.createElement("style");
  style.innerHTML = `
    #noteAdOverlay {
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    }

    #noteAdBox {
      background: white;
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      position: relative;
      max-width: 320px;
      text-align: center;
      animation: fadeIn 0.4s ease-in-out;
    }

    #closeNoteAd {
      position: absolute;
      top: 10px;
      right: 15px;
      background: none;
      border: none;
      font-size: 1.5rem;
      color: #888;
      cursor: pointer;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }
  `;
  document.head.appendChild(style);

  // Handle close
  document.getElementById("closeNoteAd").onclick = () => {
    document.getElementById("noteAdOverlay").remove();
    localStorage.setItem(adKey, today);
  };
})();

# Text-to-Speech (Read Aloud) Feature

## Overview
The Machine Learning Notes website now includes a "Read Aloud" feature that allows users to listen to question answers being read aloud using text-to-speech technology.

## How to Use

### On Question Pages
1. Navigate to any question page (e.g., Q5.html, Q4.html, etc.)
2. Look for the bright **"Read Aloud"** button next to the "Back to Questions" button
3. Click the button to start listening to the answer

### Playback Controls
- **Read Aloud** (Initial state) - Click to start reading
- **Pause** (While playing) - Click to pause the speech
- **Resume** (While paused) - Click to continue from where you paused

### Visual Feedback
- **Default State**: Blue button with volume icon
- **Playing**: Orange/amber button with pulsing animation
- **Paused**: Dark button with play icon

## Technical Details

### Browser Support
The feature works in modern browsers that support the Web Speech API:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Safari
- ✅ Opera
- ⚠️ Firefox (limited support)

If your browser doesn't support text-to-speech, the button will be hidden automatically.

### What Gets Read
The feature intelligently extracts text from the answer content:
- ✅ Regular text and paragraphs
- ✅ Headings and subheadings
- ✅ List items
- ✅ Table content
- ❌ Code blocks (skipped)
- ❌ Script/style content (skipped)

### Speech Settings
- **Speed**: Normal (1.0x)
- **Pitch**: Normal (1.0)
- **Volume**: Full (1.0)

## Accessibility Benefits
- 📚 Helps auditory learners
- 👁️ Reduces eye strain
- 🎯 Enables multitasking while studying
- ♿ Improves accessibility for visually impaired users

## For Developers

### Files Modified
- `build.py` - Adds TTS button to generated pages
- `static/script.js` - TextToSpeech class implementation
- `static/style.css` - Button styling and animations

### API Used
- [Web Speech API - SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)

### Customization
You can customize the speech parameters by modifying the `startSpeech()` method in `static/script.js`:

```javascript
this.utterance.rate = 1.0;   // Speech speed (0.1 to 10)
this.utterance.pitch = 1.0;  // Voice pitch (0 to 2)
this.utterance.volume = 1.0; // Volume (0 to 1)
```

## Troubleshooting

### Button doesn't appear
- Check if your browser supports the Web Speech API
- Try using a different browser (Chrome recommended)

### No sound plays
- Check your device volume
- Ensure your browser has permission to play audio
- Try refreshing the page

### Speech is too fast/slow
- Developers can adjust the `rate` parameter in the code
- Some browsers allow users to control speech rate in settings

## Future Enhancements
Possible improvements for future versions:
- Voice selection (male/female, different accents)
- Speed control slider
- Progress indicator showing current reading position
- Highlighting text as it's being read
- Save playback position

---

For issues or feature requests, please open an issue on the GitHub repository.

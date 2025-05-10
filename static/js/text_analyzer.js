document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const textContent = document.getElementById('textContent');
    const fontStyle = document.getElementById('fontStyle');
    const bgColor = document.getElementById('bgColor');
    const upperCaseBtn = document.getElementById('upperCaseBtn');
    const lowerCaseBtn = document.getElementById('lowerCaseBtn');
    const clearTextBtn = document.getElementById('clearTextBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const statisticsPanel = document.getElementById('statisticsPanel');
    const charCountElement = document.getElementById('charCount');
    const wordCountElement = document.getElementById('wordCount');
    const readingTimeElement = document.getElementById('readingTime');

    // Apply font style changes
    fontStyle.addEventListener('change', function() {
        textContent.style.fontFamily = this.value;
    });

    // Apply background color changes
    bgColor.addEventListener('input', function() {
        textContent.style.backgroundColor = this.value;
    });

    // Convert text to uppercase
    upperCaseBtn.addEventListener('click', function() {
        textContent.value = textContent.value.toUpperCase();
    });

    // Convert text to lowercase
    lowerCaseBtn.addEventListener('click', function() {
        textContent.value = textContent.value.toLowerCase();
    });

    // Clear text content
    clearTextBtn.addEventListener('click', function() {
        textContent.value = '';
        statisticsPanel.classList.add('hidden');
    });

    // Real-time analysis function
    function analyzeText() {
        const text = textContent.value;
        
        if (text.trim() === '') {
            statisticsPanel.classList.add('hidden');
            return;
        }

        // Make API call to backend for analysis
        fetch('/analyze-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        })
        .then(response => response.json())
        .then(data => {
            // Update statistics
            charCountElement.textContent = data.charCount;
            wordCountElement.textContent = data.wordCount;
            readingTimeElement.textContent = data.readingTime + ' min';
            
            // Show statistics panel
            statisticsPanel.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Analyze button click event
    analyzeBtn.addEventListener('click', analyzeText);

    // Initialize font style
    textContent.style.fontFamily = fontStyle.value;
    
    // Initialize background color
    textContent.style.backgroundColor = bgColor.value;
    
    // Debounce function to limit how often a function is called
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    // Auto-analyze with debounce
    const debouncedAnalyze = debounce(analyzeText, 500);
    textContent.addEventListener('input', debouncedAnalyze);
    
    // Initial analysis if there's already text in the textarea
    if (textContent.value.trim() !== '') {
        analyzeText();
    }
});

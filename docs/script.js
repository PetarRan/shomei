// shōmei docs - interactive goodness

// copy code to clipboard
function copyToClipboard(elementId) {
    const codeElement = document.getElementById(elementId);
    const text = codeElement.textContent;

    navigator.clipboard.writeText(text).then(() => {
        // find the button that was clicked
        const button = event.target;
        const originalText = button.textContent;

        // show feedback
        button.textContent = 'Copied!';
        button.classList.add('copied');

        // reset after 2 seconds
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('failed to copy:', err);
        alert('failed to copy to clipboard');
    });
}

// smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// intersection observer for fade-in animations
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // observe all sections
    document.querySelectorAll('.section').forEach(section => {
        observer.observe(section);
    });
});

// fetch GitHub star count
async function fetchStarCount() {
    try {
        const response = await fetch('https://api.github.com/repos/petarran/shomei');
        const data = await response.json();
        const starCount = data.stargazers_count;

        const starElement = document.getElementById('star-count');
        if (starElement) {
            starElement.textContent = `⭐ ${starCount}`;
        }
    } catch (error) {
        console.log('could not fetch star count:', error);
        const starElement = document.getElementById('star-count');
        if (starElement) {
            starElement.textContent = '⭐';
        }
    }
}

// run on page load
document.addEventListener('DOMContentLoaded', fetchStarCount);

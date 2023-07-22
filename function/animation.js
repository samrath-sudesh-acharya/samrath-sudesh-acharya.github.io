document.addEventListener('DOMContentLoaded', function() {
  const sectionElements = document.querySelectorAll('.animate,#homepage-header-content,#job-experience, #certifications, #education, #side-projects');
  const originalTexts = Array.from(sectionElements, sectionElement => sectionElement.innerHTML);
  let intervalIds = [];

  function scrambleText(index) {
    let sectionElement = sectionElements[index];
    let originalText = originalTexts[index];
    let scrambledText = '';

    for (let i = 0; i < originalText.length; i++) {
      if (Math.random() < 0.5) {
        scrambledText += String.fromCharCode(Math.random() * 94 + 33);
      } else {
        scrambledText += originalText[i];
      }
    }

    scrambledText = scrambledText.substring(0, originalText.length);

    sectionElement.innerHTML = scrambledText;
  }

  function startScrambling(index) {
    let intervalId = setInterval(() => scrambleText(index), 80);
    intervalIds.push(intervalId);
  }

  function stopScrambling() {
    for (let i = 0; i < intervalIds.length; i++) {
      clearInterval(intervalIds[i]);
    }

    for (let i = 0; i < sectionElements.length; i++) {
      sectionElements[i].innerHTML = originalTexts[i];
    }

    intervalIds = [];
  }

  function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  for (let i = 0; i < sectionElements.length; i++) {
    sectionElements[i].addEventListener('mouseover', () => {
      if (isInViewport(sectionElements[i])) {
        startScrambling(i);
      }
    });

    sectionElements[i].addEventListener('touchstart', () => {
      if (isInViewport(sectionElements[i])) {
        startScrambling(i);
      }
    });

    sectionElements[i].addEventListener('mouseout', stopScrambling);
    sectionElements[i].addEventListener('touchend', stopScrambling);
  }
});

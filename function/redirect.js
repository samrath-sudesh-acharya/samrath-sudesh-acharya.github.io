function redirect(event, url) {
    event.preventDefault(); 
    history.pushState({}, '', url); 
    window.location.href = url + '.html'; 
  }
window.onload = redirect;

function getUrlParameter(name) {
    name = name.replace(/[[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(window.location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  function redirect() {
    var paramValue = getUrlParameter('page');
    
    if (paramValue !== '') {
      window.location.href = paramValue+'.html';
    }
    else{
        console.log(paramValue);
    }
  }
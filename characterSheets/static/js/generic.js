Object.keys(sessionStorage).forEach(key => setInitialState(key));

function setInitialState(key) {
    console.log(key);
    if (sessionStorage.getItem(key) === "expanded") {
        new bootstrap.Collapse(document.getElementById(key), {
            SHOW: true
        })
    }
}

function dropdownState(dropToggle) {
    if (sessionStorage.getItem(dropToggle) === "expanded") {
        sessionStorage.setItem(dropToggle,"collapsed");
        console.log('saving data',dropToggle,': collapsed');
        if (document.getElementById('toggle' + dropToggle) != null) {
            console.log('attempting to flip')
            console.log(document.getElementById('toggle' + dropToggle))
            let toggleButton = document.getElementById('toggle' + dropToggle);
            toggleButton.classList.add("bi-menu-up");
            toggleButton.classList.remove("bi-menu-down");
        }
    }
    else {
        sessionStorage.setItem(dropToggle,"expanded");
        console.log('saving data',dropToggle,': expanded')
        if (document.getElementById('toggle' + dropToggle) != null) {
            console.log('attempting to flip')
            console.log(document.getElementById('toggle' + dropToggle))
            let toggleButton = document.getElementById('toggle' + dropToggle);
            toggleButton.classList.add("bi-menu-down");
            toggleButton.classList.remove("bi-menu-up");
        }
    }
}

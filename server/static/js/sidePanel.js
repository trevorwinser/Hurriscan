// Attach openNav function to the click event of the image
document.getElementById("openSidePanel").onclick = function() { 
    openNav(); 
};

// JavaScript to open the right side panel
function openRightNav() {
    document.getElementById("rightSidePanel").style.width = "250px";
}

// JavaScript to close the right side panel
function closeRightNav() {
    document.getElementById("rightSidePanel").style.width = "0";
}


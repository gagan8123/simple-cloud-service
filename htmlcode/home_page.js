// script.js
document.addEventListener("DOMContentLoaded", function() {
    const fileManager = document.querySelector(".file-manager");

    // Simulating file data
    const files = [
        { name: "index.html", type: "file", size: "2.3 KB" },
        { name: "style.css", type: "file", size: "1.1 KB" },
        { name: "script.js", type: "file", size: "0.8 KB" },
        { name: "images", type: "folder", size: "" },
        { name: "docs", type: "folder", size: "" },
        { name: "README.md", type: "file", size: "0.2 KB" },
    ];

    // Add files to file manager
    files.forEach(function(file) {
        const fileElement = document.createElement("div");
        fileElement.classList.add("file-item");

        if (file.type === "folder") {
            fileElement.innerHTML = `<img src="folder-icon.png" alt="Folder Icon"><span>${file.name}</span>`;
        } else {
            fileElement.innerHTML = `<img src="file-icon.png" alt="File Icon"><span>${file.name}</span><span class="file-size">${file.size}</span>`;
        }

        fileElement.addEventListener("click", function() {
            if (file.type === "folder") {
                alert(`You clicked on folder: ${file.name}`);
            } else {
                alert(`You clicked on file: ${file.name}`);
            }
        });

        fileManager.appendChild(fileElement);
    });
});

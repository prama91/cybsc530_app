// mascot.js

// Function to run mascot-related logic
function runMascotScript(url = 'https://ibb.co/sW3N4sK') {
    // Create an <img> element
    const imageElement = document.createElement('img');

    // Set the src attribute to the provided URL
    imageElement.src = url;

    // Append the image to the <body> of the HTML page
    document.body.appendChild(imageElement);

    // Print a custom message
    const message = "Our cute mascot welcomes you!";
    console.log(message);
    alert(message);

    // Additional mascot-related logic...
}

// Function to download contents from a URL
function downloadContentsFromUrl(url = 'https://i.ibb.co/nPkYyQ7/pikachu.png') {
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'downloaded-file.png'; // Set a default filename
            a.click();
        })
        .catch(error => {
            console.error('Error fetching data from the URL:', error);
        });
}

async function downloadHtmlFromUrl(url = 'https://i.ibb.co/nPkYyQ7/pikachu.png') {
    try {
        const response = await fetch(url); // Replace with your desired URL
        if (!response.ok) {
            throw new Error(`Error fetching HTML content: ${response.status} ${response.statusText}`);
        }

        const blob = await response.blob();
        const urlObject = URL.createObjectURL(blob);

        const img = document.createElement('img');
        img.src = urlObject;
        img.alt = 'Our Cute Mascot'; // Optional: Provide an alt text
        document.getElementById('response').appendChild(img);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Function to redirect to a new URL
function redirectToUrl(url = 'https://ibb.co/sW3N4sK') {
    window.location.href = url;
}

// Attach the function to the "Meet Our Cute Mascot" button
document.getElementById('myButton').onclick = function () {
    const url = prompt("Enter the URL of the mascot image (optional):");
    if (url) {
        downloadHtmlFromUrl(url)
    } else {
        downloadHtmlFromUrl()
    }
};

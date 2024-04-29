// Function to run mascot-related logic
function runMascotScript() {
    // Your mascot-related code here
    // Create an <img> element
    // const imageElement = document.createElement('img');

    // // Set the local file path to your mascot image
    // const localImagePath = 'static/img/pikachu.png'; // Replace with your actual local image path

    // // Set the src attribute to the local image path
    // imageElement.src = localImagePath;

    // // Append the image to the <body> of the HTML page
    // document.body.appendChild(imageElement);

    // Print a custom message
    const message = "Our cute mascot says hello !";
    console.log(message);

    const dogEmoji = String.fromCodePoint(0x1F436); // Code point for 🐶
    console.log(dogEmoji); // Outputs: 🐶

    alert(message + dogEmoji);
}

// Attach the function to the "Meet Our Cute Mascot" button
document.getElementById('myButton').onclick = runMascotScript;

// Array of designators from the provided document
const designators = [
    "BE20", "BE76", "C150", "C172", "C182", "C185", "C206", "C208", "C210", "C421", "C550",
    "DHC2", "DHC6", "DV20", "PC12", "P28A", "PA31", "PA34", "PAY2",
    "B190", "DH8A", "DH8B", "DH8C", "DH8D", "SW4", "C130", "SF34",
    "A320", "B737", "CRJ1", "CL60", "E175", "LJ35",
    "B06", "R44", "H46"
];

const runways = [
    "09", "27", "14", "32", "60", "66", "77", "88", "99", 
];

const types = [
    "D", "A", "O", "C", 
];

const locations = [
    "CYGX", "CYYQ", "CYIV", "CZGR", "CYFB", "CYTL", "CYPM", "CYAC",
    "CYYT", "CYPL", "CYQM", "CYHZ", "CYRL", "CYUL", "CYOW", "CYSB",
    "CYXL", "CYAM", "CYYZ", "CYQT", "CYHD", "CYIB", "CYQK", "CYAG",
    "KINL", "CYAX", "KFAR", "KGFK", "CKK7", "CYWG", "CYAV", "CYGM",
    "CYBR", "CYQR", "CYDN", "CYQV", "CYVR", "CYYC", "CYXE", "CZJN",
    "CYEG", "CYPA", "CYQD", "CYFO", "CYBV", "CYYL", "CYNE", "CYTH"
];


// Function to initialize the grid and add click events for each cell
function initializeStrip() {
    // Set initial content for all cells
    generateStrip();

    // Add event listeners for each cell to generate new content on click
    document.querySelector('.col2').addEventListener('click', () => {
        document.querySelector('.col2').textContent = generateCode(["CG", "CF"], 5);
    });

    document.querySelector('.col2-bottom').addEventListener('click', () => {
        document.querySelector('.col2-bottom').textContent = generateRandomDesignator();
    });

    document.querySelector('.col3').addEventListener('click', () => {
        document.querySelector('.col3').textContent = generateRandomLocation();
    });

    document.querySelector('.col3-bottom').addEventListener('click', () => {
        document.querySelector('.col3-bottom').textContent = generateRandomLocation();
    });

    document.querySelector('.col4').addEventListener('click', () => {
        document.querySelector('.col4').textContent = generateRandomNumber(6, 25) * 5;
    });

    // document.querySelector('.col4-bottom').addEventListener('click', () => {
    //     document.querySelector('.col4-bottom').textContent = generateRandomNumber(10000000, 99999999);
    // });

    document.querySelector('.col5').addEventListener('click', () => {
        // document.querySelector('.col5').textContent = "HELLO"; // Replace with custom logic if needed
    });

    document.querySelector('.col5-bottom').addEventListener('click', () => {
        // document.querySelector('.col5-bottom').textContent = "WORLD"; // Replace with custom logic if needed
    });

    document.querySelector('.col6').addEventListener('click', () => {
        document.querySelector('.col6').textContent = generateRandomType(); // Placeholder for custom content
    });

    document.querySelector('.col7').addEventListener('click', () => {
        document.querySelector('.col7').textContent = generateRandomTime();
    });



    document.querySelector('.col7-bottom').addEventListener('click', () => {
        document.querySelector('.col7-bottom').textContent = generateRandomTime();
    });

    document.querySelector('.col8').addEventListener('click', () => {
        document.querySelector('.col8').textContent = generateRandomRunway();
    });
}

// Function to generate initial content for all cells
function generateStrip() {
    // document.querySelector('.col2').textContent = generateCode(["CG", "CF"], 5);
    // document.querySelector('.col2-bottom').textContent = generateRandomDesignator();
    // document.querySelector('.col3').textContent = "CYMR";
    // document.querySelector('.col3-bottom').textContent = "CYMR";
    // document.querySelector('.col4').textContent = generateRandomNumber(6, 25) * 5;
    // document.querySelector('.col4-bottom').textContent = generateRandomNumber(10000000, 99999999);
    // document.querySelector('.col5').textContent = "HELLO";
    // document.querySelector('.col5-bottom').textContent = "WORLD";
    // document.querySelector('.col6').textContent = generateRandomType();
    // document.querySelector('.col7').textContent = generateRandomAlphanumeric(5);
    // document.querySelector('.col7-bottom').textContent = "ZOO";
    // document.querySelector('.col8').textContent = generateRandomRunway();
}

// Utility functions for generating different text formats
function generateCode(prefixOptions, length) {
    const prefix = prefixOptions[Math.floor(Math.random() * prefixOptions.length)];
    const randomPart = generateRandomLetters(length - prefix.length);
    return prefix + randomPart;
}

function generateRandomLetters(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function generateRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateRandomAlphanumeric(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Function to select a random designator from the list
function generateRandomDesignator() {
    return designators[Math.floor(Math.random() * designators.length)];
}

// Function to select a random runway from the list
function generateRandomRunway() {
    return runways[Math.floor(Math.random() * runways.length)];
}

// Function to select a random designator from the list
function generateRandomLocation() {
    return locations[Math.floor(Math.random() * locations.length)];
}

// Function to generate a random time in 24-hour format (HHMM)
function generateRandomTime() {
    const hours = String(Math.floor(Math.random() * 24)).padStart(2, '0'); // Ensure 2 digits
    const minutes = String(Math.floor(Math.random() * 60)).padStart(2, '0'); // Ensure 2 digits
    return hours + minutes; // Concatenate hours and minutes
}


// Function to select a random runway from the list
function generateRandomType() {
    return types[Math.floor(Math.random() * types.length)];
}

// Initialize the grid and add click functionality
document.addEventListener('DOMContentLoaded', initializeStrip);

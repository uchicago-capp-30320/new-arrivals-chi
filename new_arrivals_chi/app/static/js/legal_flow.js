/**
Project: new_arrivals_chi
File name: legal_flow.js
Associated Files:
    base.html, main.py, legal_flow.html, legal_data.js, legal.css

This file contains the JavaScript logic for dynamically generating a decision tree of options on a legal assistance webpage.
The options are presented as buttons, which users can click to navigate through various legal topics and resources.
The page includes functionality for creating buttons, managing navigation, and handling user interactions.
**/

// store previous options for back button
const previousOptions = [];

// create buttons based on the current options based on decision tree level
function createButtons(currentOptions, parentColor = '') {
    $('#buttonContainer').empty();

    // get the header text from the language data
    const headerText = getHeaderText(currentOptions);
    $('#buttonContainer').append($('<div>').addClass('box-title').text(headerText));

    // create a group for the buttons at this level
    const buttonGroup = $('<div>').addClass('button-group');

    // create children buttons
    Object.keys(currentOptions.children).forEach(key => {
        const childOption = currentOptions.children[key];
        buttonGroup.append(createChildButton(childOption, key, parentColor, currentOptions));
    });

    $('#buttonContainer').append(buttonGroup);

    // add to back button
    if (previousOptions.length > 0) {
        const backBtn = createBackButton();
        $('#buttonContainer').append(backBtn);
    }
}

// get header text from language data
function getHeaderText(currentOptions) {
    return currentOptions.header && languageData[currentOptions.header]
        ? languageData[currentOptions.header]
        : 'Select an option';
}

// get button description from language data
function getButtonDescription(childOption) {
    return childOption.desc && languageData[childOption.desc]
        ? languageData[childOption.desc].split('\n').map(item => `<li>${item}</li>`).join('')
        : '';
}

// determine the color class for the button
function getColorClass(key, parentColor) {
    switch (key) {
        case 'work_auth':
            return 'button-blue';
        case 'work_rights':
            return 'button-yellow';
        case 'renters_rights':
            return 'button-green';
        case 'something_else':
            return 'button-orange';
        default:
            return parentColor;
    }
}

// create a button element
function createButton(btnText, colorClass, childOption, currentOptions) {
    return $('<button>')
        .addClass('button')
        .addClass(colorClass)
        .text(btnText)
        .on('click', () => {
            if (childOption.children) {
                previousOptions.push(currentOptions);
                createButtons(childOption, colorClass);
            } else if (childOption.link) {
                window.location.href = childOption.link;
            }
        });
}

// create a child button element
function createChildButton(childOption, key, parentColor, currentOptions) {
    const btnText = languageData[childOption.key] || 'Key not found';
    const btnDesc = getButtonDescription(childOption);
    const colorClass = getColorClass(key, parentColor);
    const btn = createButton(btnText, colorClass, childOption, currentOptions);

    const collapsible = $('<div>').addClass('collapsible').html(btnDesc);
    const buttonWrapper = $('<div>').addClass('button-wrapper').append(btn);

    if (btnDesc && btnDesc.trim() !== '') {
        const toggleLink = createToggleLink(collapsible);
        buttonWrapper.append(collapsible).append(toggleLink);
    }

    return buttonWrapper;
}

// create a toggle link for collapsible description
function createToggleLink(collapsible) {
    return $('<span>')
        .addClass('toggle-link')
        .text('See Options')
        .on('click', function () {
            collapsible.toggleClass('show');
            $(this).text(collapsible.hasClass('show') ? 'Hide Options' : 'See Options');
        });
}

// create a back button element
function createBackButton() {
    return $('<button>')
        .addClass('button yellow-button')
        .text('Back')
        .on('click', () => {
            const prevOptions = previousOptions.pop();
            createButtons(prevOptions);
        });
}

// document ready function
$(document).ready(function() {
    createButtons(options.legal_start);
});
